from src.cfgrid import Grid


class TestGrid:

    def test_horizontal_win_positive(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 1, 0, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_horizontal(1, 1) == [(1, 1), (2, 1), (3, 1), (4, 1)]

    def test_horizontal_win_negative(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 1, 0, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_horizontal(2, 2) == []

    def test_vertical_win_positive(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 2, 0, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 1, 2, 2, 2, 2],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_vertical(4, 2) == [(4, 2), (4, 3), (4, 4), (4, 5)]

    def test_vertical_win_negative(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 2, 0, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 1, 2, 2, 2, 2],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_vertical(0, 1) == []

    # Bottom-up, left-right 1
    def test_diagonal_win_positive_1(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 2, 0, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 1, 2, 2, 0, 0],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_diagonal(3, 2, 2) == [(1, 0), (2, 1), (3, 2), (4, 3)]

    # Bottom-up, left-right 2
    def test_diagonal_win_positive_2(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 2, 0, 0, 0, 0],
                     [1, 1, 2, 0, 0, 0],
                     [1, 1, 2, 1, 0, 0],
                     [2, 2, 1, 0, 0, 0],
                     [1, 2, 1, 1, 0, 0]]
        assert grid.check_diagonal(4, 1, 1) == [(3, 0), (4, 1), (5, 2), (6, 3)]

    # Bottom-up, right-left
    def test_diagonal_win_positive_3(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 2, 1, 2, 0],
                     [1, 2, 1, 2, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 2, 2, 1, 0, 0],
                     [1, 2, 1, 0, 0, 0],
                     [1, 2, 1, 1, 0, 0]]
        assert grid.check_diagonal(2, 3, 2) == [(4, 1), (3, 2), (2, 3), (1, 4)]

    # Bottom-up, right-left
    def test_diagonal_win_positive_4(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 2, 1, 2, 0],
                     [1, 2, 1, 2, 0, 0],
                     [2, 1, 1, 0, 0, 0],
                     [1, 2, 2, 1, 0, 0],
                     [1, 2, 1, 0, 1, 0],
                     [1, 2, 1, 1, 0, 1]]
        assert grid.check_diagonal(6, 5, 1) == [(3, 2), (4, 3), (5, 4), (6, 5)]

    # Bottom-up, right-left
    def test_diagonal_win_positive_5(self):
        grid = Grid()
        grid.grid = [[1, 1, 1, 1, 0, 0],
                     [2, 1, 2, 2, 2, 0],
                     [1, 2, 1, 2, 0, 0],
                     [2, 1, 1, 1, 2, 1],
                     [1, 2, 2, 1, 1, 0],
                     [1, 2, 1, 1, 1, 0],
                     [1, 2, 1, 1, 0, 1]]
        assert grid.check_diagonal(3, 5, 1) == [(6, 2), (5, 3), (4, 4), (3, 5)]

    # Bottom-up, right-left
    def test_diagonal_win_positive_6(self):
        grid = Grid()
        grid.grid = [[1, 1, 1, 2, 0, 0],
                     [2, 1, 2, 2, 2, 0],
                     [1, 2, 1, 2, 0, 0],
                     [2, 1, 1, 1, 0, 0],
                     [1, 2, 2, 1, 0, 0],
                     [1, 2, 1, 0, 0, 0],
                     [1, 2, 1, 0, 0, 1]]
        assert grid.check_diagonal(3, 0, 2) == [(3, 0), (2, 1), (1, 2), (0, 3)]

    def test_diagonal_win_negative_1(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 1, 0, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [2, 1, 2, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_diagonal(3, 2, 1) == []

    def test_diagonal_win_negative_2(self):
        grid = Grid()
        grid.grid = [[1, 2, 1, 1, 0, 0],
                     [2, 1, 0, 0, 0, 0],
                     [1, 1, 0, 0, 0, 0],
                     [2, 1, 2, 1, 2, 1],
                     [2, 1, 2, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        assert grid.check_diagonal(3, 5, 1) == []
