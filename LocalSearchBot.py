from asyncio.windows_events import INFINITE
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np

class LocalSearchBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        all_row_marked = np.argwhere(state.row_status != 0)
        all_col_marked = np.argwhere(state.col_status != 0)

        # Saat masih pertama, bebas mau generate row atau col
        if (len(all_row_marked) + len(all_col_marked) <= 1):
            print("random")
            return self.get_random_action(state)
        else:
            print("localsearch")
            return self.get_action_local_search(state)

    def get_num_chain_loop(self, state: GameState):
        num_loop = 0
        num_chain = 0
        num_row, num_col = state.board_status.shape

        temp = np.zeros(shape=(num_row, num_col))
        # Mencari Kotak yang sudah Terbentuk
        for locX, locY in np.argwhere(state.board_status == 4):
            temp[locX, locY] = -1
        for locX, locY in np.argwhere(state.board_status == -4):
            temp[locX, locY] = -1

        # Mencari Chain
        still_search_chain = np.any(temp == 0)
        while (still_search_chain):
            is_loop = False
            loc_zero = np.argwhere(temp == 0)[0]
            first_el_chain = loc_zero
            # print(loc_zero)
            count_len_chain = 1
            if (len(loc_zero) != 0):
                x = loc_zero[0]
                y = loc_zero[1]
                temp[x, y] = count_len_chain
                while (True):
                    isMoving = True
                    # Kanan Bawah Kiri Atas
                    if (y+1 < num_col and isMoving):
                        if (state.col_status[x][y+1] == 0 and temp[x, y+1] == 0):
                            y += 1
                            isMoving = False
                    if (x+1 < num_row and isMoving):
                        if (state.row_status[x+1][y] == 0 and temp[x+1, y] == 0):
                            x += 1
                            isMoving = False
                    if (y-1 >= 0 and isMoving):
                        if (state.col_status[x][y] == 0 and temp[x, y-1] == 0):
                            y -= 1
                            isMoving = False
                    if (x-1 >= 0 and isMoving):
                        if (state.row_status[x][y] == 0 and temp[x-1, y] == 0):
                            x -= 1
                            isMoving = False
                    if isMoving:
                        break

                    if (temp[x, y] == 0):
                        count_len_chain += 1
                        temp[x, y] = count_len_chain
                        is_loop = False
                    elif (temp[x, y] == 1 and x == first_el_chain[0] and y == first_el_chain[1]):
                        num_loop += 1
                        is_loop = True
                        break
                if (not is_loop and count_len_chain >= max(num_row, num_col)):
                    num_chain += 1
            still_search_chain = np.any(temp == 0)

        return num_chain, num_loop
    
    def objective_function(self, state: GameState):
        f = 0
        chain, loop = self.get_num_chain_loop(state)
        if (loop != 0 and chain == 0):
            f = 0
        else:
            if (chain % 2 == 1):
                if (state.player1_turn):
                    f = -1
                else:
                    f = 1
            else:
                if (state.player1_turn):
                    f = 1
                else:
                    f = -1
        #playerModifier
        if state.player1_turn:
            mult = -1
        else:
            mult = 1
        sisi4 = np.argwhere(state.board_status == mult*4)
        sisi3 = np.argwhere(state.board_status == mult*3)

        # Tidak ada terbentuk 4 sisi namun terbentuk 3 sisi
        if len(sisi4) == 0 and len(sisi3) > 0:
            f -= len(sisi3)
        # Membentuk kotak 4 sisi dan/atau kotak 3 sisi
        elif len(sisi3) > 0:
            f += len(sisi3) + len(sisi4)
        return f

    def get_random_position_with_zero_value(self, matrix: np.ndarray):
        [ny, nx] = matrix.shape

        x = -1
        y = -1
        valid = False
        
        while not valid:
            x = random.randrange(0, nx)
            y = random.randrange(0, ny)
            valid = matrix[y, x] == 0
        
        return (x, y)

    def get_random_action(self, state: GameState) -> GameAction:
        all_row_marked = np.all(state.row_status != 0)
        all_col_marked = np.all(state.col_status != 0)

        # Mengambil random move
        if not (all_row_marked or all_col_marked):
            if random.random() < 0.5:
                return self.get_random_row_action(state)
            else:
                return self.get_random_col_action(state)
        elif all_row_marked:
            # Jika semua row terisi
            return self.get_random_col_action(state)
        else:
            # Jika semua column terisi
            return self.get_random_row_action(state)        

    def get_random_row_action(self, state: GameState) -> GameAction:
        position = self.get_random_position_with_zero_value(state.row_status)
        return GameAction("row", position)

    def get_random_col_action(self, state: GameState) -> GameAction:
        position = self.get_random_position_with_zero_value(state.col_status)
        return GameAction("col", position)

    def get_action_local_search(self, state: GameState) -> GameAction:
        unmarked_row = np.argwhere(state.row_status == 0)
        unmarked_col = np.argwhere(state.col_status == 0)

        # Menyimpan koordinat i, j dari unmarked_row dan unmarked_col yang terbaik
        best_coord = [0, 0]
        best_move = "no_bestmove"

        best_f = self.objective_function(state)
        for x, y in unmarked_row:
            temp_state = GameState(
                state.board_status.copy(),
                state.row_status.copy(),
                state.col_status.copy(),
                state.player1_turn
            )
            temp_state.row_status[x, y] = 1
            f = self.objective_function(temp_state)
            if (f > best_f):
                best_f = f
                best_coord = [x, y]
                best_move = "row"

        for x, y in unmarked_col:
            temp_state = GameState(
                state.board_status.copy(),
                state.row_status.copy(),
                state.col_status.copy(),
                state.player1_turn
            )
            temp_state.col_status[x, y] = 1
            f = self.objective_function(temp_state)
            if (f > best_f):
                best_f = f
                best_coord = [x, y]
                best_move = "col"

        if best_move == "no_bestmove":
            # Generate random move
            print("No bestmove")
            return self.get_random_action(state)

        print("best move", best_move, [best_coord[1], best_coord[0]])
        return GameAction(best_move, [best_coord[1], best_coord[0]])