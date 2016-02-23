"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Creates a list of tuples that are the indexes of the board 
def get_cords(board):
    """ helper func that returns the cords based on size of board """
    dim = board.get_dim()
    score_grid_cords = [(row, col) for col in range(dim) 
                       for row in range(dim)]
    return score_grid_cords
    
def mc_update_scores(scores, board, player): 
    """ logic behind calling score_helper func/which scores to give X or O """
    score_grid_cords = get_cords(board)
    if board.check_win() == provided.DRAW:
        # if board is a draw noting happens
        return
    elif board.check_win() == player: 
        # if winner is equal to player add the appropriate scores to board tiles 
        for row, col in score_grid_cords: 
            if board.square(row, col) == player: 
                scores[row][col] += SCORE_CURRENT
            elif board.square(row, col) == provided.EMPTY:
                pass
            else: 
                scores[row][col] -= SCORE_OTHER 
    else:
        # if winner is not equal to the current player add points to other players
        # move and subtract from the current player's 
        for row, col in score_grid_cords: 
            if board.square(row, col) == player: 
                scores[row][col] -= SCORE_CURRENT
            elif board.square(row, col) == provided.EMPTY:
                pass
            else: 
                scores[row][col] += SCORE_OTHER       
        print scores
            
def mc_trial(board, player):
    """ takes the current board state and player to move as args """
    # uses a while loop to and if statement to check if the board state is won
    # if it isn't it makes a random move on empty square alernating players 
    flag = True 
    while flag: 
        if board.check_win() == None:
            # gets a random tile from the list of tuples of empty spaces 
            tile = random.choice(board.get_empty_squares())
            # makes a move on the empty tile with appropriate player
            board.move(tile[0], tile[1], player)
            # switches player to move using provided switch_player func
            player = provided.switch_player(player)
        else: 
            print board
            flag = False
            return 
                
def get_best_move(board, scores): 
    """ compares scored values of a square to find the highest one and 
        returns that square as the best move """
    empty_squares = board.get_empty_squares()
    move_choice_val = -100
    move_choice_index = []
    
    # steps through each empty square and compares its value to 
    # the move_choice_val if it's larger it becomes new value 
    # and adds index to available move list 
    # if equal in value choice is added to available moves
    for row, col in empty_squares:
        if scores[row][col] > move_choice_val: 
            print scores[row][col]
            move_choice_index = [(row, col)]
            move_choice_val = scores[row][col]

        elif scores[row][col] == move_choice_val: 
            move_choice_index.append((row, col))
            
    # randomly choses a move from best moves and returns it 
    move_square = random.choice(move_choice_index)
    
    return move_square

def mc_move(board, player, trials):
    """ func that gets called when comp is going to move and runs Monte Carlo method on board """
    dim = board.get_dim()
    # Creates a list of lists to serve as a score grid 
    score_grid = [[0 for _ in range(dim)] 
                  for _ in range(dim)]
    print score_grid
    
    for _ in range(trials):
        board_clone = board.clone()
        mc_trial(board_clone, player)

        mc_update_scores(score_grid, board_clone, player) 
    
    move = get_best_move(board, score_grid)
    return move 
    


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
