import pandas as pd

def get_roll_evs(roll_probabilities: pd.DataFrame):
    """Calculates the expected value of each roll based on number of dice."""
    roll_score_dict = {"Two Triples": 2500,
        "Straight": 1500,
        "Three Pairs": 1500,
        "Four of a Kind with a Pair": 1500,
        "Six of a Kind": 3000,
        "Five of a Kind": 2000,
        "Four of a Kind": 1000,
        "Three of a Kind": 500, # Average of three of a kind scoring (1000 + 200 + 300 + 400 + 500 + 600) / 6
        "At least a 1": 100,
        "At least a 5": 50
        }
    
    roll_evs = pd.DataFrame(columns=roll_probabilities.columns, index=["Expected Roll Value"])
    for dice in roll_probabilities.columns:
        ev = 0
        for roll_type in roll_probabilities.index:
            probability = roll_probabilities.loc[roll_type, dice]
            score = roll_score_dict.get(roll_type, 0)
            ev += score * probability
        roll_evs[dice] = ev

    return roll_evs