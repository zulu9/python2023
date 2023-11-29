# FRPS+ (Flexible Rock Paper Scissors) Game / Module 1.0

# Import libraries
import random

# Import classes
from lib.rps_classes import *

# --Main--
if __name__ == '__main__':
    # TODO Read Rulesets from files
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

    my_rounds = 1
    my_target = 0

    my_ruleset = ruleset_classic
    while True:
        try:
            my_gamechoice = int(input(f"Which Game do you want to play?\n"
                                      f"[1] Classic Rock, Paper Scissors\n"
                                      f"[2] Rock, Paper, Scissors, Lizard, Spock\n"
                                      f"Input: "))
            if my_gamechoice > 2:
                print("Invalid Game Number. Please try again. ")
                continue
        except ValueError:
            print("Invalid Game Number. Please try again. ")
            continue
        else:
            if my_gamechoice == 1:
                my_ruleset = ruleset_classic
                break
            elif my_gamechoice == 2:
                my_ruleset = ruleset_rpsls
                break

    while not int(my_target) > 0:
        try:
            my_target = int(input(f"How man victories are needed to win the game?\n"
                                  f"Input: "))
        except ValueError:
            print("Invalid Number of victories. Please try again. ")
            my_target = -1

    my_game = Game(ruleset=my_ruleset, rounds=my_rounds, target_score=my_target)

    while my_game.target_score > 0:
        print(f"\nRound number: {my_game.rounds}")

        my_player_input = None
        # my_player_input = random.choice(list(my_game.ruleset.keys()))  # Random Player Choice (DEBUG)
        while my_player_input not in my_game.ruleset.keys():       # TODO make all input case insensitive
            attack_options = ', '.join(f"[{key}]" for key in my_game.ruleset.keys())
            my_player_input = input(f"Choose attack: {attack_options}: ")

        my_player_choice = Choice(my_game, choice=my_player_input)
        # my_player_choice = Choice(my_game, choice="Rock")  # Fixed Player Choice (DEBUG)
        my_ai_choice = Choice(my_game, choice=random.choice(list(my_game.ruleset.keys())))
        # my_ai_choice = Choice(my_game, choice="Scissors")  # Fixed AI Choice (DEBUG)

        print("Player chooses: ", my_player_choice.choice)
        print("Computer chooses: ", my_ai_choice.choice)

        # Basic logic
        if my_player_choice > my_ai_choice:
            verb = my_game.ruleset[my_player_choice.choice][my_ai_choice.choice]
            print(f"{my_player_choice.choice} {verb} {my_ai_choice.choice}")
            print("Player Wins!")
            my_game.target_score -= 1
        elif my_player_choice == my_ai_choice:
            print("Tie!")
        else:
            verb = my_game.ruleset[my_ai_choice.choice][my_player_choice.choice]
            print(f"{my_ai_choice.choice} {verb} {my_player_choice.choice}")
            print("Player Looses")
        print(f"Points to win: {my_game.target_score}")

        if my_game.target_score == 0:  # We won
            print("\nMatch gewonnen!")
        else:
            my_game.rounds += 1  # Play another rounds
