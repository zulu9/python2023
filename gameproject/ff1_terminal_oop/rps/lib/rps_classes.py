import time


class Game:
    def __init__(self, ruleset: dict, rounds: int = 1):
        """

        :param ruleset: Dict of possible choices and list of winning condition
        :param rounds: Number of rounds to play
        """
        self.starttime = time.time()  # Get current time
        self.rounds = rounds
        self.ruleset = ruleset


class Choice:
    def __init__(self, game: Game, choice: str):
        self.game = game
        self.choice = choice

    def __gt__(self, other):
       # print(self.game.ruleset[self.choice])
        other_looses = self.game.ruleset[self.choice].keys()
        if other.choice in other_looses:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.choice == other.choice:
            return True
        else:
            return False
