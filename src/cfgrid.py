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
        result = self.check_vertical(column, player)
        if result:
            return result
        result = self.check_horizontal(row, player)
        if result:
            return result
        result = self.check_diagonal(column, row, player)
        if result:
            return result
        return []

    def check_vertical(self, column: int, player: int) -> list[tuple[int, int]]:
        count = 0
        cells = []
        win = False
        for r in range(self.rows):
            if self.grid[column][r] == player:
                count += 1
                cells.append((column, r))
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

    def check_horizontal(self, row: int, player: int) -> list[tuple[int, int]]:
        count = 0
        cells = []
        win = False
        for c in range(self.columns):
            if self.grid[c][row] == player:
                count += 1
                cells.append((c, row))
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

    def check_diagonal(self, column: int, row: int, player: int) -> list[tuple[int, int]]:
        # Check bottom-up, left-right
        count = 0
        cells = []
        win = False
        start_offset = -min(row, column)  # Left boundary
        end_offset = min(self.rows - row, self.columns - column)  # Right boundary
        for offset in range(start_offset, end_offset):
            if self.grid[column + offset][row + offset] == player:
                count += 1
                cells.append((column + offset, row + offset))
                if count >= 4:
                    win = True
            else:
                if win:
                    break
                cells = []
                count = 0
        if win:
            return cells
        # Check bottom-up, right-left
        count = 0
        cells = []
        start_offset = -min(row, self.columns - column - 1)  # Right boundary
        end_offset = min(self.rows - row, column + 1)  # Left boundary
        # print(f"{start_offset=}  {end_offset=}")
        for offset in range(start_offset, end_offset):
            # print(f"Checking c={column - offset} r={row + offset}")
            if self.grid[column - offset][row + offset] == player:
                count += 1
                cells.append((column - offset, row + offset))
                if count >= 4:
                    win = True
            else:
                if win:
                    break
                cells = []
                count = 0
        if not win:
            cells = []
        return cells
