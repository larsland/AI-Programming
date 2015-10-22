import unittest
from gui import GameWindow


class TestGameLogic(unittest.TestCase):

    def test_move_right(self):
        move = GameWindow.move
        self.check_if_lost = lambda: False
        self.rotate = GameWindow.rotate

        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.board[0][0] = 1
        self.board[0][1] = 1
        print(self.board)
        move(self, -1)
        print(self.board)

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
