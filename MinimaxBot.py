from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np
from copy import deepcopy
from time import sleep

class MinimaxBot(Bot):
    num_of_square = 4
    def __init__(self):
        pass

    def get_action(self, state: GameState) -> GameAction:
        self.bot_code = state.player1_turn
        bestValue, bestAction = self.minimax(state, True, -9999, 9999,0)
        return bestAction

    def utility_value(self, state : GameState) -> int:
        f = 0
        if (self.bot_code): #Jika bot adalah player 1
            mult = -1
        else:
            mult = 1
        sisi4 = np.argwhere(state.board_status == mult*4)
        sisi3 = np.argwhere(np.abs(state.board_status) == 3)
        sisi4lawan = np.argwhere(state.board_status == -1*mult*4)
        f+=(len(sisi4)-len(sisi4lawan))
        if (state.player1_turn!=self.bot_code): #Jika state yang akan dihitung bukan giliran bot
            f -= len(sisi3)
        else :
            f += len(sisi3)
        return f

    def get_next_turn(self, state : GameState, act : GameAction) -> (bool, GameState):
        state_copy = deepcopy(state)
        x = act.position[0]
        y = act.position[1]
        val = 1
        playerModifier = 1
        scored = False
        if state.player1_turn:
            playerModifier = -1

        if act.action_type == 'row':
            state_copy.row_status[y][x] = playerModifier
        else :
            state_copy.col_status[y][x] = playerModifier
            

        if y < (MinimaxBot.num_of_square - 1) and x < (MinimaxBot.num_of_square - 1):
            state_copy.board_status[y][x] = (abs(state_copy.board_status[y][x]) + val) * playerModifier
            if abs(state_copy.board_status[y][x]) == 4:
                scored = True

        if act.action_type == 'row':
            state_copy.row_status[y][x] = 1
            if y >= 1:
                state_copy.board_status[y-1][x] = (abs(state_copy.board_status[y-1][x]) + val) * playerModifier
                if abs(state_copy.board_status[y-1][x]) == 4:
                    scored = True
        elif act.action_type == 'col':
            state_copy.col_status[y][x] = 1
            if x >= 1:
                state_copy.board_status[y][x-1] = (abs(state_copy.board_status[y][x-1]) + val) * playerModifier
                if abs(state_copy.board_status[y][x-1]) == 4:
                    scored = True
        if scored :
            return state_copy.player1_turn, state_copy
        else:
            return not state_copy.player1_turn, GameState(board_status=state_copy.board_status,row_status=state_copy.row_status,col_status=state_copy.col_status,player1_turn=not state_copy.player1_turn)#state_copy

    def get_best_step(self, alpha : int, beta : int, value : int, bestValue : int, isIteratingRow : bool, coord : (int, int), bestStep : GameAction, isMaximize : bool) -> (int, GameAction, int):
        if isMaximize:
            if (bestValue < value) :
                bestValue = value
                bestStep = GameAction(action_type='row' if isIteratingRow else 'col', position=coord)
            prune = max(alpha, bestValue)
            return (prune, bestStep, bestValue)
        else :
            if (bestValue > value) :
                bestValue = value
                bestStep = GameAction(action_type='row' if isIteratingRow else 'col', position=coord)
            prune = min(beta, bestValue)
            return (prune, bestStep, bestValue)


    def minimax(self, state : GameState, isMaximize : bool, alpha : int, beta : int, depth : int) -> (int,GameAction):
        if ((state.row_status == 1).all() and (state.col_status == 1).all()) or (depth>=5):
            return (self.utility_value(state),None)

        MAX, MIN = 1000, -1000
        row_choices = [(x,y) for x in range(MinimaxBot.num_of_square-1) for y in range(MinimaxBot.num_of_square)]
        col_choices = [(x,y) for x in range(MinimaxBot.num_of_square) for y in range(MinimaxBot.num_of_square-1)]

        bestStep = GameAction("row",(0,0)) #DEFAULT VALUE
        bestValue = -9999 if isMaximize else 9999

        for i,j in row_choices :
            if state.row_status[j][i] == 0 :
                next_turn, state_copy = self.get_next_turn(state, GameAction('row', (i,j)))             
                value,_ = self.minimax(state_copy,next_turn==self.bot_code,alpha,beta,depth+1)
                prune, bestStep, bestValue = self.get_best_step(alpha, beta, value, bestValue, True, (i,j), bestStep, isMaximize)
                if isMaximize :
                    alpha = prune
                else :
                    beta = prune
                if beta <= alpha :
                    break

        for i,j in col_choices :
            if state.col_status[j][i] == 0 :
                next_turn, state_copy = self.get_next_turn(state, GameAction('col', (i,j)))
                value,_ = self.minimax(state_copy,next_turn==self.bot_code,alpha,beta,depth+1)
                prune, bestStep, bestValue = self.get_best_step(alpha, beta, value, bestValue, False, (i,j), bestStep, isMaximize)
                if isMaximize :
                    alpha = prune
                else :
                    beta = prune
                if beta <= alpha :
                    break
                
        return bestValue, bestStep