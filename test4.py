import unittest
from modul4.gamelogic import _2048, gradient_heuristic
from algorithms.utils import Bunch
import copy
import numpy as np


def board_assert_eq(board, other):
    for i, j in zip(board, other):
            for x, y in zip(i, j):
                if x != y:
                    return False
    return True


class TestGameLogic(unittest.TestCase):
    def test_rotate(self):
        to_rotate = np.array([[1, 2, 4, 1],
                             [1, 2, 4, 2],
                             [1, 3, 5, 3],
                             [1, 3, 5, 4]])

        one = np.array([[1, 1, 1, 1],
                       [3, 3, 2, 2],
                       [5, 5, 4, 4],
                       [4, 3, 2, 1]])

        two = np.array([[4, 5, 3, 1],
                       [3, 5, 3, 1],
                       [2, 4, 2, 1],
                       [1, 4, 2, 1]])

        three = np.array([[1, 2, 3, 4],
                         [4, 4, 5, 5],
                         [2, 2, 3, 3],
                         [1, 1, 1, 1]])

        # Rotates 90 degrees counter-clockwise.
        self.assertTrue(np.array_equal(np.rot90(to_rotate, 0), to_rotate))
        self.assertTrue(np.array_equal(np.rot90(to_rotate, 1), three))
        self.assertTrue(np.array_equal(np.rot90(to_rotate, 2), two))
        self.assertTrue(np.array_equal(np.rot90(to_rotate, 3), one))

    def test_move_right(self):
        g = _2048()
        board = [[1, 2, 3, 4],
                 [4, 4, 5, 5],
                 [2, 2, 3, 3],
                 [1, 1, 1, 1]]
        state = Bunch(to_move=0, utility=0, board=board)

        new = g.my_move(copy.deepcopy(state), 1)

        solution = [[1, 2, 3, 4],
                    [0, 0, 5, 6],
                    [0, 0, 3, 4],
                    [0, 0, 2, 2]]

        not_true = np.array_equal(state.board, new)

        self.assertFalse(not_true)
        self.assertTrue(np.array_equal(solution, new))

    def test_move_down(self):
        g = _2048()
        board = [[1, 1, 3, 1],
                 [1, 1, 3, 1],
                 [2, 1, 2, 1],
                 [2, 1, 2, 1]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.my_move(copy.deepcopy(state), 0)

        solution = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [2, 2, 4, 2],
                    [3, 2, 3, 2]]

        not_true = np.array_equal(state.board, new)

        self.assertFalse(not_true)
        self.assertTrue(np.array_equal(solution, new))

    def test_move_up(self):
        g = _2048()
        board = [[1, 1, 3, 1],
                 [1, 1, 3, 1],
                 [2, 1, 2, 1],
                 [2, 1, 2, 1]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.my_move(copy.deepcopy(state), 2)

        solution = [[2, 2, 4, 2],
                    [3, 2, 3, 2],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]

        not_true = np.array_equal(state.board, new)

        self.assertFalse(not_true)
        self.assertTrue(np.array_equal(solution, new))

    def test_move_left(self):
        g = _2048()
        board = [[1, 2, 3, 4],
                 [4, 4, 5, 5],
                 [2, 2, 3, 3],
                 [1, 1, 1, 1]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.my_move(copy.deepcopy(state), 3)

        solution = [[1, 2, 3, 4],
                    [5, 6, 0, 0],
                    [3, 4, 0, 0],
                    [2, 2, 0, 0]]

        not_true = np.array_equal(state.board, new)

        self.assertFalse(not_true)
        self.assertTrue(np.array_equal(solution, new))

    def test_heuristic(self):
        g = _2048()

        board = [[3, 0, 0, 0],
                 [3, 1, 2, 0],
                 [3, 1, 2, 0],
                 [3, 0, 0, 0]]


        state = Bunch(to_move=0, utility=0, board=board)


        up = g.my_move(copy.deepcopy(state), 2)
        down = g.my_move(copy.deepcopy(state), 0)
        right = g.my_move(copy.deepcopy(state), 1)
        left = g.my_move(copy.deepcopy(state), 3)


        b_h = gradient_heuristic(board)
        u_h = gradient_heuristic(up)
        d_h = gradient_heuristic(down)
        r_h = gradient_heuristic(right)
        l_h = gradient_heuristic(left)

        self.assertLess(b_h, u_h)
        self.assertLess(b_h, d_h)
        self.assertLess(r_h, u_h)
        self.assertLess(l_h, d_h)

        self.assertTrue(d_h - u_h < 1)
        self.assertTrue(r_h - l_h < 1)


if __name__ == '__main__':
    unittest.main()
