import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import comb, factorial



def one_or_five_prob(dice: int):
    """
    Returns the probability of rolling a one or a five when rolling
    a specific amount of dice.
    """
    return 1 - (2/3)**dice

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



def prob_grid():
    """
    Creates a probability grid to visualize the probabilities of 
    each roll depending on how many dice are being rolled.
    """
    dice_amounts = range(6, 0, -1)
    one_or_five = [one_or_five_prob(dice) for dice in dice_amounts]
    three_of_a_kind = [x_of_a_kind(3, dice) for dice in dice_amounts]
    four_of_a_kind = [x_of_a_kind(4, dice) for dice in dice_amounts]
    five_of_a_kind = [x_of_a_kind(5, dice) for dice in dice_amounts]
    six_of_a_kind = [x_of_a_kind(6, dice) for dice in dice_amounts]
    four_with_pair = [four_of_a_kind_with_pair(dice) for dice in dice_amounts]
    three_pairs = [three_doubles(dice) for dice in dice_amounts]
    straight = [straight_prob(dice) for dice in dice_amounts]
    two_triples = [two_triples_prob(dice) for dice in dice_amounts]

    data = np.array([two_triples, straight, three_pairs, four_with_pair, six_of_a_kind,
                     five_of_a_kind, four_of_a_kind, three_of_a_kind, one_or_five])

    plt.figure(figsize=(5, 6)) 

    sns.heatmap(data, annot=True, cmap="viridis", linewidths=0.5, fmt=".4%",
            xticklabels=range(6, 0, -1), yticklabels=["Two Triples", "Straight", "Three Pairs", "Four of a Kind with a Pair", "Six of a Kind",
                                                      "Five of a Kind", "Four of a Kind", "Three of a Kind", "At least a 1 or 5"])
   
    plt.xlabel("Number of Dice Rolled")
    plt.ylabel("Type of Roll")
    plt.title("Farkle Roll Probabilities")
    plt.show()