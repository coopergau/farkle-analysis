import random
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
    def __init__(self, name: str, min_dice: int, bank_threshold: int):
        """
        Player strategy variables:
        min_dice: Minimum amount of dice they will roll, bank points otherwise.
        bank_threshold: Amount of points they will bank after reaching in that turn.
        """
        self.name = name
        self.min_dice = min_dice
        self.bank_threshold = bank_threshold
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
    
    def full_turn(self):
        dice = 6
        turn_over = False
        while not turn_over:
            rolled_dice = roll(dice)
            points, dice = score_roll(rolled_dice)
            self.update_turn_score(points)

            if self.turn_score >= self.bank_threshold or dice < self.min_dice:
                self.update_score_and_end_turn()
                turn_over = True

        