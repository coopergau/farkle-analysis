from player import Player
from game import Game
import matplotlib.pyplot as plt
import pandas as pd

def basic_game(games: int):
    winners_dict = {"One": 0, "Two": 0, "Three": 0, "Four": 0, "Five": 0, "Six": 0}
    for _ in range(games):
        one_dice = Player("One", min_dice=1, bank_threshold=300, strategy="basic")
        two_dice = Player("Two", min_dice=2, bank_threshold=300, strategy="basic")
        three_dice = Player("Three", min_dice=3, bank_threshold=300, strategy="basic")
        four_dice = Player("Four", min_dice=4, bank_threshold=300, strategy="basic")
        five_dice = Player("Five", min_dice=5, bank_threshold=300, strategy="basic")
        six_dice = Player("Six", min_dice=6, bank_threshold=300, strategy="basic")
        game = Game([one_dice, two_dice, three_dice, four_dice, five_dice, six_dice], winner_threshold=10_000)
        game.play_game()
        winner = game.winner
        winners_dict[winner.name] += 1
    print(winners_dict)
    return winners_dict

def complex_1v1(games: int, ev_table: pd.DataFrame, not_farkle_table: pd.DataFrame):
    winners_dict = {"basic": 0, "ev_table": 0}
    for _ in range(games):
        basic_player = Player("basic", min_dice=1, bank_threshold=300, strategy="basic")
        ev_table_player = Player("ev_table", min_dice=2, bank_threshold=300, strategy="ev table", ev_table=ev_table, not_farkle_table=not_farkle_table)
       
        game = Game([basic_player, ev_table_player], winner_threshold=10_000)
        game.play_game()
        winner = game.winner
        winners_dict[winner.name] += 1
    print(winners_dict)
    return winners_dict

def visualize_winners(winners_dict: dict, games: int):
    plt.bar(winners_dict.keys(), winners_dict.values(), color='skyblue', edgecolor='black')
    
    plt.xlabel("Minimum Dice Needed to Keep Rolling")
    plt.ylabel(f"Wins after {games} Games")
    plt.title("Number of Wins Based on Basic Dice Strategy")

    # Show plot
    plt.show()