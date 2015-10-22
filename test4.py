import unittest
from modul4.gamelogic import _2048, Tile
from algorithms.utils import Bunch
import copy


def board_assert_eq(board, other):
    for i, j in zip(board, other):
            for x, y in zip(i, j):
                if x.value != y.value:
                    return False
    return True

class TestGameLogic(unittest.TestCase):

    def test_rotate(self):
        g = _2048()

        to_rotate = [[Tile(1), Tile(2), Tile(4), Tile(1)],
                     [Tile(1), Tile(2), Tile(4), Tile(2)],
                     [Tile(1), Tile(3), Tile(5), Tile(3)],
                     [Tile(1), Tile(3), Tile(5), Tile(4)]]

        one = [[Tile(1), Tile(1), Tile(1), Tile(1)],
               [Tile(3), Tile(3), Tile(2), Tile(2)],
               [Tile(5), Tile(5), Tile(4), Tile(4)],
               [Tile(4), Tile(3), Tile(2), Tile(1)]]

        two = [[Tile(1), Tile(4), Tile(2), Tile(1)],
               [Tile(2), Tile(4), Tile(2), Tile(1)],
               [Tile(3), Tile(5), Tile(3), Tile(1)],
               [Tile(4), Tile(5), Tile(3), Tile(1)]]

        two = [[Tile(4), Tile(5), Tile(3), Tile(1)],
               [Tile(3), Tile(5), Tile(3), Tile(1)],
               [Tile(2), Tile(4), Tile(2), Tile(1)],
               [Tile(1), Tile(4), Tile(2), Tile(1)]]

        three = [[Tile(1), Tile(2), Tile(3), Tile(4)],
                 [Tile(4), Tile(4), Tile(5), Tile(5)],
                 [Tile(2), Tile(2), Tile(3), Tile(3)],
                 [Tile(1), Tile(1), Tile(1), Tile(1)]]

        self.assertTrue(board_assert_eq(g.rotate(to_rotate, 0), to_rotate))
        self.assertTrue(board_assert_eq(g.rotate(to_rotate, 1), one))
        self.assertTrue(board_assert_eq(g.rotate(to_rotate, 2), two))
        # self.assertTrue(board_assert_eq(g.rotate(to_rotate, 3), three))

    def test_move_right(self):
        g = _2048()
        board = [[Tile(1), Tile(2), Tile(3), Tile(4)],
                 [Tile(4), Tile(4), Tile(5), Tile(5)],
                 [Tile(2), Tile(2), Tile(3), Tile(3)],
                 [Tile(1), Tile(1), Tile(1), Tile(1)]]
        state = Bunch(to_move=0, utility=0, board=board)

        new = g.make_move(copy.deepcopy(state), 1)

        solution = [[Tile(1), Tile(2), Tile(3), Tile(4)],
                    [Tile(), Tile(), Tile(5), Tile(6)],
                    [Tile(), Tile(), Tile(3), Tile(4)],
                    [Tile(), Tile(), Tile(2), Tile(2)]]

        not_true = board_assert_eq(state.board, new.board)

        self.assertFalse(not_true)
        self.assertTrue(board_assert_eq(solution, new.board))

    def test_move_down(self):
        g = _2048()
        board = [[Tile(1), Tile(1), Tile(3), Tile(1)],
                 [Tile(1), Tile(1), Tile(3), Tile(1)],
                 [Tile(2), Tile(1), Tile(2), Tile(1)],
                 [Tile(2), Tile(1), Tile(2), Tile(1)]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.make_move(copy.deepcopy(state), 0)

        solution = [[Tile(), Tile(), Tile(), Tile()],
                    [Tile(), Tile(), Tile(), Tile()],
                    [Tile(2), Tile(2), Tile(4), Tile(2)],
                    [Tile(3), Tile(2), Tile(3), Tile(2)]]

        self.assertTrue(board_assert_eq(solution, new.board))

    def test_move_up(self):
        g = _2048()
        board = [[Tile(1), Tile(1), Tile(3), Tile(1)],
                 [Tile(1), Tile(1), Tile(3), Tile(1)],
                 [Tile(2), Tile(1), Tile(2), Tile(1)],
                 [Tile(2), Tile(1), Tile(2), Tile(1)]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.make_move(copy.deepcopy(state), 2)

        solution = [[Tile(2), Tile(2), Tile(4), Tile(2)],
                    [Tile(3), Tile(2), Tile(3), Tile(2)],
                    [Tile(), Tile(), Tile(), Tile()],
                    [Tile(), Tile(), Tile(), Tile()]]

        self.assertTrue(board_assert_eq(solution, new.board))

    def test_move_left(self):
        g = _2048()
        board = [[Tile(1), Tile(2), Tile(3), Tile(4)],
                 [Tile(4), Tile(4), Tile(5), Tile(5)],
                 [Tile(2), Tile(2), Tile(3), Tile(3)],
                 [Tile(1), Tile(1), Tile(1), Tile(1)]]

        state = Bunch(to_move=0, utility=0, board=board)
        new = g.make_move(copy.deepcopy(state), 3)

        solution = [[Tile(1), Tile(2), Tile(3), Tile(4)],
                    [Tile(5), Tile(6), Tile(), Tile()],
                    [Tile(3), Tile(4), Tile(), Tile()],
                    [Tile(2), Tile(2), Tile(), Tile()]]

        self.assertTrue(board_assert_eq(solution, new.board))


if __name__ == '__main__':
    unittest.main()
