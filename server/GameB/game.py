import random
import math
import copy
from collections import OrderedDict

from .player import Player
import time


def current_milli_time():
    return round(time.time() * 1000)

class Game():
    def __init__(self, num_players=2, min_spread=1, max_spread=5, card_range_low=1, card_range_high=10, password=""):
        """
        Initializes Game B

        :param num_players: (int) Number of players
        :param min_spread: (int) Minimum spread required for the market
        :param max_spread: (int) Maximum spread required for the market
        :param card_range_low: (int) Minimum number for card range
        :param card_range_high: (int) Maximum number for card range
        :param password: (string) Optional password. If not provided, will be auto-generated.
        """
        # Initialize variables
        self.num_players = num_players
        self.original_num_players = num_players
        self.min_spread = min_spread
        self.max_spread = max_spread
        self.card_range_low = card_range_low
        self.card_range_high = card_range_high
        self.players = OrderedDict()
        self.all_players = list(range(self.num_players))
        self.trade_log = {}
        self.turn = 0
        self.roundTurn = 0
        self.true_value = 0
        self.last_state = None
        self.true_pnl = OrderedDict([(i,0) for i in range(self.num_players)])
        self.status = 0 # 0 represents a game that hasn't started. 1 represents a game that is in progress. 2 represents a game that is over.
        # Create card deck
        # list(range(card_range_low, card_range_high + 1)
        self.cards = [i for i in range(card_range_low, card_range_high + 1)]
        # Shuffle cards
        random.seed(current_milli_time())
        random.shuffle(self.cards)

        # self.round_order = [i for i in range(self.num_players)]
        self.transaction_counter = 0

        # Initialize market variables
        self.last_bid = None
        self.last_bid_lots = None
        self.last_ask = None
        self.last_ask_lots = None
        self.new_market = True
        # Initialize revealed_cards
        self.revealed_cards = []
        
        # Generate password if not actually provided.
        if password:
            self.password = password
        else:
            self.password = str(random.random())

    ####################
    #     SETTERS      #
    ####################
    def make_market(self, player, bid, bid_lots, ask, ask_lots):
        """
        Player submits the new market

        :param player:
        :param bid: (int) Bids for market
        :param bid_lots: (int) Number of bid lots
        :param ask: (int) Asks for market
        :param ask_lots: (int) Number of ask lots
        :return:
        """
        # Checking if the player is at the right turn
        err = self.check_turn(player)
        if err != None:
            raise Exception(err)

        # Temporary variables
        p = player
        spread = ask - bid

        # Undo
        self.last_state = copy.deepcopy(self)
        # Save space
        self.last_state.last_state = None

        # First player of the game
        if self.new_market:
            if spread < self.min_spread:
                raise Exception("Spread is less than minimum spread. Enter a wider spread.")
            elif spread > self.max_spread:
                raise Exception("Spread is greater than maximum spread. Enter a narrower spread.")
            self.game_locked = True
        # Subsequent turns
        else:
            if self.last_ask - self.last_bid == self.min_spread:
                raise Exception("Must transact.  We are at the minimum spread.")
            elif spread < self.min_spread:
                raise Exception("Spread is less than minimum spread. Enter a wider spread.")
            elif spread > self.max_spread:
                raise Exception("Spread is greater than maximum spread. Enter a narrower spread.")
            elif bid < self.last_bid:
                raise Exception("Bid is less than the previous bid. Enter a higher bid.")
            elif ask > self.last_ask:
                raise Exception("Ask is greater than the previous ask. Enter a lower ask.")
            elif spread == self.last_ask - self.last_bid:
                raise Exception("Spread is the same as the last spread. Enter a narrower spread.")

        # Pass the variable on
        p.make_market(self.turn, bid, bid_lots, ask, ask_lots)

        # Set new variables based on new market
        self.last_market_maker = p
        self.last_bid = bid
        self.last_ask = ask
        self.last_bid_lots = bid_lots
        self.last_ask_lots = ask_lots
        # Add to trade log
        if self.turn in self.trade_log:
            self.trade_log[self.turn] = (self.trade_log[self.turn], {'player': player.player_id,
                                     'action': 'made market',
                                     'bid': bid,
                                     'bid_lots': bid_lots,
                                     'ask': ask,
                                     'ask_lots': ask_lots})
        else: 
            self.trade_log[self.turn] = {'player': player.player_id,
                                        'action': 'made market',
                                        'bid': bid,
                                        'bid_lots': bid_lots,
                                        'ask': ask,
                                        'ask_lots': ask_lots}
        # Boolean to verify if first market created
        self.new_market = False

        # If last person in round, create a new set of rotation
        print("Market", self.roundTurn, self.turn, self.num_players, list(self.players.keys()))
        if self.roundTurn == self.num_players - 1:
            self.shuffle_round_order(player)
        # Increment each turn
        self.turn = self.turn + 1
        self.roundTurn = (self.roundTurn + 1) % self.num_players
        print("Updated turns:", self.turn, self.roundTurn)
        return "SPREAD SUCCESS"

    def start(self):
        # Distribute cards to each player
        id = 0
        for player in self.players: 
            # player is the key
            card = self.distribute_card()
            self.true_value += card
            p = Player(id, card, player)
            self.players[player] = p
            id += 1
        self.status = 1
        self.num_players = len(self.players)
        
        # Generate turn sequence
        turn_sequence = [i for i in range(self.num_players)]
        random.seed(current_milli_time())
        random.shuffle(turn_sequence)
        self.round_order = turn_sequence
    
    def add_user(self, player):
        if self.status != 0:
            return
        if len(self.players) >= self.num_players:
            return
        self.players[player] = None # initialize the player within the dict, but the value will be None.
        
    def transact(self, player, position, quantity):
        """
        Player makes a transaction. Max one transaction per turn. Will error after that.

        :param player: (player) Player class
        :param position: (str) "Buy": to buy, "Sell": to sell (case insensitive)
        :param quantity: (int) Number of lots
        :return:
        """
        # Checks if the correct turn for player
        err = self.check_turn(player)
        if err != None:
            raise Exception(err)
        err = self.check_transact_conditions()
        if err != None:
            raise Exception(err)

        # Undo
        self.last_state = copy.deepcopy(self)
        # Save space
        self.last_state.last_state = None

        # Calls the corresponding player class
        p = player
        price = 0
        if position == 'BUY':
            if quantity > self.last_ask_lots:
                raise Exception("{} total available lots. Enter a value less than or equal to that.".format(self.last_ask_lots))

            # Current player buys from previous player
            p.buy_from(self.turn, self.last_market_maker, self.last_ask, quantity)

            # Previous player sells to current player
            price = self.last_ask
            self.last_market_maker.sell_to(self.turn, p, self.last_ask, quantity)

        # If the player clicks on the sell button
        elif position == 'SELL':
            if quantity > self.last_bid_lots:
                raise Exception(
                    "{} total available lots. Enter a value less than or equal to that.".format(self.last_bid_lots))

            # Current player sells to previous player
            p.sell_to(self.turn, self.last_market_maker, self.last_bid, quantity)

            # Previous player buys from current player
            price = self.last_bid
            self.last_market_maker.buy_from(self.turn, p, self.last_bid, quantity)
        # Updates corresponding trade log
        self.trade_log[self.turn] = {'player': player.player_id,
                                     'action': position,
                                     'quantity': quantity,
                                     'price': price,
                                     'market maker': self.last_market_maker.player_id}
        self.new_market = True
        # Increment transaction counter
        self.transaction_counter += 1

        # TODO: This API HAS NOT BEEN MADE YET! HOW TO PUSH THIS
        if self.transaction_counter % 2 == 0:
            self.reveal_card()
        return "TRANSACTION SUCCESS"

    def stall(self, player):
        """
        If player does not make any moves within the given time
        :param player: (player) Player class
        """
        # If first player, make a new market based on generic prediction
        if self.new_market:
            predicted_price = int((self.card_range_low + self.card_range_high) * self.num_players / 2)
            self.make_market(player, bid=predicted_price - math.floor(self.max_spread / 2), bid_lots=random.randint(5, 20), ask=predicted_price + math.floor(self.max_spread / 2), ask_lots=random.randint(5, 20))
            return "SPREAD SUCCESS"
        # If previous market is already at minimum spread
        elif self.last_ask - self.last_bid == self.min_spread:
            # 0: Sell, 1: Buy
            buy_or_sell = random.randint(0, 1)
            if buy_or_sell == 0:
                quantity = random.randint(2, self.last_bid_lots)
                self.transact(player, "SELL", quantity)
            elif buy_or_sell == 1:
                quantity = random.randint(2, self.last_ask_lots)
                self.transact(player, "BUY", quantity)
            return "TRANSACTION SUCCESS"
        # If previous market is 1 larger than the minimum spread
        elif self.last_ask - self.last_bid == self.min_spread + 1:
            # 0: Change Bid, 1: Change Ask
            change_bid_or_ask = random.randint(0, 1)
            if change_bid_or_ask == 0:
                return self.make_market(player, bid=self.last_bid+1, bid_lots=random.randint(5, 20), ask=self.last_ask, ask_lots=random.randint(5, 20))
            elif change_bid_or_ask == 1:
                return self.make_market(player, bid=self.last_bid, bid_lots=random.randint(5, 20), ask=self.last_ask-1, ask_lots=random.randint(5, 20))
            return "SPREAD SUCCESS"
        else:
            self.make_market(player, bid=self.last_bid+1, bid_lots=random.randint(5, 20), ask=self.last_ask-1, ask_lots=random.randint(5, 20))
            return "SPREAD SUCCESS"

    def drop(self, player):
        """
        If a player does not respond, we will drop them from the game.

        :param player: (player) Player class
        """
        
        # # Find the order of the dropped player
        # for i in sorted(self.all_players):
        #     dropped_player = i
        #     if self.players[i] == player:
        #         break
        
        
        print("round order", self.round_order)
        lst = list(self.players.keys())
        print("lst", lst)
        drop_index = -1
        for i in range(len(lst)):
            key = lst[i]
            if key == player: # this is the player who we want to drop
                drop_index = i
        print("drop_index", drop_index)
        if drop_index < 0:
            # player was not in the round order, just return (error?)
            return
        print("roundTurn", self.roundTurn)
        print("turn", self.turn)
        self.round_order.remove(drop_index) # remove that element (the element which is equal to drop_index)
        if drop_index < self.roundTurn: # player has already gone in this round
            self.roundTurn -= 1 # compensate for changing the order array

        # for all players that still need to go, if their index was above drop_index, decrement by 1
        for i in range(len(self.round_order)):
            val = self.round_order[i]
            if val > drop_index:
                self.round_order[i] -= 1
        
        player_obj = self.players.pop(player)
        # Subtract 1 from number of players
        self.num_players -= 1
        
        # Add card back to deck? Or not?
        # player_card = player_obj.card_value
        return "DROP SUCCESS"

    def undo(self):
        """
        Undoes the last action.
        """
        if not self.last_state:
            return self
        return self.last_state

    def set_true_pnl(self):
        """
        Calculates PNL for end game calculation

        :return:
        """
        true_pnls = OrderedDict()
        for k in self.players:
            player = self.players[k]
            true_pnl = player.calc_true_pnl(self.true_value)
            true_pnls[player.player_id] = true_pnl
        self.true_pnl = true_pnls

    ####################
    #     GETTERS      #
    ####################
    def get_revealed_cards(self):
        """
        Gets the total list of revealed cards
        :return:
        """
        return self.revealed_cards

    def get_most_recent_revealed_card(self):
        """
        Gets the most recently revealed card
        :return:
        """
        return self.revealed_cards[-1]

    def get_true_pnl(self):
        """
        Calculates PNL for end game calculation

        :return:
        """
        if self.status == 2:
            return self.true_pnl
        else:
            return {}

    def get_all_players_position(self):
        """
        Gets all players' positions

        :return: (dict) {0: -1, 1: 1} (int) Key: Player ID, (int) Value: Position
        """
        all_position = OrderedDict()
        for k in self.players:
            player = self.players[k]
            all_position[player.player_id] = player.get_position()
        return all_position

    def get_num_players(self):
        """
        Gets the number of players in the game

        :return: (int) Number of players in the game
        """
        return self.num_players

    def get_players_cards(self):
        """
        Gets each player's card value.

        :return: (dict) {0: 3, 1: 5} (int) Key: Player ID, (int) Value: Card value
        """
        card_values = OrderedDict()
        for k in self.players:
            player = self.players[k]
            card_values[player.player_id] = player.card_value
        return card_values

    def get_current_player(self):
        """
        Gets the player id of the current turn.

        :return: (int) Player ID of the current turn
        """

        idx = self.round_order[self.roundTurn]
        print(self.round_order)
        print(idx)
        lst = list(self.players.keys())
        print(lst)
        player = lst[idx]
        return player
        # TODO 
        # by using self.num_players, we are assuming that the room is full?
        # return self.round_order[self.turn % len(self.players)]

    def get_current_market(self):
        """
        Gets current market set by the last player.

        :return: (list) [Bid, Bid Size, Ask, Ask Size]
        """
        return [self.last_bid, self.last_bid_lots, self.last_ask, self.last_ask_lots]

    def get_trade_log(self):
        """
        Gets the trade log.

        :return: (dict)
        """
        return self.trade_log

    def get_current_spread(self):
        """
        Gets the most recent spread. 

        :return: (list) [(bid, bid_volume), (ask, ask_volume)]
        """
        spread = {"bid":{"price":self.last_bid, "volume": self.last_bid_lots}, "ask": {"price": self.last_ask, "volume": self.last_ask_lots}}
        return spread

    def get_true_sum(self):
        """
        Gets the true sum

        :return:
        """
        return self.true_value

    ####################
    # HELPER FUNCTIONS #
    ####################
    def distribute_card(self):
        """
        Distribute the first card in the deck.

        :return: (int) Distributed card
        """
        card = self.cards[0]
        if self.cards[1:]:
            self.cards = self.cards[1:]
        else:
            self.cards = []
        return card

    def reveal_card(self):
        """
        Reveals card after every 2 turns
        !!! DOES NOT PUSH THE NEW CARD OUT

        :return:
        """
        if self.cards:
            c = self.distribute_card()
            self.revealed_cards.append(c)

    def shuffle_round_order(self, current_player):
        """
        Shuffles round order in order to prevent same order each iteration

        :param current_player: (player) Player
        :return:
        """
        # List of all players
        # all_players = copy.deepcopy(self.all_players)
        # Randomly shuffle players
        # random.shuffle(all_players)
        # if self.num_players
        last_index = self.round_order[-1]
        lst = list(self.players.values())
        last_player = lst[last_index]
        turn_sequence = [i for i in range(self.num_players)]
        random.seed(current_milli_time())    
        random.shuffle(turn_sequence)
        next_player = lst[turn_sequence[0]]
        # Prevent same player from going twice in a row
        if next_player.player_id == last_player.player_id:
            turn_sequence[0], turn_sequence[1] = turn_sequence[1], turn_sequence[0] # swap first two people in this case. we already had "randomization" so this can be deterministic
        self.round_order = turn_sequence
        # self.round_order = copy.deepcopy(all_players)

    def check_transact_conditions(self):
        """
        Check if transactions are within the correct bounds

        :return:
        """
        err = None
        if self.turn == 0:
            err = "Must make market on first turn"
        elif self.new_market:
            err = "Must make market."
        return err

    def check_turn(self, player):
        """
        Checks if player is at the right number of turns

        :param player: (player) Player
        :return:
        """
        # idx = self.round_order[self.roundTurn]
        curr_id = self.get_current_player()
        # print(curr_id, player, player.username, self.roundTurn)
        if player.username != curr_id:
            return "Not your turn"
