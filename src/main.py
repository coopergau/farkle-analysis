import pandas as pd
from player import Player, roll, score_roll
from game import Game
from roll_probabilities import calculate_roll_probabilities, save_prob_dfs, roll_type_prob_grid, points_scoring_prob_grid, categorize_roll
from expected_roll_value import theoretic_roll_evs, empirical_roll_evs

ROLL_SIMS = 1_000_000
thresholds = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000]
index = 4

def main():

    #roll_type_prob_df, points_scoring_prob_df = calculate_roll_probabilities()
    #save_prob_dfs(roll_type_prob_df, points_scoring_prob_df)
    
    roll_probs = pd.read_csv("Roll Type Probabilities.csv", index_col=0)
    #scoring_prob = pd.read_csv("Probability of Scoring Points.csv", index_col=0)

    #roll_type_prob_grid(roll_probs)
    #points_scoring_prob_grid(scoring_prob)
    roll_evs = theoretic_roll_evs(roll_probs)
    print(roll_evs)
    sim_roll_evs = empirical_roll_evs(1_000_000)
    print(sim_roll_evs)


    """winners_dict = {"One": 0, "Two": 0, "Three": 0, "Four": 0, "Five": 0, "Six": 0}
    for _ in range(SIMS):
        one_dice = Player("One", min_dice=3, bank_threshold=700)
        two_dice = Player("Two", min_dice=3, bank_threshold=400)
        three_dice = Player("Three", min_dice=3, bank_threshold=750)
        four_dice = Player("Four", min_dice=3, bank_threshold=800)
        five_dice = Player("Five", min_dice=3, bank_threshold=1000)
        six_dice = Player("Six", min_dice=3, bank_threshold=1200)
        game = Game([one_dice, two_dice, three_dice, four_dice, five_dice, six_dice], winner_threshold=10_000)
        game.play_game()
        winner = game.winner
        winners_dict[winner.name] += 1
        print(winners_dict)
    """


if __name__ == "__main__":
    main()