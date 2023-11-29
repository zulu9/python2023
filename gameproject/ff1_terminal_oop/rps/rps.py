# Flexible RPS (Rock, Paper, Scissors) Game

# Imports
import random

from lib.rps_classes import *

# --Functions--


# --Main--
my_ruleset_classic = {
    "Rock": ["Scissors"],
    "Paper": ["Rock"],
    "Scissors": ["Paper"]
}
my_ruleset_rpsls = {
    "Rock": ["Paper", "Lizard"],
    "Paper": ["Rock", "Spock"],
    "Scissors": ["Paper", "Lizard"],
    "Lizard": ["Paper", "Spock"],
    "Spock": ["Scissors", "Rock"]
}

my_game = Game(ruleset=my_ruleset_rpsls, rounds=5)

while my_game.rounds > 0:
    my_player_input = None
    while my_player_input not in my_game.ruleset.keys():
        my_player_input = input(f"Choose: {my_game.ruleset.keys()}: ")
    my_player_choice = Choice(my_game, choice=my_player_input)
    my_ai_choice = Choice(my_game, choice=random.choice(list(my_game.ruleset.keys())))

    print("Player chooses: ", my_player_choice.choice)
    print("Computer chooses: ", my_ai_choice.choice)

    if my_player_choice > my_ai_choice:
        print("Player wins!")
    elif my_player_choice == my_ai_choice:
        print("Tie!")
    else:
        print("Player Looses")
    my_game.rounds -= 1
