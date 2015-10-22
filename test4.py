import unittest
from modul4.gamelogic import _2048, Tile
from algorithms.utils import Bunch
import copy


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

        self.assertEqual(g.rotate(to_rotate, 0), to_rotate)
        self.assertEqual(g.rotate(to_rotate, 1), one)
        self.assertEqual(g.rotate(to_rotate, 2), two)
        self.assertEqual(g.rotate(to_rotate, 3), three)

    def test_move_right(self):
        g = _2048()
        board = [[Tile() for _ in range(4)] for _ in range(4)]
        board[0][0] = Tile(2)
        board[0][1] = Tile(2)
        board[1][0] = Tile(3)
        board[1][1] = Tile(3)
        board[2][0] = Tile(1)
        board[2][1] = Tile(1)
        board[3][0] = Tile()
        board[3][1] = Tile(1)
        state = Bunch(to_move=0, utility=0, board=board)
        print(state.board)
        new = g.make_move(3, copy.deepcopy(state))
        print(new.board)

        solution = [[Tile(3), Tile(), Tile(), Tile()],
                    [Tile(4), Tile(), Tile(), Tile()],
                    [Tile(2), Tile(), Tile(), Tile()],
                    [Tile(1), Tile(), Tile(), Tile()]]

        self.assertNotEqual(state.board, new.board)
        self.assertEqual(solution, new.board)

    def test_move_down(self):
        g = _2048()
        board = [[Tile(1), Tile(1), Tile(3), Tile(1)],
                 [Tile(1), Tile(1), Tile(3), Tile(1)],
                 [Tile(2), Tile(1), Tile(2), Tile(1)],
                 [Tile(2), Tile(1), Tile(2), Tile(1)]]

        state = Bunch(to_move=0, utility=0, board=board)
        print(state.board)
        new = g.make_move(0, copy.deepcopy(state))
        print(new.board)

        solution = [[Tile(), Tile(), Tile(), Tile()],
                    [Tile(), Tile(), Tile(), Tile()],
                    [Tile(2), Tile(2), Tile(4), Tile(2)],
                    [Tile(3), Tile(2), Tile(3), Tile(2)]]

        self.assertEqual(new.board, solution)


if __name__ == '__main__':
    unittest.main()
