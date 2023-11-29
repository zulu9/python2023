import time


class Game:
    def __init__(self, ruleset: dict, rounds: int = 1):
        self.starttime = time.time()
        self.rounds = rounds
        self.ruleset = ruleset


class Choice:
    def __init__(self, game: Game, choice: str):
        super().__init__()
        self.game = game
        self.choice = choice

    def __gt__(self, other):
        self.victory_conditions = self.game.ruleset

        other_looses = self.victory_conditions[self.choice]
        if other.choice in other_looses:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.choice == other.choice:
            return True
        else:
            return False
