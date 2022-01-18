import unittest
import numpy as np

from game import Game


class TestGameA(unittest.TestCase):

    def testGame(self):
        """
        Everyone has 1 lots
        """
        # True values of: 50, 100, 200, 3 Players, 5 Rounds
        g = Game([50, 100, 200], num_players=3, num_rounds=5)

        # Names of A, B, and C
        g.player_setup(["A", "B", "C"])

        g.players[0].assign_bids_and_asks([1, 40, 60, 1], [1, 90, 100, 1], [1, 190, 210, 1])
        g.players[1].assign_bids_and_asks([1, 50, 60, 1], [1, 80, 85, 1], [1, 100, 120, 1])
        g.players[2].assign_bids_and_asks([1, 70, 80, 1], [1, 110, 120, 1], [1, 300, 310, 1])

        g.play_round()

        # Round 1
        # Q1: Player 2 buys from Player 0 at (60+70)/2 = 65
        # Q2: Player 2 buys from Player 1 at (85+110)/2 = 97.5
        # Q3: Player 2 buys from Player 1 at (120+300)/2 = 210

        true_transaction_history = np.array([[[0, 0, 0], [0, 0, 0], [65, 0, 0]],
                                             [[0, 0, 0], [0, 0, 0], [0, 97.5, 0]],
                                             [[0, 0, 0], [0, 0, 0], [0, 210, 0]]])

        true_lots_history = np.array([[[0, 0, 0], [0, 0, 0], [1, 0, 0]],
                                      [[0, 0, 0], [0, 0, 0], [0, 1, 0]],
                                      [[0, 0, 0], [0, 0, 0], [0, 1, 0]]])

        self.assertIsNone(np.testing.assert_array_almost_equal(true_transaction_history, g.transactions_history[0]))
        self.assertIsNone(np.testing.assert_array_almost_equal(true_lots_history, g.lots_history[0]))


        g.players[0].assign_bids_and_asks([1, 40, 60, 2], [1, 90, 100, 1], [1, 190, 210, 1])
        g.players[1].assign_bids_and_asks([1, 50, 60, 1], [1, 80, 85, 2], [1, 100, 120, 2])
        g.players[2].assign_bids_and_asks([1, 70, 80, 2], [1, 110, 120, 1], [1, 300, 310, 1])

        g.play_round()

        # Round 2
        # Q1: Player 2 buys from Player 0 at (60+70)/2 = 65
        # Q2: Player 0 buys from Player 1 at (85+90)/2 = 87.5
        # Q2: Player 2 buys from Player 1 at (85+110)/2 = 97.5
        # Q3: Player 0 buys from Player 1 at (120+190)/2 = 155
        # Q3: Player 2 buys from Player 1 at (120+300)/2 = 210

        true_transaction_history = np.array([[[0, 0, 0], [0, 0, 0], [65, 0, 0]],
                                             [[0, 87.5, 0], [0, 0, 0], [0, 97.5, 0]],
                                             [[0, 155, 0], [0, 0, 0], [0, 210, 0]]])

        true_lots_history = np.array([[[0, 0, 0], [0, 0, 0], [1, 0, 0]],
                                      [[0, 1, 0], [0, 0, 0], [0, 1, 0]],
                                      [[0, 1, 0], [0, 0, 0], [0, 1, 0]]])

        self.assertIsNone(np.testing.assert_array_almost_equal(true_transaction_history, g.transactions_history[1]))
        self.assertIsNone(np.testing.assert_array_almost_equal(true_lots_history, g.lots_history[1]))

        g.end_game = True
    def testGame1(self):
        # True values of: 50, 100, 200, 3 Players, 5 Rounds
        g = Game([5, 10, 100], num_players=3, num_rounds=5)

        # Names of A, B, and C
        g.player_setup(["A", "B", "C"])

        g.players[0].assign_bids_and_asks([2, 5, 7, 2], [5, 10, 20, 5], [8, 100, 150, 8])
        g.players[1].assign_bids_and_asks([3, 10, 20, 4], [3, 10, 15, 3], [2, 70, 80, 2])
        g.players[2].assign_bids_and_asks([8, 15, 17, 8], [3, 17, 18, 4], [7, 90, 110, 7])

        g.play_round()

        #print(g.calculate_realized_pnls_and_lots())

        #print(g.transactions_history[-1])
        #print(g.transactions_history[-1].shape)

        #print(g.lots_history[-1])
        #print(g.lots_history[-1].shape)

        #print(g.get_last_transaction_display())

        realized_gains = np.zeros((3, 3))

        #print("lots history", g.lots_history[-1])

        for transaction_matrices in g.transactions_history:
            for q in range(3):
                nonzero = (np.array(transaction_matrices[q]) > 0).astype(int)
                t = np.array(transaction_matrices[q])
                #print(q, "nonzero", nonzero)
                #print(q, "t", t)
                premiums = np.multiply(t - g.true_values[q] * g.lots_history[-1][q], nonzero)
                #print(q, "premiums", premiums)
                for p in range(g.num_players):
                    realized_gains[q, p] += sum(premiums[:, p]) - sum(premiums[p, :])
        #print(realized_gains)
        #print(g.calculate_realized_pnls_and_lots())

    def testGame2(self):
        # True values of: 10, 50, 100, 3 Players, 5 Rounds
        g = Game([10, 50, 100], num_players=3, num_rounds=5)

        # Names of A, B, and C
        g.player_setup(["A", "B", "C"])

        g.players[0].assign_bids_and_asks([11, 12, 14, 12], [17, 57, 62, 11], [6, 93, 103, 11])
        g.players[1].assign_bids_and_asks([19, 18, 20, 6], [7, 60, 65, 10], [7, 64, 74, 8])
        g.players[2].assign_bids_and_asks([16, 20, 22, 11], [18, 45, 50, 8], [11, 99, 109, 9])

        g.play_round()

        #print(g.transactions_total_prices)

        # calculate average transaction prices for each question (we'll use these to underscore the intermediate PnL)
        unrealized_pnls = np.zeros((3, g.num_players))

        unrealized_pnls = np.zeros((3, g.num_players))
        for q in range(3):
            t = g.transactions_total_prices[q]
            #print("t", t)
            nonzero = (np.array(t) > 0).astype(int)
            #print("nonzero", nonzero)
            premiums = np.multiply(t - g.avg_transaction_price_for_q[q] * g.lots_history[-1][q], nonzero)
            for p in range(g.num_players):
                unrealized_pnls[q, p] += sum(premiums[:, p]) - sum(premiums[p, :])

    def testGame3(self):
        # True values of: 10, 50, 100, 3 Players, 5 Rounds
        g = Game([10, 20, 50], num_players=6, num_rounds=5)

        # Names of A, B, and C
        g.player_setup(["A", "B", "C", "D", "E", "F"])

        g.players[0].assign_bids_and_asks([16, 9, 14, 12], [16, 10, 12, 15], [11, 87, 97, 11])
        g.players[1].assign_bids_and_asks([8, 3, 5, 17], [19, 29, 39, 5], [14, 104, 109, 8])
        g.players[2].assign_bids_and_asks([14, 2, 4, 20], [17, 17, 27, 11], [5, 86, 91, 15])
        g.players[3].assign_bids_and_asks([6, 8, 10, 16], [10, 11, 16, 10], [9, 83, 93, 11])
        g.players[4].assign_bids_and_asks([11, 12, 22, 19], [5, 13, 18, 13], [15, 93, 95, 12])
        g.players[5].assign_bids_and_asks([9, 14, 24, 11], [19, 11, 16, 19], [6, 91, 93, 10])

        g.play_round()

        net_lots = np.zeros((3, g.num_players))  # 3 is num questions
        realized_gains = np.zeros((3, g.num_players))

        for transaction_lots in g.lots_history:
            for q in range(3):
                for p in range(g.num_players):
                    net_lots[q, p] += sum(transaction_lots[q][p, :]) - sum(transaction_lots[q][:, p])
        for i, transaction_matrices in enumerate(g.transactions_history):
            for q in range(3):
                nonzero = (np.array(transaction_matrices[q]) > 0).astype(int)
                print("nonzero")
                print(nonzero)
                t = np.array(transaction_matrices[q])
                print("t", t)
                premiums = np.multiply(t - g.true_values[q] * g.lots_history[i][q], nonzero)
                print("premiums", premiums)
                for p in range(g.num_players):
                    realized_gains[q, p] += sum(premiums[:, p]) - sum(premiums[p, :])
        print(realized_gains.T)

        print(g.calculate_realized_pnls_and_lots()[0].T)




if __name__ == "__main__":
    unittest.main()
