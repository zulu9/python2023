# Flexible RPS (Rock, Paper, Scissors) Game
import random

# Imports
from lib.rps_classes import *

# --Functions--


# --Main--
my_ruleset_classic = {
    "Rock": {"Scissors": "crushes"},
    "Paper": {"Rock": "covers"},
    "Scissors": {"Paper": "cut"}
}
my_ruleset_rpsls = {
    "Rock": {"Scissors": "crushes", "Lizard": "crushes"},
    "Paper": {"Rock": "covers", "Spock": "disproves"},
    "Scissors": {"Paper": "cut", "Lizard": "decapitates"},
    "Lizard": {"Paper": "eats", "Spock": "poisons"},
    "Spock": {"Scissors": "smashes", "Rock": "vaporizes"}
}

my_rounds = int(input("How man rounds? "))
my_game = Game(ruleset=my_ruleset_rpsls, rounds=my_rounds)

while my_game.rounds > 0:
    my_player_input = random.choice(list(my_game.ruleset.keys()))
    while my_player_input not in my_game.ruleset.keys():
        my_player_input = input(f"Choose: {my_game.ruleset.keys()}: ")
    my_player_choice = Choice(my_game, choice=my_player_input)
    my_ai_choice = Choice(my_game, choice=random.choice(list(my_game.ruleset.keys())))
    my_ai_choice = Choice(my_game, choice="Scissors")

    print("Player chooses: ", my_player_choice.choice)
    print("Computer chooses: ", my_ai_choice.choice)

    if my_player_choice > my_ai_choice:
        verb = my_game.ruleset[my_player_choice.choice][my_ai_choice.choice]
        print(f"{my_player_choice.choice} {verb} {my_ai_choice.choice}")
        print("Player Wins!")
    elif my_player_choice == my_ai_choice:
        print("Tie!")
    else:
        verb = my_game.ruleset[my_ai_choice.choice][my_player_choice.choice]
        print(f"{my_ai_choice.choice} {verb} {my_player_choice.choice}")
        print("Player Looses")
    my_game.rounds -= 1
    print()
