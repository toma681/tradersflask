class Player:
    def __init__(self, name):
        self.name = name
        self.running_pnl = 0
        self.q1_bids, self.q1_asks = [], []
        self.q2_bids, self.q2_asks = [], []
        self.q3_bids, self.q3_asks = [], []

    def assign_bids_and_asks(self, q1_market, q2_market, q3_market):
        """
        Fills in the player's bids and asks for each question.
        A market for a question is a 4 item tuple:
        First item is # lots for bid
        Second item is bid
        Third item is ask
        Fourth item is # lots for ask
        # TODO: return false if # lots not valid
        Returns: True 
        """
        self.q1_bids.append((q1_market[1], q1_market[0]))
        self.q1_asks.append((q1_market[2], q1_market[3]))
        self.q2_bids.append((q2_market[1], q2_market[0]))
        self.q2_asks.append((q2_market[2], q2_market[3]))
        self.q3_bids.append((q3_market[1], q3_market[0]))
        self.q3_asks.append((q3_market[2], q3_market[3]))
        return "SPREAD SUCCESS"
