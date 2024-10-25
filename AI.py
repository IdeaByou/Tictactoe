import random
import copy

class AI():
    def __init__(self,lv = 1, player = 2) :
        self.level = lv
        self.player = player
        
    def random_play(self,board):
        empty_sqrs = board.get_empty_sqr()
        return random.choice(empty_sqrs)
    
    def minimax_play(self,board,maximizing):
        
        #terminal case
        case = board.state(show=False)
        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isFull():
            return 0, None
        
        #Base Case
        if maximizing :
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqr()
            
            for row, column in empty_sqrs :
                temp_board = copy.deepcopy(board)
                temp_board.mark(row,column,1)
                eval = self.minimax_play(temp_board,False)[0]
                if eval > max_eval :
                    max_eval = eval 
                    best_move = (row,column)
        
            return (max_eval, best_move)
        
        elif not maximizing :
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqr()
            
            for row, column in empty_sqrs :
                temp_board = copy.deepcopy(board)
                temp_board.mark(row,column,self.player)
                eval = self.minimax_play(temp_board,True)[0]
                if eval < min_eval :
                    min_eval = eval 
                    best_move = (row,column)
        
            return (min_eval, best_move)    

    def play(self, board):
        if self.level == 0 :
            #random 
            return self.random_play(board)
        else :
            #minimax
            score,move = self.minimax_play(board,False)
            return move #return best mark position (row,col)
 