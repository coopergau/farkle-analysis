from src.player import score_roll

def test_score_roll_returns_correct_scores():
    # Unique rolls
    straight = score_roll([1, 2, 3, 4, 5, 6])
    three_pairs = score_roll([2, 2, 3, 3, 4, 4])
    four_of_a_kind_with_pair = score_roll([2, 2, 2, 2, 1, 1])
    two_triples = score_roll([5, 5, 5, 6, 6, 6])
   
    # Same number multiples
    six_of_a_kind = score_roll([5, 5, 5, 5, 5, 5])
    five_of_a_kind = score_roll([5, 5, 5, 5, 5, 2])
    four_of_a_kind = score_roll([5, 5, 5, 5, 2, 3])
    
    # Three of a kinds
    three_sixes = score_roll([6, 6, 6, 2, 2, 3])
    three_fives = score_roll([5, 5, 5, 2, 2, 3])
    three_fours = score_roll([4, 4, 4, 2, 2, 3])
    three_threes = score_roll([3, 3, 3, 2, 2, 4])
    three_twos = score_roll([2, 2, 2, 3, 3, 4])
    three_ones = score_roll([1, 1, 1, 2, 3, 4])

    # Basic 5s and 1s combos
    one_five = score_roll([5, 2, 2, 4, 6, 3])
    two_fives = score_roll([5, 5, 2, 4, 6, 3])
    one_one = score_roll([1, 2, 2, 4, 6, 3])
    two_ones = score_roll([1, 1, 2, 4, 6, 3])
    five_and_one = score_roll([5, 1, 2, 2, 3, 4])
    two_fives_and_two_ones = score_roll([5, 5, 1, 1, 3, 4])

    # Basic multiples of a kind with a 5 and/or a 1
    triple_3_with_1 = score_roll([3, 3, 3, 1, 2, 6])
    quad_3_with_1 = score_roll([3, 3, 3, 3, 1, 6])
    five_3s_with_1 = score_roll([3, 3, 3, 3, 3, 1])
    triple_3_with_5 = score_roll([3, 3, 3, 5, 2, 6])
    quad_3_with_5 = score_roll([3, 3, 3, 3, 5, 6])
    five_3s_with_5 = score_roll([3, 3, 3, 3, 3, 5])
    triple_3_with_1_and_5 = score_roll([3, 3, 3, 1, 5, 6])

    # Assertions
    assert straight == (1500, 0)
    assert three_pairs == (1500, 0)
    assert four_of_a_kind_with_pair == (1500, 0)
    assert two_triples == (2500, 0)
    
    assert six_of_a_kind == (3000, 0)
    assert five_of_a_kind == (2000, 1)
    assert four_of_a_kind == (1000, 2)
    
    assert three_sixes == (600, 3)
    assert three_fives == (500, 3)
    assert three_fours == (400, 3)
    assert three_threes == (300, 3)
    assert three_twos == (200, 3)
    assert three_ones == (1000, 3)

    assert one_five == (50, 5)
    assert two_fives == (100, 4)
    assert one_one == (100, 5)
    assert two_ones == (200, 4)
    assert five_and_one == (150, 4)
    assert two_fives_and_two_ones == (300, 2)

    assert triple_3_with_1 == (400, 2)
    assert quad_3_with_1 == (1100, 1)
    assert five_3s_with_1 == (2100, 0)
    assert triple_3_with_5 == (350, 2)
    assert quad_3_with_5 == (1050, 1)
    assert five_3s_with_5 == (2050, 0)
    assert triple_3_with_1_and_5 == (450, 1)
