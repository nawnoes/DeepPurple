import Montecarlo as Monte


class ChessAI :
    def __init__(self):
        self.monte = Monte.Monte()
        self.decision = None

    def ask(self, Board):
        turn = Board.turn
        self.monte.set_state(Board)
        self.analyze()
        return self.decision

    def analyze(self):
        self.decision = self.monte.predict()

