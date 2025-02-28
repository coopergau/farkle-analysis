import pandas as pd
from player import Player, roll, score_roll
from game import Game
from roll_probabilities import calculate_roll_probabilities, save_prob_dfs, roll_type_prob_grid, points_scoring_prob_grid, categorize_roll
from expected_roll_value import theoretic_roll_evs, empirical_roll_evs
from strategy_comparison import basic_game, complex_1v1, visualize_winners

ROLL_SIMS = 1_000_000
GAMES = 20_000

def main():

    #roll_type_prob_df, points_scoring_prob_df = calculate_roll_probabilities()
    #save_prob_dfs(roll_type_prob_df, points_scoring_prob_df)
    
    #roll_probs = pd.read_csv("Roll Type Probabilities.csv", index_col=0)
    #scoring_prob = pd.read_csv("Probability of Scoring Points.csv", index_col=0)

    #roll_type_prob_grid(roll_probs)
    #points_scoring_prob_grid(scoring_prob)
    #theoretical_roll_evs = theoretic_roll_evs(roll_probs)
    #print(roll_evs)
    #roll_evs = empirical_roll_evs(ROLL_SIMS)
    #print(roll_evs)

    winners = complex_1v1(GAMES)
    #winners = basic_game(GAMES)
    visualize_winners(winners, GAMES)


if __name__ == "__main__":
    main()