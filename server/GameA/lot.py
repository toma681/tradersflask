class Lot:
    def __init__(self, player, question, bid_or_ask_type, price):
        self.player = player  # zero indexed integer
        self.question = question  # zero indexed integer
        self.bid_or_ask_type = bid_or_ask_type  # string "BID" or "ASK"
        self.price = price