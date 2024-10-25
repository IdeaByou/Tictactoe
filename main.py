import sys #help to quit application
import pygame
import numpy 
import random
import copy
from Constant import *

#PYGAME
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( "TIC TAC TOE" )
screen.fill( BG_COLOR )

#CLASS
class Board : 
    def __init__(self) :
        self.squares = numpy.zeros((ROWS,COLUMNS))
        self.empty_sqr = self.squares
        self.marked_sqr = 0
        
    def state (self,show=False):
        """
        return 0 : no one win
        return 1 : player 1 win
        return 2 : player 2 win
        """
        #Vertical win 
        for i in range(COLUMNS):
            if self.squares[0][i] == self.squares[1][i] == self.squares[2][i] != 0 :
                if show:
                    color = PLAYER2_COLOR if self.squares[0][i] == 2 else PLAYER1_COLOR
                    iPos = (i * SQ_SIZE + SQ_SIZE // 2, 20)
                    fPos = (i * SQ_SIZE + SQ_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                
                return self.squares[0][i]
        #Horizontal win
        for i in range(ROWS):
            if self.squares[i][0] == self.squares[i][1] == self.squares[i][2] != 0 :
                if show:
                    color = PLAYER2_COLOR if self.squares[i][0] == 2 else PLAYER1_COLOR
                    iPos = (20, i * SQ_SIZE + SQ_SIZE // 2)
                    fPos = (WIDTH - 20, i * SQ_SIZE + SQ_SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[i][0]
            
        #Digonal win 
        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = PLAYER2_COLOR if self.squares[i][0] == 2 else PLAYER1_COLOR
                iPos = (20, 20)
                fPos = (i * SQ_SIZE + SQ_SIZE // 2, i * SQ_SIZE + SQ_SIZE // 2)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        # asc Digonal
        elif self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if show:
                color = PLAYER2_COLOR if self.squares[i][0] == 2 else PLAYER1_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        
        #No win yet
        return 0
            
    def mark (self, row, column, player):
        self.squares[row][column] = player
        self.marked_sqr += 1
        
    def isEmpty_sqr (self, row, column):
        return self.squares[row][column] == 0 
    
    def get_empty_sqr (self):
        sqrs = []
        for i in range(ROWS):
            for j in range(COLUMNS):
                if self.isEmpty_sqr(i,j):
                    sqrs.append((i,j))
        return sqrs            
        
    def isFull (self):
        return self.marked_sqr == 9 
        
    def isEmpty (self):
        return self.marked_sqr == 0 

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
             
class Game :
    def __init__(self,mode = 'ai',ai_lv = 1):
        self.board = Board()
        self.player = 1 # 1 : X , 2 : O
        self.showLine()
        self.gamemode = mode # "pvp" or "ai"
        self.running =  True
        self.ai_lv = ai_lv
        self.ai = AI(lv=self.ai_lv)
    
    def showLine (self):
        #Vetical Liness
        pygame.draw.line(screen,LINE_COLOR,(SQ_SIZE,0),(SQ_SIZE,HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(SQ_SIZE*2,0),(SQ_SIZE*2,HEIGHT),LINE_WIDTH)
        
        #Horizontal Lines
        pygame.draw.line(screen,LINE_COLOR,(0,SQ_SIZE),(WIDTH,SQ_SIZE),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,SQ_SIZE*2),(WIDTH,SQ_SIZE*2),LINE_WIDTH)
        
    def next_turn (self):
        self.player = self.player % 2 + 1
        
    def draw_fig (self,row,column,player):
        if player == 1 :
            #Draw X
            pygame.draw.line(screen,PLAYER1_COLOR,\
                (column * SQ_SIZE + X_OFFSET, row * SQ_SIZE + X_OFFSET),\
                ((column+1) * SQ_SIZE - X_OFFSET, (row+1) * SQ_SIZE - X_OFFSET),X_WIDTH)
            pygame.draw.line(screen,PLAYER1_COLOR,\
                ((column+1) * SQ_SIZE - X_OFFSET, row * SQ_SIZE + X_OFFSET),\
                ((column) * SQ_SIZE + X_OFFSET, (row+1) * SQ_SIZE - X_OFFSET),X_WIDTH)
        else :
            #Draw O
            pygame.draw.circle(screen,PLAYER2_COLOR,(column * SQ_SIZE + SQ_SIZE//2, row * SQ_SIZE + SQ_SIZE//2),CIRCLE_RADIUS,CIRCLE_WIDTH)
    
    def make_move(self,row,column,player):
        self.board.mark(row,column,player)
        #draw
        self.draw_fig(row,column,player)
        self.next_turn()
    
    def change_gamemode(self):
        self.gamemode = "ai" if self.gamemode == 'pvp' else 'pvp'
        
    def isEnd(self):
        return self.board.isFull() or self.board.state(show=True) 
    
    def reset(self):
        # Reset game state
        self.__init__(mode = self.gamemode, ai_lv= self.ai.level)
        
        # Clear screen
        screen.fill(BG_COLOR)
        
        # Redraw lines
        self.showLine()
        
        # Update display
        pygame.display.update()

def main ():
    
    game = Game()
    board = game.board
    ai = game.ai
    pygame.display.set_caption( f"TIC TAC TOE - {game.gamemode} {'' if game.gamemode == 'pvp' else f'LV : {ai.level}'}" )
    while True :

        #pygame event
        for event in pygame.event.get():
            
            #Player quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # keydown event
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                    game.reset()
                    board = game.board
                    ai = game.ai
                    pygame.display.set_caption( f"TIC TAC TOE - {game.gamemode} {'' if game.gamemode == 'pvp' else f'LV : {ai.level}'}" )
                    pygame.display.update()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
    
                # 0-random ai
                if (event.key == pygame.K_KP0 or event.key == pygame.K_0) and ai.level != 0 and game.gamemode == "ai":
                    ai.level = 0
                    game.reset()
                    board = game.board
                    ai = game.ai
                    pygame.display.set_caption( f"TIC TAC TOE - {game.gamemode} {'' if game.gamemode == 'pvp' else f'LV : {ai.level}'}" )
                    pygame.display.update()
                
                # 1-minimax ai
                if (event.key == pygame.K_KP1 or event.key == pygame.K_1) and ai.level != 1 and game.gamemode == "ai" :
                    ai.level = 1
                    game.reset()
                    board = game.board
                    ai = game.ai
                    pygame.display.set_caption( f"TIC TAC TOE - {game.gamemode} {'' if game.gamemode == 'pvp' else f'LV : {ai.level}'}" )
                    pygame.display.update()
                    
            #Player click event
            if event.type == pygame.MOUSEBUTTONDOWN and game.running :
                x,y = event.pos
                column,row = x//SQ_SIZE, y //SQ_SIZE
                
                #Player mark
                if game.board.isEmpty_sqr(row,column):    
                    game.make_move(row,column,game.player)
                    
                    if game.isEnd():
                        game.running = False
                 
        if game.gamemode == "ai" and game.player == ai.player and game.running:
            #updatesceen 
            pygame.display.update() 
                
            #ai methods
            row, column = ai.play(board)
            game.make_move(row,column,ai.player)
            
            if game.isEnd():
                game.running = False
                   
        pygame.display.update()
                
main()