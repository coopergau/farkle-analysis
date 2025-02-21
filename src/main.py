from player import Player
from game import Game

SIMS = 10_000

def main():

    winners_dict = {"One": 0, "Two": 0, "Three": 0, "Four": 0, "Five": 0, "Six": 0}
    for _ in range(SIMS):
        one_dice = Player("One", min_dice=1, bank_threshold=500)
        two_dice = Player("Two", min_dice=2, bank_threshold=500)
        three_dice = Player("Three", min_dice=3, bank_threshold=500)
        four_dice = Player("Four", min_dice=4, bank_threshold=500)
        five_dice = Player("Five", min_dice=5, bank_threshold=500)
        six_dice = Player("Six", min_dice=6, bank_threshold=500)
        game = Game([one_dice, two_dice, three_dice, four_dice, five_dice, six_dice])
        game.play_game()
        winner = game.winner
        winners_dict[winner.name] += 1
        print(winners_dict)



if __name__ == "__main__":
    main()