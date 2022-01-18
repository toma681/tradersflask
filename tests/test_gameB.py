from unittest import TestCase
from .server.GameB import game


class TestGameB(TestCase):
    def simple_test(self):
        """
        Basic logic test
        """
        g = game.Game()
        self.assertEqual(3, 3)

