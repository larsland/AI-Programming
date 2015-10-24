import copy
import pickle
import random
from modul4.adversial import *
from algorithms.utils import Bunch
import numpy as np

'''
improved_gradient_table = np.array([[0.135759, 0.121925, 0.102812, 0.099937],
                                    [0.0997992, 0.0888405, 0.076711, 0.0724143],
                                    [0.060654, 0.0562579, 0.037116, 0.0151889],
                                    [0.0125498, 0.00992495, 0.00575871, 0.00335193]])
'''

improved_gradient_table = np.array([[64, 32, 16, 8],
                                    [32, 16, 8, 4],
                                    [16, 8, 4, 2],
                                    [8, 4, 2, 1]])

snake_table = np.array([[15, 14, 13, 12],
                        [8, 9, 10, 11],
                        [7, 6, 5, 4],
                        [0, 1, 2, 3]])


def snake_heuristic(board, snake_table=snake_table):
    return sum(sum(board * snake_table))


def gradient_heuristic(board, gradient_table=improved_gradient_table):
    return sum(sum(board * gradient_table))


def empty_heuristic(board):
    num_empty = 0

    for line in board:
        for cell in line:
            if cell == 0:
                num_empty += 1

    return num_empty


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

                        moves.append((o, current_state_1))
                        o += 1

                        current_state_1[x, y] = 2
                        moves.append((o, current_state_1))

        return moves

    def utility(self, state, player=None):
        return 0.8*snake_heuristic(state) + 0.2*gradient_heuristic(state)  # + empty_heuristic(state)

    def my_move(self, state, move):
        board = state
        merged = []
        moved = False

        # Rotate board and convert to list
        lines = np.rot90(board, -(move + 1)).tolist()

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
        empty_spots = []
        for i in range(4):
            for j in range(4):
                if state[i, j] == 0:
                    empty_spots.append((i, j))
        print(empty_spots)
        if empty_spots:
            x, y = random.choice(empty_spots)
            n = self.distributed_tile()
            state[x, y] = n

        return state

    def distributed_tile(self):
        return 1 if random.randint(0, 100) < 90 else 2

    def adv_move2(self, state):
        empty_spots = np.where(state == 0)[0]
        return empty_spots
