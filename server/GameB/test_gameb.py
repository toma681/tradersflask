from .player import Player
import unittest
from .game import Game


class TestGameB(unittest.TestCase):

    def test1(self):
        # Create game
        g = Game(num_players=2, min_spread=2, max_spread=5, card_range_low=1, card_range_high=10)

        # Player 0 makes market
        self.assertTrue(g.make_market(g.players[0], 5, 1, 8, 1), "SPREAD SUCCESS")

        # Player 1 buys from Player 0
        self.assertTrue(g.transact(g.players[1], "BUY", 1), "TRANSACTION SUCCESS")

        # Player 1 makes new market
        self.assertTrue(g.make_market(g.players[1], 5, 1, 8, 1), "SPREAD SUCCESS")

        # Player 0 makes a narrower market
        self.assertTrue(g.make_market(g.players[0], 6, 1, 8, 1), "SPREAD SUCCESS")

        # Player 1 attempts to make a narrower market, but at the minimum spread
        with self.assertRaisesRegexp(Exception, 'Must transact.  We are at the minimum spread.'):
            # 'Must transact.  We are at the minimum spread.'
            g.make_market(g.players[1], 7, 1, 8, 1)

        # Player 1 buys from Player 0
        self.assertTrue(g.transact(g.players[1], "BUY", 1), "TRANSACTION SUCCESS")

        # Player 1 now has 2 long positions
        self.assertEqual(g.players[1].get_position(), 2)

        # Player 0 now has 2 short positions
        self.assertEqual(g.players[0].get_position(), -2)

        # Display all positions
        self.assertEqual(g.get_all_players_position(), {0: -2, 1: 2})

    def test2(self):
        # Create game
        g = Game(num_players=3, min_spread=2, max_spread=20, card_range_low=1, card_range_high=20)

        # Player 0 makes market
        self.assertTrue(g.make_market(g.players[0], 20, 2, 40, 2), "SPREAD SUCCESS")

        # Player 1 makes new market
        self.assertTrue(g.make_market(g.players[1], 29, 3, 33, 4), "SPREAD SUCCESS")

        # Player 2 attempts to buy 5 lots.
        with self.assertRaisesRegexp(Exception, '4 total available lots. Enter a value less than or equal to that.'):
            g.transact(g.players[2], "BUY", 5)

        # Player 2 buys 3 lots.
        self.assertTrue(g.transact(g.players[2], "BUY", 3), "TRANSACTION SUCCESS")

        # Player 2 is now long 3.
        self.assertEqual(g.players[2].get_position(), 3)

        # Player 1 is now short 3.
        self.assertEqual(g.players[1].get_position(), -3)

        # Player 2 makes a new market.
        self.assertTrue(g.make_market(g.players[2], 28, 2, 35, 1), "SPREAD SUCCESS")

        # Check that the next person in order is not player 2.
        self.assertNotEqual(g.round_order[0], 2)

        # New shuffled round player makes a narrower market
        self.assertTrue(g.make_market(g.players[g.round_order[0]], 28, 2, 34, 1), "SPREAD SUCCESS")

    def test3(self):
        # Create game
        g = Game(num_players=3, min_spread=2, max_spread=20, card_range_low=1, card_range_high=20)

        # First player stalls the game
        g.stall(g.players[0])

        # Bid should be (20+1)*3/2 = 31, 31 - 20/2 = 21
        self.assertEqual(g.get_current_market()[0], 21)

        # Bid size should be between 2 and 20
        self.assertTrue(2 <= g.get_current_market()[1] <= 20)

        # Ask should be (20+1)*3/2 = 31, 31 + 20/2 = 41
        self.assertEqual(g.get_current_market()[2], 41)

        # Ask size should be between 2 and 20
        self.assertTrue(2 <= g.get_current_market()[3] <= 20)

    def test4(self):
        # Create game
        g = Game(num_players=3, min_spread=2, max_spread=20, card_range_low=1, card_range_high=20)

        # Player 0 makes market
        self.assertTrue(g.make_market(g.players[0], 22, 2, 24, 2), "SPREAD SUCCESS")

        # Player 1 stalls at minimum spread, so it transacts
        self.assertTrue(g.stall(g.players[1]), "TRANSACTION SUCCESS")

        # Player 1 buys at 22 or sells at 20
        self.assertTrue((g.trade_log[1]['action'] == 'BUY' and g.trade_log[1]['price'] == 24) or (g.trade_log[1]['action'] == 'SELL' and g.trade_log[1]['price'] == 22))

        # Player 1 trade quantity is 2
        self.assertTrue(g.trade_log[1]['quantity'] == 2)

        # Player 1 stalls at making a market
        self.assertTrue(g.stall(g.players[1]), "SPREAD SUCCESS")

        # Bid should be (20+1)*3/2 = 31, 31 - 20/2 = 21
        self.assertEqual(g.get_current_market()[0], 21)

        # Bid size should be between 2 and 20
        self.assertTrue(2 <= g.get_current_market()[1] <= 20)

        # Ask should be (20+1)*3/2 = 31, 31 + 20/2 = 41
        self.assertEqual(g.get_current_market()[2], 41)

        # Ask size should be between 2 and 20
        self.assertTrue(2 <= g.get_current_market()[3] <= 20)

    def test5(self):
        # Create game
        g = Game(num_players=3, min_spread=2, max_spread=20, card_range_low=1, card_range_high=20)

        # Player 0 makes market
        self.assertTrue(g.make_market(g.players[0], 21, 2, 24, 2), "SPREAD SUCCESS")

        # Player 1 stalls at minimum spread, so it makes a new market
        self.assertTrue(g.stall(g.players[1]), "SPREAD SUCCESS")

        # 21 and 23 or 22 and 24
        self.assertTrue((g.get_current_market()[0] == 21 and g.get_current_market()[2] == 23) or (g.get_current_market()[0] == 22 and g.get_current_market()[2] == 24))

        # Bid size should be between 2 and 20
        self.assertTrue(2 <= g.get_current_market()[1] <= 20)

        # Ask size should be between 2 and 20
        self.assertTrue(2 <= g.get_current_market()[3] <= 20)

    def test6(self):
        """
        Player 1 gets dropped from a 3 player game.
        """
        # Create game
        g = Game(num_players=3, min_spread=2, max_spread=20, card_range_low=1, card_range_high=20)

        # Player 0 makes market
        self.assertTrue(g.make_market(g.players[0], 21, 2, 24, 2), "SPREAD SUCCESS")

        g.drop(g.players[1])

        # Player should be 2 now
        self.assertEqual(g.num_players, 2)

        # Current player should be 2 now
        self.assertEqual(g.get_current_player(), 2)

        # Player 2 makes new market
        self.assertTrue(g.make_market(g.players[2], 22, 2, 24, 2), "SPREAD SUCCESS")

    def test7(self):
        """
        Undo making a market
        """
        # Create game
        g = Game(num_players=3, min_spread=2, max_spread=20, card_range_low=1, card_range_high=20)

        # Player 0 makes market
        self.assertTrue(g.make_market(g.players[0], 21, 2, 24, 2), "SPREAD SUCCESS")

        self.assertTrue(g.transact(g.players[1], "BUY", 2))

        g = g.undo()

        # Current player should be 1 now
        self.assertEqual(g.get_current_player(), 1)

    def test8(self):
        # Create game
        g = Game(num_players=5, min_spread=5, max_spread=50, card_range_low=1, card_range_high=50)

        g.stall(g.players[0])

        g.drop(g.players[1])

        g.stall(g.players[2])

        g.drop(g.players[3])

        g.stall(g.players[4])

        g.drop(g.players[g.get_current_player()])

        print(g.get_players_cards())
        print(g.get_current_player())
        print(g.players)
        print(g.all_players)
        print(g.round_order)
        print(g.turn)


if __name__ == "__main__":
    unittest.main()
