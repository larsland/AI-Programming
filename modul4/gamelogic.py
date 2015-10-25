import copy
import pickle
import random
import numpy as np


improved_gradient_table = np.array([[64, 32, 16, 8],
                                    [32, 16, 8, 4],
                                    [16, 8, 4, 2],
                                    [8, 4, 2, 1]])

snake_table = np.array([[64503, 32251, 16125, 8062],
                        [4031, 2015, 1007, 503],
                        [251, 125, 62, 31],
                        [1, 3, 7, 15]])


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

    def actions(self, state):
        moves = []
        for i in range(4):
            current_state = np.copy(state)
            board = self.my_move(current_state, i)
            if not np.array_equal(state, board):
                current_state = board
                moves.append((i, current_state))

        return moves

    def utility(self, state, player=None):
        return snake_heuristic(state)  # + 0.1*gradient_heuristic(state)  # + empty_heuristic(state)

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

    def terminal_test(self, state):
        actions = self.actions(state)

        return not actions

    def adv_move2(self, state):
        empty_spots = []
        for i in range(4):
            for j in range(4):
                if state[i, j] == 0:
                    empty_spots.append((i, j))

        if empty_spots:
            x, y = random.choice(empty_spots)
            n = self.distributed_tile()
            state[x, y] = n

        return state

    def distributed_tile(self):
        return 1 if random.randint(0, 100) < 90 else 2

    def adv_move(self, state):
        empty_spots = np.where(state == 0)
        if empty_spots[0].size:
            r = random.choice(range(len(empty_spots[0])))
            x, y = empty_spots[0][r], empty_spots[1][r]
            state[x, y] = self.distributed_tile()
        return state
