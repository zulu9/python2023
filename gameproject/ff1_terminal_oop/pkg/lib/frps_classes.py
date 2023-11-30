# FRPS+ (Flexible Rock Paper Scissors)
# Classes

class Game:
    def __init__(self, ruleset: dict, rounds: int = 1, target_score: int = 1):
        """
        Object defining the general properties of the game.

        :param ruleset: Dict of possible choices containing a dict
            of winning conditions and corresponding verbs
        :param rounds: Number of rounds to play
        :param target_score: Number of victories to win game
        """
        self.start_time = None  # Placeholder so Games can handle the starttime within the Game class
        self.rounds = rounds
        self.target_score = target_score
        self.ruleset = ruleset


class Choice:
    def __init__(self, game: Game, choice: str):
        """
        Compares the Player's (P1) and AI (P2) choices to determine the winner.

        :param game: The current game object
        :param choice: The Player's (P1) or AI  (P2) choice to compare
        """
        self.game = game
        self.choice = choice

    # Define equal and greater than methods to compare choices
    def __eq__(self, other):
        """
        Checks if P1 and P2 chose the same
        :param other: instance of Choice for P2
        :return: True if P1 and P2 picked the same. False if not.
        """
        if self.choice == other.choice:
            return True
        else:
            return False

    def __gt__(self, other):
        """
        Check if action
        :param other: instance of Choice for P2
        :return: True if P1 has won, false if P1 has lost or chose same as P2
        """
        other_looses = self.game.ruleset[self.choice].keys()  # List of conditions where P2 looses
        if other.choice in other_looses:
            return True
        else:
            return False
