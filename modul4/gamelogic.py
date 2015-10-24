import copy
import pickle
import random
from modul4.adversial import *
from algorithms.utils import Bunch
import numpy as np


improved_gradient_table_backup = np.array([[50, 10, 5, 1],
                                    [10, 6, 3, 2],
                                    [5, 3, 2, 1],
                                    [1, 2, 1, -3]])


improved_gradient_tables = [
    improved_gradient_table,
    np.rot90(improved_gradient_table, 1),
    np.rot90(improved_gradient_table, 2),
    np.rot90(improved_gradient_table, 3)
]


def gradient_heuristic(board, gradient_tables=improved_gradient_tables):
    # Flatten board as numpy 1D array
    board = np.array(board).reshape(-1)
    # Change all values from binary to decimal
    for i, v in enumerate(board):
        board[i] = 1 << v
    # Inflate board to 4x4 matrix
    board.resize((4, 4))

    h = 0
    for table in gradient_tables:
        dot_product = np.dot(board, table)
        h += sum(sum(dot_product))

    return h


class _2048:
    def __init__(self):
        self.initial = np.zeros((4, 4), dtype=np.int)
        self.score = 0

    def actions(self, state, player):
        moves = []
        if player:
            for i in range(4):
                current_state = np.copy(state)
                board = self.my_move(current_state, i)
                if not np.array_equal(state, board):
                    current_state = board
                    moves.append((i, current_state))

        else:
            o = 0
            for y in range(4):
                for x in range(4):
                    if state[x, y] == 0:
                        o += 1
                        current_state_1 = np.copy(state)
                        current_state_1[x, y] = 1

                        current_state_2 = np.copy(current_state_1)
                        current_state_2[x, y] = 2

                        moves.append((o, current_state_1))
                        o += 1
                        moves.append((o, current_state_2))

        return moves

    def utility(self, state, player=None):
        return gradient_heuristic(state)

    def my_move(self, state, move):
        board = state
        merged = []
        moved = False

        # Rotate board and convert to list
        lines = np.rot90(board, -(move+1)).tolist()

        j = 0
        for line in lines:
            while len(line) and line[-1] == 0:
                line.pop(-1)
            i = len(line) - 1
            while i >= 0:
                if line[i] == 0:
                    moved = True
                    line.pop(i)
                i -= 1
            i = 0
            while i < len(line) - 1:
                if line[i] == line[i + 1] and not ((i, j) in merged or (i + 1, j) in merged):
                    moved = True
                    line[i] += 1
                    self.score += 1 * (2 ** line[i])
                    merged.append((i, j))
                    line.pop(i + 1)
                else:
                    i += 1
            while len(line) < len(board):
                line.append(0)

            j += 1

        # Create numpy array from list and rotate it back to original orientation
        board = np.rot90(np.array(lines), (move + 1))

        return board

    def make_move(self, state, move=None, player=False):
        if not player:
            return self.adv_move(state)
        else:
            return self.my_move(state, move)

    def terminal_test(self, state, player):
        actions = self.actions(state, player)

        return not actions

    def adv_move(self, state):
        board = state
        empty_spots = []
        for i in range(0, 4):
            for j in range(0, 4):
                if board[i, j] == 0:
                    empty_spots.append((i, j))
        if empty_spots:
            x, y = random.choice(empty_spots)
            n = self.distributed_tile()
            board[x, y] = n

        return board

    def distributed_tile(self):
        return 1 if random.randint(0, 100) < 90 else 2

if __name__ == '__main__':
    print("wat")