import unittest
from order_book import OrderBook
import numpy as np


class TestGameB(unittest.TestCase):

    def testOrderBook1(self):
        """
        Everyone has 1 lots
        """
        # BID - Player 0: 10 x 1, Player 1: 20 x 1, Player 2: 30 x 1
        bid = OrderBook(1, "BID", {0: (10, 1), 1: (20, 1), 2: (30, 1)})

        # ASK - Player 0: 15 x 1, Player 1: 25 x 1, Player 2: 35 x 1
        ask = OrderBook(1, "ASK", {0: (15, 1), 1: (25, 1), 2: (35, 1)})

        # Match BID and ASK
        # Player 0 sells to Player 2 at (15+30)/2 = 22.5 for 1 lot
        price, lots = OrderBook.match(bid.book, ask.book, 3, 1)

        true_price = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [22.5, 0, 0]])

        true_lots = np.array([[0, 0, 0],
                              [0, 0, 0],
                              [1, 0, 0]])

        self.assertIsNone(np.testing.assert_array_almost_equal(price, true_price))
        self.assertIsNone(np.testing.assert_array_almost_equal(lots, true_lots))

    def testOrderBook2(self):
        """
        Player 0's two lots get matched to Player 1 and 2 each
        """
        # BID - Player 0: 10 x 1, Player 1: 20 x 1, Player 2: 30 x 1
        bid = OrderBook(1, "BID", {0: (10, 1), 1: (20, 1), 2: (30, 1)})

        # ASK - Player 0: 15 x 2, Player 1: 25 x 1, Player 2: 35 x 1
        ask = OrderBook(1, "ASK", {0: (15, 2), 1: (25, 1), 2: (35, 1)})

        # Match BID and ASK
        # Player 0 sells to Player 2 at (15+30)/2 = 22.5 for 1 lot
        # Player 0 sells to Player 1 at (15+20)/2 =17.5 for 1 lot
        price, lots = OrderBook.match(bid.book, ask.book, 3, 1)

        true_price = np.array([[0, 0, 0],
                               [17.5, 0, 0],
                               [22.5, 0, 0]])

        true_lots = np.array([[0, 0, 0],
                              [1, 0, 0],
                              [1, 0, 0]])

        self.assertIsNone(np.testing.assert_array_almost_equal(price, true_price))
        self.assertIsNone(np.testing.assert_array_almost_equal(lots, true_lots))

    def testOrderBook3(self):
        """
        Player 2's two lots get matched to Player 0 and 1 each
        """
        # BID - Player 0: 10 x 1, Player 1: 20 x 1, Player 2: 30 x 2
        bid = OrderBook(1, "BID", {0: (10, 1), 1: (20, 1), 2: (30, 2)})

        # ASK - Player 0: 15 x 1, Player 1: 25 x 1, Player 2: 35 x 1
        ask = OrderBook(1, "ASK", {0: (15, 1), 1: (25, 1), 2: (35, 1)})

        # Match BID and ASK
        # Player 0 sells to Player 2 at (15+30)/2 = 22.5 for 1 lot
        # Player 1 sells to Player 2 at (25+30)/2 = 27.5 for 1 lot
        price, lots = OrderBook.match(bid.book, ask.book, 3, 1)

        true_price = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [22.5, 27.5, 0]])

        true_lots = np.array([[0, 0, 0],
                              [0, 0, 0],
                              [1, 1, 0]])

        self.assertIsNone(np.testing.assert_array_almost_equal(price, true_price))
        self.assertIsNone(np.testing.assert_array_almost_equal(lots, true_lots))

    def testOrderBook4(self):
        """
        Player 2's two lots get matched to Player 0's
        """
        # BID - Player 0: 10 x 1, Player 1: 20 x 1, Player 2: 30 x 2
        bid = OrderBook(1, "BID", {0: (10, 1), 1: (20, 1), 2: (30, 2)})

        # ASK - Player 0: 15 x 2, Player 1: 25 x 1, Player 2: 35 x 1
        ask = OrderBook(1, "ASK", {0: (15, 2), 1: (25, 1), 2: (35, 1)})

        # Match BID and ASK
        # Player 0 sells to Player 2 at (15+30)/2 = 22.5 for 2 lots
        price, lots = OrderBook.match(bid.book, ask.book, 3, 1)

        true_price = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [45, 0, 0]])

        true_lots = np.array([[0, 0, 0],
                              [0, 0, 0],
                              [2, 0, 0]])

        self.assertIsNone(np.testing.assert_array_almost_equal(price, true_price))
        self.assertIsNone(np.testing.assert_array_almost_equal(lots, true_lots))
if __name__ == "__main__":
    unittest.main()
