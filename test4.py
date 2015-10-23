import unittest
from modul4.gamelogic import _2048, gradient_heuristic
from algorithms.utils import Bunch
import copy


def board_assert_eq(board, other):
    for i, j in zip(board, other):
            for x, y in zip(i, j):
                if x != y:
                    return False
    return True

class TestGameLogic(unittest.TestCase):

    def test_rotate(self):
        g = _2048()

        to_rotate = [[1, 2, 4, 1],
                     [1, 2, 4, 2],
                     [1, 3, 5, 3],
                     [1, 3, 5, 4]]

        one = [[1, 1, 1, 1],
               [3, 3, 2, 2],
               [5, 5, 4, 4],
               [4, 3, 2, 1]]

        two = [[1, 4, 2, 1],
               [2, 4, 2, 1],
               [3, 5, 3, 1],
               [4, 5, 3, 1]]

        two = [[4, 5, 3, 1],
               [3, 5, 3, 1],
               [2, 4, 2, 1],
               [1, 4, 2, 1]]

        three = [[1, 2, 3, 4],
                 [4, 4, 5, 5],
                 [2, 2, 3, 3],
                 [1, 1, 1, 1]]

        self.assertTrue(board_assert_eq(g.rotate(to_rotate, 0), to_rotate))
        self.assertTrue(board_assert_eq(g.rotate(to_rotate, 1), one))
        self.assertTrue(board_assert_eq(g.rotate(to_rotate, 2), two))
        # self.assertTrue(board_assert_eq(g.rotate(to_rotate, 3), three))

    def test_move_right(self):
        g = _2048()
        board = [[1, 2, 3, 4],
                 [4, 4, 5, 5],
                 [2, 2, 3, 3],
                 [1, 1, 1, 1]]
        state = Bunch(to_move=0, utility=0, board=board)

        new = g.make_move(copy.deepcopy(state), 1)

        solution = [[1, 2, 3, 4],
                    [0, 0, 5, 6],
                    [0, 0, 3, 4],
                    [0, 0, 2, 2]]

        not_true = board_assert_eq(state.board, new.board)

        self.assertFalse(not_true)
        self.assertTrue(board_assert_eq(solution, new.board))

    def test_move_down(self):
        g = _2048()
        board = [[1, 1, 3, 1],
                 [1, 1, 3, 1],
                 [2, 1, 2, 1],
                 [2, 1, 2, 1]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.make_move(copy.deepcopy(state), 0)

        solution = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [2, 2, 4, 2],
                    [3, 2, 3, 2]]

        self.assertTrue(board_assert_eq(solution, new.board))

    def test_move_up(self):
        g = _2048()
        board = [[1, 1, 3, 1],
                 [1, 1, 3, 1],
                 [2, 1, 2, 1],
                 [2, 1, 2, 1]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.make_move(copy.deepcopy(state), 2)

        solution = [[2, 2, 4, 2],
                    [3, 2, 3, 2],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]

        self.assertTrue(board_assert_eq(solution, new.board))

    def test_move_left(self):
        g = _2048()
        board = [[1, 2, 3, 4],
                 [4, 4, 5, 5],
                 [2, 2, 3, 3],
                 [1, 1, 1, 1]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.make_move(copy.deepcopy(state), 3)

        solution = [[1, 2, 3, 4],
                    [5, 6, 0, 0],
                    [3, 4, 0, 0],
                    [2, 2, 0, 0]]

        self.assertTrue(board_assert_eq(solution, new.board))

    def test_heuristic(self):
        g = _2048()

        board = [[1, 2, 3, 4],
                 [4, 4, 5, 5],
                 [2, 2, 3, 3],
                 [1, 1, 1, 1]]
        h1 = gradient_heuristic(board)

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.make_move(copy.deepcopy(state), 3)

        h2 = gradient_heuristic(new.board)

        print('Heuristic for board 1', h1)
        print('Heuristic for board 2', h2)


if __name__ == '__main__':
    unittest.main()
