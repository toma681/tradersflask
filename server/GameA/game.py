import numpy as np
import copy
from itertools import chain
from .player import Player
from .order_book import OrderBook


class Game:
    def __init__(self, true_values, num_players=5, num_rounds=5):
        self.num_players = num_players
        self.all_players = list(range(self.num_players))
        self.current_player = 0
        self.players = []
        self.num_rounds = num_rounds
        self.num_rounds_played = 0
        self.unrealized_pnls_history = []
        self.transactions_history = []
        self.lots_history = []
        self.avg_transactions_prices_history = []
        self.true_values = true_values
        self.end_game = False
        self.last_state = None
        self.market = [[0 for _ in range(6)] for _ in range(self.num_players)]

    def player_setup(self, player_names):
        """
        instantiates players
        """
        for i in range(self.num_players):
            self.players.append(self.make_player(player_names[i]))
            self.players[i].assign_bids_and_asks([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0])

    def next_turn(self):
        self.current_player = (self.current_player + 1) % self.num_players
        
    def play_round(self):
        if self.num_rounds_played >= self.num_rounds:
            print("Already played all rounds")
            return False

        # Undo
        self.last_state = copy.deepcopy(self)
        # Save space
        self.last_state.last_state = None

        self.show_market()
        
        # one transaction table for each round
        self.transactions_total_prices = np.zeros((3, self.num_players, self.num_players))  
        self.transactions_lots = np.zeros((3, self.num_players, self.num_players))

        self.unrealized_pnls = np.zeros((3, self.num_players))


        # Need players' prices + lots information to be ready within all the player objects now

        q1_bids, q2_bids, q3_bids, q1_asks, q2_asks, q3_asks = {}, {}, {}, {}, {}, {}
        for p in range(len(self.players)):
            player = self.players[p]
            q1_bids[p] = (player.q1_bids[-1][0], player.q1_bids[-1][1])
            q2_bids[p] = (player.q2_bids[-1][0], player.q2_bids[-1][1])
            q3_bids[p] = (player.q3_bids[-1][0], player.q3_bids[-1][1])
            q1_asks[p] = (player.q1_asks[-1][0], player.q1_asks[-1][1])
            q2_asks[p] = (player.q2_asks[-1][0], player.q2_asks[-1][1])
            q3_asks[p] = (player.q3_asks[-1][0], player.q3_asks[-1][1])

        # construct the order book objects for each question and send results of matching to transaction tables
        q1_bids_book, q1_asks_book = OrderBook(0, "BID", q1_bids), OrderBook(0, "ASK", q1_asks)
        self.transactions_total_prices[0], self.transactions_lots[0] = OrderBook.match(q1_bids_book, q1_asks_book, self.num_players, 0)
        
        q2_bids_book, q2_asks_book = OrderBook(1, "BID", q2_bids), OrderBook(1, "ASK", q2_asks)
        self.transactions_total_prices[1], self.transactions_lots[1] = OrderBook.match(q2_bids_book, q2_asks_book, self.num_players, 1)
        
        q3_bids_book, q3_asks_book = OrderBook(2, "BID", q3_bids), OrderBook(2, "ASK", q3_asks)
        self.transactions_total_prices[2], self.transactions_lots[2] = OrderBook.match(q3_bids_book, q3_asks_book, self.num_players, 2)

        self.calculate_pnls()  # self.unrealized_pnls and self.avg_transaction_price_for_q are now updated
        self.avg_transactions_prices_history.append(self.avg_transaction_price_for_q)
        self.unrealized_pnls_history.append(self.unrealized_pnls)
        self.transactions_history.append(self.transactions_total_prices)
        self.lots_history.append(self.transactions_lots)
        if self.num_rounds_played == self.num_rounds - 1:
            self.realized_pnls, self.lots = self.calculate_realized_pnls_and_lots()
            self.total_unrealized_pnls = np.array(self.unrealized_pnls_history[0])
            for urpnl in self.unrealized_pnls_history[1:]:
                self.total_unrealized_pnls += urpnl 
            self.pnls = self.realized_pnls + self.total_unrealized_pnls
        self.num_rounds_played += 1

        return "ROUND PlAYED"

    def calculate_realized_pnls_and_lots(self):
        net_lots = np.zeros((3, self.num_players)) # 3 is num questions
        realized_gains = np.zeros((3, self.num_players))

        for transaction_lots in self.lots_history:
            for q in range(3):
                for p in range(self.num_players):
                    net_lots[q, p] += sum(transaction_lots[q][p, :]) - sum(transaction_lots[q][:, p])

        for i, transaction_matrices in enumerate(self.transactions_history):
            for q in range(3):
                nonzero = (np.array(transaction_matrices[q]) > 0).astype(int)
                t = np.array(transaction_matrices[q])
                premiums = np.multiply(t - self.true_values[q] * self.lots_history[i][q], nonzero)
                for p in range(self.num_players):
                    realized_gains[q, p] += sum(premiums[:, p]) - sum(premiums[p, :])

        return realized_gains, net_lots
    
    def get_current_player(self):
        return self.players[self.current_player]
    def calculate_pnls(self):
        # calculate average transaction prices for each question (we'll use these to underscore the intermediate PnL)
        self.avg_transaction_price_for_q = [-1, -1, -1]
        for q in range(3):
            transactions_for_this_q = np.array(self.transactions_total_prices[q])
            if np.count_nonzero(transactions_for_this_q) == 0:
                self.avg_transaction_price_for_q[q] = 0
            else:
                self.avg_transaction_price_for_q[q] = np.nan_to_num(np.sum(transactions_for_this_q) / np.sum(self.transactions_lots[q]))

        for q in range(3):
            t = self.transactions_total_prices[q]
            nonzero = (np.array(t) > 0).astype(int)
            premiums = np.multiply(t - self.avg_transaction_price_for_q[q] * self.transactions_lots[q], nonzero)
            for p in range(self.num_players):
                self.unrealized_pnls[q, p] += sum(premiums[:, p]) - sum(premiums[p, :])

    def make_player(self, player_name=""):
        """
        Returns the validly-named player object that's just been created
        """
        if player_name == "":
            # random-letter-named player
            return Player(chr(np.random.random_integers(65,90)))
        else:
            return Player(player_name)

    def undo(self):
        """
        Undoes the last action.
        """
        if not self.last_state:
            return self
        return self.last_state

    ####################
    #     GETTERS      #
    ####################

    def get_last_transaction_history(self):
        """
        Gets the last transaction history
        :return:
        """
        if not self.transactions_history:
            return self.transactions_history[-1]

    def get_last_transaction_display(self):
        """
        Gets the display for last transactions.

        :return:
        """
        if not self.transactions_history:
            return [[[0 for _ in range(self.num_players)] for _ in range(self.num_players)] for _ in range(3)]

        last_transact = self.transactions_history[-1]
        last_lots = self.lots_history[-1]

        # Copy shape
        ret = np.zeros(last_lots.shape)
        # Fill in
        ret[:] = last_lots
        ret = ret.astype('str')
        for i in range(ret.shape[0]):
            for j in range(ret.shape[1]):
                for k in range(ret.shape[2]):
                    if last_lots[i][j][k] == 0:
                        ret[i][j][k] = '0'
                    else:
                        ret[i][j][k] = str(last_transact[i][j][k]/last_lots[i][j][k]) + "x" + str(int(last_lots[i][j][k]))

        # ret = [list(zip(chain(*l1), chain(*l2))) for l1, l2 in zip(last_transact, last_lots)]
        # for i in range(self.num_players):
        #     temp = [ret[i][j:j + self.num_players] for j in range(0, len(ret[i]), self.num_players)]
        #     ret[i] = temp
        #
        # for i in range(len(ret)):
        #     for j in range(len(ret[0])):
        #         for k in range(len(ret[0][0])):
        #             if type(ret[i][j][k]) is tuple and int(ret[i][j][k][1]) == 0:
        #                 ret[i][j][k] = 0
        #             else:
        #                 ret[i][j][k] = str(ret[i][j][k][0]/ret[i][j][k][1]) + "x" + str(int(ret[i][j][k][1]))
        return ret.tolist()

    def show_market(self):
        """
        Creates market display for game
        :return:
        """
        def format_market(bid_or_ask):
            price = bid_or_ask[0]
            quantity = bid_or_ask[1]
            return str(price) + "x" + str(quantity)
        res = []
        for i in range(self.num_players):
            temp = []
            player = self.players[i]
            temp.append(format_market(player.q1_bids[-1]))
            temp.append(format_market(player.q1_asks[-1]))

            temp.append(format_market(player.q2_bids[-1]))
            temp.append(format_market(player.q2_asks[-1]))

            temp.append(format_market(player.q3_bids[-1]))
            temp.append(format_market(player.q3_asks[-1]))

            res.append(temp)

        self.market = res

    def get_market(self):
        """
        Gets all the submitted values by the players

        :return: (list)
        """
        return self.market

    def get_pnl_table(self):
        """
        Gets the PnL table
        :return:
        """
        ret = self.unrealized_pnls_history[-1]

        round_number = len(self.unrealized_pnls_history)
        round_pnl = np.zeros((self.num_players,))

        for i in range(round_number):
            ret = np.vstack((ret, self.unrealized_pnls_history[i].sum(axis=0)))
            round_pnl += self.unrealized_pnls_history[i].sum(axis=0)

        return np.vstack((ret, round_pnl)).T

    def get_adjusted_pnl_table(self):
        """
        Gets the adjusted PnL table
        :return:
        """
        # Prevent display from returning none type
        if not self.unrealized_pnls_history:
            return [[0 for _ in range(9)] for _ in range(self.num_players)]

        # TODO: This part is pretty terribly written
        # If End Game
        if self.end_game:
            ret = self.calculate_realized_pnls_and_lots()[0].T
        else:
            ret = self.unrealized_pnls_history[-1].T

        for i in range(self.num_rounds_played):
            ret = np.hstack((ret, self.unrealized_pnls_history[i].T.sum(axis=1).reshape(self.num_players, 1)))

        if self.end_game:
            for i in range(4 - self.num_rounds_played):
                ret = np.hstack((ret, np.zeros((self.num_players, 1))))
            ret = np.hstack((ret, self.calculate_realized_pnls_and_lots()[0].T.sum(axis=1).reshape(self.num_players, 1)))
        else:
            for i in range(5 - self.num_rounds_played):
                ret = np.hstack((ret, np.zeros((self.num_players, 1))))

        ret = np.hstack((ret, ret[:, 3:].sum(axis=1).reshape(self.num_players, 1)))

        ret = np.around(ret, decimals=1)

        return ret.tolist()

    def get_num_players(self):
        """
        Gets the number of players in the game

        :return: (int) Number of players in the game
        """
        return self.num_players

    def get_avg_transactions_prices(self):
        """
        Gets the most recent average transaction prices
        :return:
        """
        if not self.avg_transactions_prices_history:
            return [0, 0, 0]
        else:
            ret = []
            for p in self.avg_transactions_prices_history[-1]:
                ret.append(round(p, 2))
            return ret
    # def __repr__(self):
    #     return self.all_players 