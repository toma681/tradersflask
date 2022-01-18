class Player():
    def __init__(self, player_id, card_value, username=""):
        """

        :param player_id: (int) Player ID value
        :param card_value: (int) Designed card for the game
        """
        self.player_id = player_id
        self.username = username
        self.card_value = card_value
        self.short_pos = []
        self.long_pos = []
        self.pnl = 0
        self.player_trade_log = {}
        self.last_bid = None
        self.last_bid_lots = None
        self.last_ask = None
        self.last_ask_lots = None
    
    def make_market(self, turn, bid, bid_lots, ask, ask_lots):
        """
        Creates a market for the next player

        :param turn: (int) The Nth turn of the game
        :param bid: (int) Price for bid
        :param bid_lots: (int) Number of lots for the bid
        :param ask: (int) Price for ask
        :param ask_lots: (int) Number of lots for the ask
        :return: (str) Confirmation of market
        """
        self.last_bid = bid
        self.last_bid_lots = bid_lots
        self.last_ask = ask
        self.last_ask_lots = ask_lots
        self.player_trade_log[turn] = {'bid': bid, 
                                    'bid_lots': bid_lots,
                                    'ask': ask,
                                    'ask_lots': ask_lots}
        return "Successfully made market"
    
    def buy_from(self, turn, counterparty, price, quantity):
        """
        Method for player to buy from previous player

        :param turn: (int) The Nth turn of the game
        :param counterparty: (player) Counter-party player
        :param price: (int) Price of transaction
        :param quantity: (int) Number of lots for transaction
        :return: (str) Confirmation of buying
        """
        self.long_pos.append(quantity)
        self.pnl -= price * quantity
        self.player_trade_log[turn] = {'action': 'buy',
                                        'price': price,
                                        'quantity': quantity,
                                        'counterparty': counterparty,
                                        'total_long_pos': sum(self.long_pos)}
        return "Successfully bought"
    
    def sell_to(self, turn, counterparty, price, quantity):
        """
        Method for player to sell to previous player

        :param turn: (int) The Nth turn of the game
        :param counterparty: (player) Counter-party player
        :param price: (int) Price of transaction
        :param quantity: (int) Number of lots for transaction
        :return: (str) Confirmation of buying
        """
        self.short_pos.append(quantity)
        self.pnl += price * quantity
        self.player_trade_log[turn] = {'action': 'sell',
                                        'price': price,
                                        'quantity': quantity,
                                        'counterparty': counterparty,
                                        'total_short_pos': sum(self.short_pos)}
        return "Successfully sold"
    
    def calc_true_pnl(self, true_val):
        """
        Calculates true PnL values from the sum of players' cards

        :param true_val: (int) true sum of players' cards
        :return: (int) True PnL
        """
        long_sum = sum(self.long_pos) * true_val
        short_sum = sum(self.short_pos) * true_val
        return long_sum - short_sum + self.pnl

    ####################
    #     GETTERS      #
    ####################

    def get_position(self):
        """
        Gets the current position

        Positive if long, Negative if short
        :return:
        """
        return sum(self.long_pos) - sum(self.short_pos)

    def get_card_value(self):
        """
        Gets player's card value
        :return:
        """
        return self.card_value

    def get_current_pnl(self):
        """
        Gets the current PnL of the player
        :return:
        """
        return self.pnl 
