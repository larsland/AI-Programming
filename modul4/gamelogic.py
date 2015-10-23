import copy
import pickle
import random
from modul4.adversial import *
from algorithms.utils import Bunch
import numpy as np


improved_gradient_table = np.array([[0.135759, 0.121925, 0.102812, 0.099937],
                                    [0.0997992, 0.0888405, 0.076711, 0.0724143],
                                    [0.060654, 0.0562579, 0.037116, 0.0151889],
                                    [0.0125498, 0.00992495, 0.00575871, 0.00335193]])

'''
improved_gradient_table = np.array([[50, 10, 5, 1],
                                    [10, 6, 3, 2],
                                    [5, 3, 2, 1],
                                    [1, 2, 1, -3]])
'''

improved_gradient_tables = [
    improved_gradient_table,
    np.rot90(improved_gradient_table, 1),
    np.rot90(improved_gradient_table, 2),
    np.rot90(improved_gradient_table, 3)
]


def gradient_heuristic(board, gradient_tables=improved_gradient_tables):
    h = 0
    for table in gradient_tables:
        for x, y in zip(board, table):
            for i, j in zip(x, y):
                h += (1 << i) * j
        # dot_product = np.dot(np.array(board), table)
        # h += sum(sum(dot_product))

    return h


class _2048(Game):
    def __init__(self):
        initial = Bunch(to_move=0, utility=0, board=[[]], moves=[])
        initial.board = np.zeros((4, 4), dtype=np.int)
        self.initial = initial
        self.score = 0
        '''
        self.gradient_tables = \
            [
                np.array([[7, 6, 5, 4],
                          [6, 5, 4, 3],
                          [5, 4, 3, 2],
                          [4, 3, 2, 1]]),
                np.array([[1, 2, 3, 4],
                          [2, 3, 4, 5],
                          [3, 4, 5, 6],
                          [4, 5, 6, 7]]),
                np.array([[4, 5, 6, 7],
                          [3, 4, 5, 6],
                          [2, 3, 4, 5],
                          [1, 2, 3, 4]]),
                np.array([[4, 3, 2, 1],
                          [5, 4, 3, 2],
                          [6, 5, 4, 3],
                          [7, 6, 5, 4]])
            ]
        '''

    def actions(self, state, player=True):
        moves = []
        if player:
            for i in range(4):
                # current_state = pickle.loads(pickle.dumps(state, -1))
                current_state = copy.deepcopy(state)
                board = self.my_move(current_state, i)
                if not np.array_equal(state.board, board):
                    current_state.board = board
                    moves.append((i, current_state))
        else:
            for y in range(4):
                for x in range(4):
                    if state.board[x, y] == 0:
                        current_state_1 = copy.deepcopy(state)
                        current_state_1.board[x][y] = 1

                        current_state_2 = copy.deepcopy(state)
                        current_state_2.board[x, y] = 2

                        moves.append((x, current_state_1))
                        moves.append((x, current_state_1))
        for move in moves:
            print('yo', move[1].board)
        return moves

    def utility(self, state, player=None):
        return gradient_heuristic(state.board)

    def my_move(self, state, move):
        board = state.board
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
            return Bunch(to_move=0, utility=0, board=self.adv_move(state))
        else:
            return Bunch(to_move=1, utility=0, board=self.my_move(state, move))

    def terminal_test(self, state):
        return not self.actions(state)

    def adv_move(self, state):
        board = state.board
        empty_spots = []
        for i in range(0, 4):
            for j in range(0, 4):
                if board[i, j] == 0:
                    empty_spots.append((i, j))
        if empty_spots:
            tile = random.choice(empty_spots)
            n = self.distributed_tile()
            board[tile[0]][tile[1]] = n

        return board

    def distributed_tile(self):
        return 1 if random.randint(0, 100) < 90 else 2

if __name__ == '__main__':
    print("wat")