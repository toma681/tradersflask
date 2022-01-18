from collections import OrderedDict
from .lot import Lot
import numpy as np


class OrderBook:
    def __init__(self, question, bid_or_ask_type, players_prices_and_lots):
        """
        Expects players_prices_and_lots to be a dictionary of player:(price, # lots) pairings,
        where player is a zero-indexed int
        """
        self.bid_or_ask_type = bid_or_ask_type
        self.question = question
        self.book = self.construct_book_using_players_dict(players_prices_and_lots)

    def construct_book_using_players_dict(self, players_prices_and_lots):
        """
        Expects players_prices_and_lots to be a dictionary of player:(price, # lots) pairings,
        where player is a zero-indexed int
        Returns a sorted dictionary containing prices:list of lots pairings which is ascending in prices
        """
        lots_list = []
        for player in players_prices_and_lots.keys():
            for _ in range(players_prices_and_lots[player][1]):
                lots_list.append(Lot(player, self.question, self.bid_or_ask_type, players_prices_and_lots[player][0]))

        return self.construct_book_using_list_of_lots(lots_list)

    def construct_book_using_list_of_lots(self, list_of_lots):
        result = OrderedDict()
        list_of_lots.sort(key=lambda x: x.price)
        # add prices as keys and list of lot objects as values to OrderedDict
        for lot in list_of_lots:
            if lot.price not in result:
                result[lot.price] = [lot]
            else:
                result[lot.price].append(lot)

        return result

    @classmethod
    def match(cls, bids_book, asks_book, num_players, question):
        """
        Class method that takes in two OrderBook objects (bids_book and asks_book)
        as well as the number of players playing and current question (zero indexed int).
        Matches lots across the two books and returns two transaction tables, one for 
        total $ amount transacted and other for number of lots transacted.
        """
        bid_lots_list = []
        for price in bids_book.book:
            for lot in bids_book.book[price]:
                bid_lots_list.append(lot)

        ask_lots_list = []
        for price in asks_book.book:
            for lot in asks_book.book[price]:
                ask_lots_list.append(lot)

        transaction_total_prices = np.zeros((num_players, num_players))  # rows are buyers, columns are sellers
        transaction_lots = np.zeros((num_players, num_players))  # rows are buyers, columns are sellers 

        b = len(bid_lots_list) - 1  # loop in descending order of bids
        while b >= 0:
            a = 0
            while a < len(ask_lots_list):  # loop in ascending order of asks
                if ask_lots_list[a].price <= bid_lots_list[b].price and ask_lots_list[a].player != bid_lots_list[
                    b].player:  # make the trade happen
                    transacted_ask = ask_lots_list.pop(a)
                    a -= 1
                    transacted_bid = bid_lots_list.pop(b)
                    transaction_price = (transacted_bid.price + transacted_ask.price) * 0.5
                    transaction_lots[transacted_bid.player, transacted_ask.player] += 1
                    transaction_total_prices[transacted_bid.player, transacted_ask.player] += transaction_price
                    break
                a += 1
            b -= 1
        return transaction_total_prices, transaction_lots
