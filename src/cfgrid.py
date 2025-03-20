ROWS = 6
COLUMNS = 7


class ColumnFull(Exception):
    pass


class Grid():
    def __init__(self, rows: int = ROWS, columns: int = COLUMNS):
        self.rows = rows
        self.columns = columns
        self.grid = [[0 for _ in range(rows)] for _ in range(columns)]

    def __str__(self) -> str:
        return '\n'.join([' '.join([str(self.grid[column][row])
                                    for column in range(self.columns)])
                          for row in range(self.rows - 1, -1, -1)])

    def drop_in_column(self, column: int, player: int) -> int:
        if column < 0 or column >= self.columns:
            raise IndexError
        try:
            first_free = self.grid[column].index(0)
        except ValueError:
            raise ColumnFull
        self.grid[column][first_free] = player
        return first_free

    def check_win(self, column: int, row: int, player: int) -> list[tuple[int, int]]:
        result = self.check_generic(self.generate_vertical(column), player)
        if result:
            return result
        result = self.check_generic(self.generate_horizontal(row), player)
        if result:
            return result
        result = self.check_generic(self.generate_diagonal_leftright(column, row), player)
        if result:
            return result
        result = self.check_generic(self.generate_diagonal_rightleft(column, row), player)
        if result:
            return result
        return []

    def check_generic(self, gen, player):
        count = 0
        cells = []
        win = False
        for c, r in gen:
            if self.grid[c][r] == player:
                count += 1
                cells.append((c, r))
                if count >= 4:
                    win = True
            else:
                if win:
                    break
                count = 0
                cells = []
        if not win:
            cells = []
        return cells

    def generate_vertical(self, column: int):
        for row in range(self.rows):
            yield (column, row)

    def generate_horizontal(self, row: int):
        for column in range(self.columns):
            yield (column, row)

    def generate_diagonal_leftright(self, column: int, row: int):
        start_offset = -min(row, column)  # Left boundary
        end_offset = min(self.rows - row, self.columns - column)  # Right boundary
        for offset in range(start_offset, end_offset):
            yield (column + offset, row + offset)

    def generate_diagonal_rightleft(self, column: int, row: int):
        start_offset = -min(row, self.columns - column - 1)  # Right boundary
        end_offset = min(self.rows - row, column + 1)  # Left boundary
        for offset in range(start_offset, end_offset):
            yield (column - offset, row + offset)
