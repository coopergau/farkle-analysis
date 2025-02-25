from typing import List
import random
from player import Player

def tie_break(players):
    """
    For now a tie break is just a randomly chosen winner.
    If ties happen frequently, thi will be adjusted to properly test strategy.
    """
    return random.choice(players)

class Game:
    def __init__(self, players: List[Player], initial_bank=0, winner_threshold=10_000):
        Game.players = players
        Game.initial_bank = initial_bank
        Game.winner_threshold = winner_threshold
        Game.winner = None

    def __str__(self):
        players_info = "\n".join(str(player) for player in self.players)
        winner_info = f"\nWinner: {self.winner}"
        return players_info + winner_info
    
    def play_round(self):
        for player in self.players:
            player.full_turn()

    def check_for_winner(self):
        potential_winners = [player for player in self.players if player.score >= self.winner_threshold]
        if len(potential_winners) == 0:
            # No player over winner threshold
            return False, None
        elif len(potential_winners) == 1:
            # One player over winner threshold
            return True, potential_winners[0]
        else:
            # Multiple players over winner threshold: Choose player with highest points or go to tie break
            max_score = max(player.score for player in potential_winners)
            top_winners = [player for player in potential_winners if player.score == max_score]
            if len(top_winners) == 1:
                # Player with highest points
                return True, top_winners[0]
            else:
                # Tie break
                return True, tie_break(top_winners)

    def play_game(self):
        game_over = False
        while not game_over:
            self.play_round()
            game_over, winner = self.check_for_winner()
        self.winner = winner
    