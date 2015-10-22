import copy
import pickle
import random
from modul4.adversial import *
from algorithms.utils import Bunch


class Tile:
    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class _2048(Game):
    def __init__(self):
        self.initial = Bunch(to_move=0, utility=0, board=[[]], moves=[])
        self.score = 0

    def legal_moves(self, state):
        moves = []
        for i in range(4):
            # current_state = pickle.loads(pickle.dumps(state, -1))
            current_state = copy.deepcopy(state)
            move = self.make_move(i, current_state)
            if state.board != move.board:
                moves.append(i)
        return moves

    def utility(self, state, player):
        pass

    def to_move(self, state):
        pass

    def display(self, state):
        print(state)

    def my_move(self, move, state):
        board = state.board
        merged = []
        moved = False
        lines = self.rotate(board, move+1)
        for line in lines:
            while len(line) and line[-1].value == 0:
                line.pop(-1)
            i = len(line)-1
            while i >= 0:
                if line[i].value == 0:
                    moved = True
                    line.pop(i)
                i -= 1
            i = 0
            while i < len(line)-1:
                if line[i].value == line[i+1].value and not (line[i] in merged or line[i+1] in merged):
                    moved = True
                    line[i] = Tile(line[i].value + 1)
                    self.score += 1 * (2**line[i].value)
                    merged.append(line[i])
                    line.pop(i+1)
                else:
                    i += 1
            while len(line) < len(board):
                line.append(Tile())

        board = self.rotate(lines, 0-(move+1))

        #if moved:
        #    board = self.add_random_tile(board)

        board = board
        return board

    def make_move(self, move, state):
        print("wat", state.to_move)
        if state.to_move:
            return Bunch(to_move=0, utility=0, board=self.adv_move(state))
        else:
            return Bunch(to_move=1, utility=0, board=self.my_move(move, state))

    def terminal_test(self, state):
        return not self.legal_moves(state)

    def adv_move(self, state):
        board = state.board
        empty_spots = []
        for i in range(0, 4):
            for j in range(0, 4):
                if board[i][j].value == 0:
                    empty_spots.append((i, j))
        if empty_spots:
            tile = random.choice(empty_spots)
            n = self.distributed_tile()
            board[tile[0]][tile[1]].value = n

        return board

    def distributed_tile(self):
        return 1 if random.randint(0, 100) < 90 else 2

    def rotate(self, l, num):
        num %= 4
        s = len(l)-1
        l2 = []
        if num == 0:
            l2 = l
        elif num == 1:
            l2 = [[None for i in j] for j in l]
            for y in range(len(l)):
                for x in range(len(l[y])):
                    l2[x][s-y] = l[y][x]
        elif num == 2:
            l2 = l
            l2.reverse()
            for i in l:
                i.reverse()
        elif num == 3:
            l2 = [[None for i in j] for j in l]
            for y in range(len(l)):
                for x in range(len(l[y])):
                    l2[y][x] = l[x][s-y]
        return l2




'''
class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self, h=3, v=3, k=3):
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Bunch(to_move='X', utility=0, board={}, moves=moves)

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def make_move(self, move, state):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return Bunch(to_move=if_(state.to_move == 'X', 'O', 'X'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def utility(self, state):
        "Return the value to X; 1 for win, -1 for loss, 0 otherwise."
        return state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print(board.get((x, y), '.')),
            print("wat")

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (
                self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))
            ):
            return if_(player == 'X', +1, -1)
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x, delta_y):
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k
'''

if __name__ == '__main__':
    print("wat")