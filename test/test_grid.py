from connectfour import Grid


class TestGrid:

    def test_horizontal_win(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 1, 0, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_horizontal(1, 1) == [(1, 1), (2, 1), (3, 1), (4, 1)]

    def test_vertical_win(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 2, 0, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 1, 2, 2, 2, 2],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_vertical(4, 2) == [(4, 2), (4, 3), (4, 4), (4, 5)]
