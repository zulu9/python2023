# FRPS+ (Flexible Rock Paper Scissors)
# Game / Module
# Release 1.0.1

# Import libraries
import random
import time

# Import classes and functions
from frps_classes import *
import frps_functions as frps_f

# --Main--
if __name__ == '__main__':
    """
    Example implementation with two Games.

    Rulesets are read from the YAML files into a dict. Here are some examples of the resulting structure
    See frps_functions.py or files in ./res/ for examples of the YAML

    ruleset_classic = {
        "Rock": {"Scissors": "crushes"},
        "Paper": {"Rock": "covers"},
        "Scissors": {"Paper": "cut"}
    }
    ruleset_rpsls = {
        "Rock": {"Scissors": "crushes", "Lizard": "crushes"},
        "Paper": {"Rock": "covers", "Spock": "disproves"},
        "Scissors": {"Paper": "cut", "Lizard": "decapitates"},
        "Lizard": {"Paper": "eats", "Spock": "poisons"},
        "Spock": {"Scissors": "smashes", "Rock": "vaporizes"}
    }
    """

    # Select Game ruleset
    my_ruleset = None
    while True:
        try:
            my_gamechoice = int(input(f"Which Game do you want to play?\n"
                                      f"[1] Classic Rock, Paper, Scissors\n"
                                      f"[2] Rock, Paper, Scissors, Lizard, Spock\n"
                                      f"Input: "))
            if my_gamechoice > 2:
                print("Please enter the number of the Game you want to play.")
                continue
        except ValueError:
            print("Please enter the number of the Game you want to play.")
            continue
        else:
            if my_gamechoice == 1:
                my_ruleset = frps_f.load_ruleset_from_file("./res/rps.yaml")
                break
            elif my_gamechoice == 2:
                my_ruleset = frps_f.load_ruleset_from_file("./res/rpsls.yaml")
                break

    # Set target score (Number of matches the player needs to win the Game)
    my_score_target = 0
    while not int(my_score_target) > 0:
        try:
            my_score_target = int(input(f"How man victories are needed to win the game?\n"
                                  f"Input: "))
        except ValueError:
            print("Invalid Number of victories. Please try again. ")
            my_score_target = 0

    # Create instance of Game
    my_game = Game(ruleset=my_ruleset, rounds=1, target_score=my_score_target)

    # Set the start time of the game to now
    my_game.start_time = time.time()
    # While we have not reached the target score ask for action
    while my_game.target_score > 0:
        print(f"\nRound number: {my_game.rounds}")

        # Get and validate player choice.  Create instance of Choice class to save it.
        my_player_input = None
        attack_options = ', '.join(f"[{key}]" for key in my_game.ruleset.keys())  # Format choices for display
        # my_player_input = random.choice(list(my_game.ruleset.keys()))  # Random Player Choice (DEBUG)
        # my_player_input = "Rock"  # Static Player Choice (DEBUG)
        while my_player_input not in my_game.ruleset.keys():  # ruleset.keys contains valid choices
            my_player_input = input(f"Choose attack: {attack_options}: ")
        my_player_turn = Choice(my_game, choice=my_player_input)

        # Create computer Choice (random from keys in the ruleset dict)
        my_ai_turn = Choice(my_game, choice=random.choice(list(my_game.ruleset.keys())))
        # my_ai_turn = Choice(my_game, choice="Scissors")  # Static AI Choice (For DEBUG)

        print("Player chooses: ", my_player_turn.choice)
        print("Computer chooses: ", my_ai_turn.choice)

        # Basic logic
        if my_player_turn > my_ai_turn:  # Player wins
            verb = my_game.ruleset[my_player_turn.choice][my_ai_turn.choice]  # Get verb from the ruleset
            my_game.target_score -= 1
            print(f"\t{my_player_turn.choice} {verb} {my_ai_turn.choice}")
            print("\tYou won this round!")
        elif my_player_turn == my_ai_turn:  # Player and Computer picked the same = Tie
            print("\tIt's a tie!")
        else:  # When in doubt, computer always wins
            verb = my_game.ruleset[my_ai_turn.choice][my_player_turn.choice]  # Get verb from the ruleset
            print(f"\t{my_ai_turn.choice} {verb} {my_player_turn.choice}")
            print("\tYou lost this round.")
        print(f"Points left to win the game: {my_game.target_score}")

        if my_game.target_score == 0:  # We won
            print(f"Gametime: {round(time.time()-my_game.start_time)}s")
            print("\n***YOU ARE WINNER***")
        else:
            my_game.rounds += 1  # Play another round
