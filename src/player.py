import random
import pandas as pd
from collections import Counter

def roll(dice: int):
    if dice > 6 or dice < 1:
        raise ValueError("Number of dice must be between 1 and 6.")
    return [random.randint(1, 6) for die in range(dice)]

def score_roll(roll: list):
    """
    Returns the score associated with a given role and the dice left over: (score, leftover_dice)
    """
    counts = Counter(roll)  # Counts of each die in the roll
    unique_dice = set(roll)  # Number of unique values in the roll
    values = sorted(counts.values())  # Sorted counts
    points = 0

    # Special Cases
    if values == [3, 3]: # Two triples
        return 2500, 0 
    elif unique_dice == {1, 2, 3, 4, 5, 6}: # 1-6 Straight 
        return 1500, 0  
    elif values == [2, 2, 2]: # Three pairs
        return 1500, 0  
    elif values == [2, 4]: # Four of a kind + a pair
        return 1500, 0  
    
    leftover_dice = len(roll)

    # Six, five, or four of a kind
    for num, count in counts.items():
        if count == 6:
            return 3000, 0
        elif count == 5:
            points += 2000
            counts[num] -= 5
            leftover_dice -= 5
        elif count == 4:
            points += 1000
            counts[num] -= 4
            leftover_dice -= 4

    # Three of a kind
    triple_scores = {1: 1000, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}
    for num, count in list(counts.items()):
        if count >= 3:
            points += triple_scores[num]
            counts[num] -= 3
            leftover_dice -= 3

    # Individual 1s and 5s
    points += counts[1] * 100
    points += counts[5] * 50
    leftover_dice -= counts[1]
    leftover_dice -= counts[5]

    return points, leftover_dice

class Player:
    def __init__(self, name: str, min_dice: int, bank_threshold: int, strategy: str, ev_table: pd.DataFrame=None, not_farkle_table: pd.DataFrame=None):
        """
        Player strategy variables:
        min_dice: Minimum amount of dice they will roll, bank points otherwise.
        bank_threshold: Amount of points they will bank after reaching in that turn.
        strategy: Dictates how player choose to roll or bank points.
        """
        self.name = name
        self.min_dice = min_dice
        self.bank_threshold = bank_threshold
        self.strategy = strategy
        self.ev_table = ev_table
        self.not_farkle_table = not_farkle_table
        self.score = 0
        self.turn_score = 0

    def __str__(self):
        return f"Player: {self.name} | Score: {self.score} | Turn Score: {self.turn_score}"
    
    def update_turn_score(self, score):
        if score == 0:
            self.turn_score = 0
        else:
            self.turn_score += score

    def update_score_and_end_turn(self):
        if self.turn_score != 0:
            self.score += self.turn_score
            self.turn_score = 0
    
    def basic_turn(self):
        dice = 6
        turn_over = False
        while not turn_over:
            rolled_dice = roll(dice)
            points, dice = score_roll(rolled_dice)
            self.update_turn_score(points)

            if dice == 0:
                dice = 6
                continue
            # Choose to bank if turn points is high enough or amount of dice left is too small
            if self.turn_score >= self.bank_threshold or dice < self.min_dice:
                self.update_score_and_end_turn()
                turn_over = True

    def ev_table_turn(self):
        """
        Uses expected value of the next roll to determine when to bank points.
        If P(Not Farkle) * (current turn points + expected value of next roll) > current turn points, then roll again,
        else, bank points and end turn.
        """
        dice = 6
        turn_over = False
        while not turn_over:
            rolled_dice = roll(dice)
            points, dice = score_roll(rolled_dice)
            self.update_turn_score(points)

            if dice == 0:
                dice = 6
                continue

            # Choose to bank or roll
            prob_no_farkle = self.not_farkle_table[str(dice)].values[0]
            expected_total_points = self.turn_score + self.ev_table[dice].values[0]
            risk_adjusted_expected_points = prob_no_farkle * expected_total_points

            if risk_adjusted_expected_points <= self.turn_score:
                self.update_score_and_end_turn()
                turn_over = True

    def full_turn(self):
        if self.strategy == "basic":
            self.basic_turn()
        elif self.strategy == "ev table":
            self.ev_table_turn()