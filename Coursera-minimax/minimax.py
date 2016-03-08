"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)


#import user41_ZS2W2PY7iA_10 as zk 

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """ 
    
    if board.check_win() != None:  
        return SCORES[board.check_win()], (-1, -1)
    
    possible_moves = board.get_empty_squares()
    
    result = (-1, (-1, -1))
    
    for move in possible_moves: 
        # make clone of board, make a move, check to see if move finished game
        board_copy = board.clone() 
        board_copy.move(move[0], move[1], player) 

        
        # Changes player before making another move, need throw away variable 
        # because func returns score and move 
        if SCORES[player] == 1: 
            score, _ = mm_move(board_copy, provided.PLAYERO)
        else: 
            score, _ = mm_move(board_copy, provided.PLAYERX)            
 
        if score * SCORES[player] == 1: 
            return score, move 
 
        elif score * SCORES[player] == 0:
            result = (score, move) 
        
        elif result[0] == -1:  
            result = (result[0], move) 
            
    return result[0] * SCORES[player], result[1]        

#zk.run_suite(mm_move)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
