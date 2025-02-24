import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import comb, factorial
from collections import Counter

from player import roll


def one_or_five_prob(dice: int):
    """
    Returns the probability of rolling a single number when rolling
    a specific amount of dice. Used for probability of rolling a one or a five.
    """
    return 1 - (5/6)**dice

def x_of_a_kind(x: int, dice: int):
    """
    Returns the probability of rolling 3, 4, 5, or 6 of a kind where
    x is the number of a kind and dice is the amount of dice being rolled.
    """
    if x not in {3, 4, 5, 6}:
        raise ValueError("x must be 3, 4, 5, or 6")
    if dice not in {1, 2, 3, 4, 5, 6}:
        raise ValueError("Can only roll 1, 2, 3, 4, 5, or 6 dice")
    if x > dice:
        return 0
    
    total_outcomes = 6**dice

    # Special case 1: Three of a kind has to avoid being two three of a kinds
    if x == 3 and dice == 6:
        combinations = comb(dice, x)
        favourable_outcomes = 6 * combinations * 5**2 * 4

    # Special case 2: Four of a kind has to avoid being with a pair
    elif x == 4 and dice == 6:
        combinations = comb(dice, x)
        favourable_outcomes = 6 * combinations * 5 * 4

    # Standard cases
    else:
        combinations = comb(dice, x)
        remaining_dice = dice - x
        favourable_outcomes = 6 * combinations * 5**remaining_dice

    return favourable_outcomes / total_outcomes

# Special rolls
def two_triples_prob(dice: int):
    if dice not in {1, 2, 3, 4, 5, 6}:
        raise ValueError("Can only roll 1, 2, 3, 4, 5, or 6 dice")

    if dice < 6:
        return 0
    else:
        total_outcomes = 6**6
        arrangements = comb(6, 2)
        dice_combinations = comb(6, 3)
        favourable_outcomes = arrangements * dice_combinations
        return favourable_outcomes / total_outcomes

def straight_prob(dice: int):
    if dice not in {1, 2, 3, 4, 5, 6}:
        raise ValueError("Can only roll 1, 2, 3, 4, 5, or 6 dice")
     
    if dice < 6:
        return 0
    else:
        total_outcomes = 6**6
        favourable_outcomes = factorial(6)
        return favourable_outcomes / total_outcomes

def three_doubles(dice: int):
    if dice not in {1, 2, 3, 4, 5, 6}:
        raise ValueError("Can only roll 1, 2, 3, 4, 5, or 6 dice")
     
    if dice < 6:
        return 0
    else:
        total_outcomes = 6**6
        arrangements = comb(6, 3)
        dice_combinations = factorial(6) / (factorial(2) * factorial(2) * factorial(2))
        favourable_outcomes = arrangements * dice_combinations
        return favourable_outcomes / total_outcomes
    
def four_of_a_kind_with_pair(dice: int):
    if dice not in {1, 2, 3, 4, 5, 6}:
        raise ValueError("Can only roll 1, 2, 3, 4, 5, or 6 dice")
     
    if dice < 6:
        return 0
    else:
        total_outcomes = 6**6
        arrangements = comb(6, 4)
        two_number_options = 6 * 5
        favourable_outcomes = arrangements * two_number_options
        return favourable_outcomes / total_outcomes

def theoretical_prob_grid():
    """
    Creates a probability grid to visualize the probabilities of 
    each roll depending on how many dice are being rolled.
    """
    dice_amounts = range(6, 0, -1)
    at_least_a_one = [one_or_five_prob(dice) for dice in dice_amounts]
    at_least_a_five = at_least_a_one
    three_of_a_kind = [x_of_a_kind(3, dice) for dice in dice_amounts]
    four_of_a_kind = [x_of_a_kind(4, dice) for dice in dice_amounts]
    five_of_a_kind = [x_of_a_kind(5, dice) for dice in dice_amounts]
    six_of_a_kind = [x_of_a_kind(6, dice) for dice in dice_amounts]
    four_with_pair = [four_of_a_kind_with_pair(dice) for dice in dice_amounts]
    three_pairs = [three_doubles(dice) for dice in dice_amounts]
    straight = [straight_prob(dice) for dice in dice_amounts]
    two_triples = [two_triples_prob(dice) for dice in dice_amounts]

    data = np.array([two_triples, straight, three_pairs, four_with_pair, six_of_a_kind,
                     five_of_a_kind, four_of_a_kind, three_of_a_kind, at_least_a_one, at_least_a_five])

    plt.figure(figsize=(5, 6)) 

    sns.heatmap(data, annot=True, cmap="viridis", linewidths=0.5, fmt=".2%",
            xticklabels=range(6, 0, -1), yticklabels=["Two Triples", "Straight", "Three Pairs", "Four of a Kind with a Pair", "Six of a Kind",
                                                      "Five of a Kind", "Four of a Kind", "Three of a Kind", "At least a 1", "At least a 5"])
   
    plt.xlabel("Number of Dice Rolled")
    plt.ylabel("Type of Roll")
    plt.title("Theoretical Farkle Roll Probabilities")
    plt.show(block=True)

# Simulations for finding estimates of actual probabilities and for finding points vs. no points probabilities
def categorize_roll(roll: list):
    """
    Very similar to the score_roll function in player.py.
    Returns a list of type of roll and a bool of if there were points scored -> ([str], bool)
    Roll types are: one, five, triple, four_of_a_kind, five_of_a_kind, 
    six_of_a_kind, four_with_pair, three_pairs, straight, and two_triples.
    There can be multiple roll types together i.e. four 2s and a 1 is four
    of a kind and a one, so the rolls types are returned as a list.
    """
    counts = Counter(roll)  # Counts of each die in the roll
    unique_dice = set(roll)  # Number of unique values in the roll
    values = sorted(counts.values())  # Sorted counts

    # Special Cases
    if values == [3, 3]: # Two triples
        return ["two_triples"], True
    elif unique_dice == {1, 2, 3, 4, 5, 6}: # 1-6 Straight 
        return ["straight"], True
    elif values == [2, 2, 2]: # Three pairs
        return ["three_pairs"], True 
    elif values == [2, 4]: # Four of a kind + a pair
        return ["four_with_pair"], True  
    
    roll_type = []

    # Six, five, or four of a kind
    for num, count in counts.items():
        if count == 6:
            return ["six_of_a_kind"], True
        elif count == 5:
            roll_type.append("five_of_a_kind")
            counts[num] -= 5
        elif count == 4:
            roll_type.append("four_of_a_kind")
            counts[num] -= 4

    # Three of a kind
    for num, count in list(counts.items()):
        if "triple" not in roll_type and count >= 3:
            roll_type.append("triple")
            counts[num] -= 3

    # Individual 1s and 5s
    if counts[1] != 0:
        roll_type.append("one")
    if counts[5] != 0:
        roll_type.append("five")
 
    points_scored = bool(roll_type)
    return roll_type, points_scored

def roll_sims(sims: int, dice: int):
    """
    Simulates rolls.
    Returns two dictionaries:
    1. The counts of how many times each roll type occured.
    2. The counts of how many rolls occured where points were scored.
    """
    roll_counter = {"one": 0, "five": 0, "triple": 0, "four_of_a_kind": 0, "five_of_a_kind": 0, 
                    "six_of_a_kind": 0, "four_with_pair": 0, "three_pairs": 0, "straight": 0, "two_triples": 0}
    points_occured = {"rolls_with_points": 0, "total_rolls": sims}

    for _ in range(sims):
        rolled_dice = roll(dice)
        roll_types, points_scored = categorize_roll(rolled_dice)

        for roll_type in roll_types:
            roll_counter[roll_type] += 1

        if points_scored:
            points_occured["rolls_with_points"] += 1
    
    return roll_counter, points_occured
    
def simulated_prob_grid():
    """
    Creates a probability grid to visualize the probabilities of 
    each roll depending on how many dice are being rolled.
    But uses the simulated rolls.
    """
    dice_amounts = range(6, 0, -1)
    one = []
    five = []
    triple = []
    four_of_a_kind = []
    five_of_a_kind = []
    six_of_a_kind = []
    four_with_pair = []
    three_pairs = []
    straight = []
    two_triples = []

    list_mapping = {
        "one": one,
        "five": five,
        "triple": triple,
        "four_of_a_kind": four_of_a_kind,
        "five_of_a_kind": five_of_a_kind,
        "six_of_a_kind": six_of_a_kind,
        "four_with_pair": four_with_pair,
        "three_pairs": three_pairs,
        "straight": straight,
        "two_triples": two_triples,
    }

    rolls = 1_000_000
    for dice in dice_amounts:
        roll_counter, _ = roll_sims(rolls, dice)
        for key, value in roll_counter.items():
            list_mapping[key].append(value)
    
    data = np.array([two_triples, straight, three_pairs, four_with_pair, six_of_a_kind,
                     five_of_a_kind, four_of_a_kind, triple, one, five])
    data = data / rolls

    plt.figure(figsize=(5, 6)) 

    sns.heatmap(data, annot=True, cmap="viridis", linewidths=0.5, fmt=".2%",
            xticklabels=range(6, 0, -1), yticklabels=["Two Triples", "Straight", "Three Pairs", "Four of a Kind with a Pair", "Six of a Kind",
                                                      "Five of a Kind", "Four of a Kind", "Three of a Kind", "At least a 1", "At least a 5"])
   
    plt.xlabel("Number of Dice Rolled")
    plt.ylabel("Type of Roll")
    plt.title("Simulated Farkle Roll Probabilities")
    plt.show(block=False)
