from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np
from copy import deepcopy

class MinimaxBot(Bot):
    num_of_square = 4
    def __init__(self):
        pass

    def get_action(self, state: GameState) -> GameAction:
        _,bestAction = self.minimax(state,True,-9999,9999)
        return bestAction

    def utility_value(self, state : GameState) -> int:
        if state.player1_turn:
            return np.count_nonzero(state.board_status==-4)
        else:
            return np.count_nonzero(state.board_status==4)

    def get_next_turn(self,state : GameState, act : GameAction) -> tuple[bool,GameState]:
        state_copy = deepcopy(state)
        x = act.position[0]
        y = act.position[1]
        val = 1
        playerModifier = 1
        scored = False
        if state.player1_turn:
            playerModifier = -1
        if act.action_type=='row':
            state_copy.row_status[x][y] = playerModifier
        else :
            state_copy.col_status[x][y] = playerModifier
            

        if y < (MinimaxBot.num_of_square-1) and x < (MinimaxBot.num_of_square-1):
            state_copy.board_status[y][x] = (abs(state_copy.board_status[y][x]) + val) * playerModifier
            if abs(state_copy.board_status[y][x]) == 4:
                scored = True

        if type == 'row':
            state_copy.row_status[y][x] = 1
            if y >= 1:
                state_copy.board_status[y-1][x] = (abs(state_copy.board_status[y-1][x]) + val) * playerModifier
                if abs(state_copy.board_status[y-1][x]) == 4:
                    scored = True

        elif type == 'col':
            state_copy.col_status[y][x] = 1
            if x >= 1:
                state_copy.board_status[y][x-1] = (abs(state_copy.board_status[y][x-1]) + val) * playerModifier
                if abs(state_copy.board_status[y][x-1]) == 4:
                    scored = True
        print(scored,state_copy.player1_turn)
        if scored :
            return state_copy.player1_turn,state_copy
        else:
            return not state_copy.player1_turn, state_copy

    def minimax(self,state : GameState, isMaximize : bool, alpha : int, beta : int) -> tuple[int,GameAction]:
        bot_code = state.player1_turn
        print(state.row_status)
        if ((state.row_status == 1).all() and (state.col_status == 1).all()):
            return (self.utility_value(state),None)

        MAX, MIN = 1000, -1000
        row_choices = [(x,y) for x in range(MinimaxBot.num_of_square) for y in range(MinimaxBot.num_of_square-1)]
        col_choices = [(x,y) for x in range(MinimaxBot.num_of_square-1) for y in range(MinimaxBot.num_of_square)]

        if isMaximize:
            bestValue = -9999
            bestStep = None
            for i,j in row_choices :
                if state.row_status[i][j] == 0 :
                    next_turn,state_copy = self.get_next_turn(state,GameAction('row',(i,j)))
                    print(state_copy.row_status)
                    value,_ = self.minimax(state_copy,next_turn==bot_code,alpha,beta)
                    if bestValue < value :
                        bestValue = value
                        bestStep = GameAction('row',(j,i))
                    alpha = max(alpha,bestValue)
                    if beta <= alpha :
                        break
            for i,j in col_choices :
                if state.col_status[i][j] == 0 :
                    next_turn,state_copy = self.get_next_turn(state,GameAction('col',(i,j)))
                    value,_ = self.minimax(state_copy,next_turn==bot_code,alpha,beta)
                    if bestValue < value :
                        bestValue = value
                        bestStep = GameAction('col',(j,i))
                    alpha = max(alpha,bestValue)
                    if beta <= alpha :
                        break

            return bestValue, bestStep

        else:
            bestValue = 9999
            bestStep = None
            for i,j in row_choices:
                if state.row_status[i][j] == 0 :
                    next_turn,state_copy = self.get_next_turn(state,GameAction('row',(i,j)))
                    value,_ = self.minimax(state_copy,next_turn==bot_code,alpha,beta)
                    if bestValue > value :
                        bestValue = value
                        bestStep = GameAction('row',(i,j))
                    beta = min(beta,bestValue)
                    if beta <= alpha :
                        break
            for i,j in col_choices:
                if state.col_status[i][j] == 0 :
                    next_turn,state_copy = self.get_next_turn(state,GameAction('col',(i,j)))
                    value,_ = self.minimax(state_copy,next_turn==bot_code,alpha,beta)
                    if bestValue > value :
                        bestValue = value
                        bestStep = GameAction('col',(i,j))
                    beta = min(beta,bestValue)
                    if beta <= alpha :
                        break

            return bestValue, bestStep
        

# if __name__=='__main__':
#     bot = MinimaxBot()
#     bot.minimax(None,True,0,0)

    