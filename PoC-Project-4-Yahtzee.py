"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""
# http://www.codeskulptor.org/#user39_Io14jzkfjB_2.py


# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    if not hand:
        return 0
    six_scores = []
    for item in hand:
        six_scores.append(hand.count(item)*item)
    return max(six_scores)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    die = [num for num in range(1, num_die_sides + 1)]
    possible_seq = gen_all_sequences(die, num_free_dice)
    scores = []
    for item in possible_seq:
        scores.append(score(held_dice + item))
    return float(sum(scores)) / float(len(scores))

# print expected_value((2, 2), 6, 2) 

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    hand_hold = [()]
    for item in hand:
        for subset in hand_hold:
            hand_hold = hand_hold + [tuple(subset) + (item,)]
    return set(hand_hold)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    result = (0.0, ())
    current_score = 0.0
    
    for item in gen_all_holds(hand):
        value = expected_value(item, num_die_sides, len(hand) - len(item))
        if value > current_score:
            current_score = value
            result = (current_score, item)
  
    return result


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score

#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    




