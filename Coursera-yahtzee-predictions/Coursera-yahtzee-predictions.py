"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

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
    # reutrning a score for the box with the largest value
    # includes the combination of like die (ex. 2, 2, 2 = 6)
    hand_score = 0
    for item in hand: 
        count = hand.count(item) 
        score_update = count * item
        if score_update > hand_score: 
            hand_score = score_update
    return hand_score 


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    list_of_outcomes = list(range(1, num_die_sides + 1))
    all_rolls = gen_all_sequences(list_of_outcomes, num_free_dice)
    # gets a set of all possible sorted tuples for dice rolls using remaing die
    
    # uses for loop below to step through possible outcomes, updates the 
    # score from our score function for each hand possible. Then divides
    # the score by the total number of hands tested. To get average expected_val. 

    temp_scores = []
    for item in all_rolls: 
        temp_scores.append(score(held_dice + item))
        
    final_score = float(sum(temp_scores)) / len(temp_scores) 
    return final_score         



def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    power_set = [[]]
    for elem in hand:
        # iterate over the sub sets so far
        for sub_set in power_set:
        # add a new subset consisting of the subset at hand added elem
            small_set = [list(sub_set) + [elem]]
            power_set = power_set + small_set  
    output_set = set()
    for item in power_set:         
        output_set.add(tuple(item))
    return output_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    
    output = (0.0, ())
    current_value = 0 
    
    for dice_held in all_holds: 
        temp = expected_value(dice_held, num_die_sides, len(hand) - len(dice_held)) 
        if temp > current_value:
            current_value = temp 
            output = (temp, dice_held)
    return output 


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



