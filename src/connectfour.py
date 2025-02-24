ROWS = 6
COLUMNS = 7
PLAYER_LIST = (1, 2)


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
        for r in range(self.rows):
            if self.grid[column][r] == player:
                count += 1
                cells.append((column, r))
                if count >= 4:
                    return cells
            else:
                count = 0
                cells = []
        return []

    def check_horizontal(self, row: int, player: int) -> list[tuple[int, int]]:
        count = 0
        cells = []
        for c in range(self.columns):
            if self.grid[c][row] == player:
                count += 1
                cells.append((c, row))
                if count >= 4:
                    return cells
            else:
                count = 0
                cells = []
        return []

    def check_diagonal(self, column: int, row: int, player: int) -> list[tuple[int, int]]:
        # Check bottom-up, left-right
        count = 0
        cells = []
        start_offset = -min(row, column)  # Left boundary
        end_offset = min(self.rows - row, self.columns - column)  # Right boundary
        for offset in range(start_offset, end_offset):
            if self.grid[column + offset][row + offset] == player:
                count += 1
                cells.append((column + offset, row + offset))
                if count >= 4:
                    return cells
            else:
                cells = []
                count = 0
        # Check bottom-up, right-left
        count = 0
        cells = []
        start_offset = -min(row, self.columns - column - 1)  # Right boundary
        end_offset = min(self.rows - row, column)  # Left boundary
        # print(f"{start_offset=}  {end_offset=}")
        for offset in range(start_offset, end_offset):
            # print(f"Checking c={column - offset} r={row + offset}")
            if self.grid[column - offset][row + offset] == player:
                count += 1
                cells.append((column - offset, row + offset))
                if count >= 4:
                    return cells
            else:
                cells = []
                count = 0
        return []


def main() -> None:
    import time
    from machine import Pin
    from neopixel import NeoPixel
    import neopixelmatrix as npm
    from joystick import Joystick, LEFT, RIGHT, DOWN
    import framebuf

    def grid_to_framebuffer(grid: list[list[int]],
                            fb: framebuf.FrameBuffer,
                            offset: tuple[int, int],
                            palette: list[int]) -> None:
        # Erase area for grid
        fb.rect(offset[0], offset[1], len(grid), len(grid[0]), 0, True)
        num_rows = len(grid[0])
        for row in range(num_rows):
            for column in range(len(grid)):
                fb.pixel(column + offset[0], row + offset[1], palette[grid[column][num_rows - row - 1]])

    PURPLE_565 = npm.rgb888_to_565(npm.PURPLE)
    GREEN_565 = npm.rgb888_to_565(npm.GREEN)
    # WHITE_565 = 0xFFFF

    DISP_HEIGHT = 8
    DISP_WIDTH = 8
    NO_LEDS = DISP_HEIGHT * DISP_WIDTH  # 8x8 LED matrix
    DATA_PIN = 0
    PALETTE = [0, PURPLE_565, GREEN_565]
    OFFSET = (0, 2)

    grid = Grid()
    np = NeoPixel(Pin(DATA_PIN), NO_LEDS)
    display = npm.NeoPixelMatrix(np, DISP_WIDTH, DISP_HEIGHT, brightness=0.05)
    j = Joystick(27, 26, 16)

    pixel_pos = 0
    active_player = PLAYER_LIST[0]

    display.pixel(pixel_pos, 0, PALETTE[active_player])
    display.show()

    while True:
        time.sleep_ms(250)
        hpos = j.horizontal_position()
        vpos = j.vertical_position()
        if hpos == LEFT and pixel_pos > 0:
            display.pixel(pixel_pos, 0, 0)
            pixel_pos -= 1
            display.pixel(pixel_pos, 0, PALETTE[active_player])
            display.show()
        elif hpos == RIGHT and pixel_pos < (COLUMNS - 1):
            display.pixel(pixel_pos, 0, 0)
            pixel_pos += 1
            display.pixel(pixel_pos, 0, PALETTE[active_player])
            display.show()
        # if j.is_sw_down():
        if vpos == DOWN:
            try:
                row = grid.drop_in_column(pixel_pos, active_player)
                grid_to_framebuffer(grid.grid, display, OFFSET, PALETTE)
                win = grid.check_win(pixel_pos, row, active_player)
                if win:
                    print(f"ConnectFour! Player {active_player} wins")
                    display.show()
                    for _ in range(10):
                        for cell in win:
                            display.pixel(cell[0] + OFFSET[0], DISP_HEIGHT - cell[1] - OFFSET[1] + 1, 0)
                        display.show()
                        time.sleep_ms(500)
                        for cell in win:
                            display.pixel(cell[0] + OFFSET[0],
                                          DISP_HEIGHT - cell[1] - OFFSET[1] + 1,
                                          PALETTE[active_player])
                        display.show()
                        time.sleep_ms(500)
                    break
                else:
                    active_player = PLAYER_LIST[(PLAYER_LIST.index(active_player) + 1) % len(PLAYER_LIST)]
                    display.pixel(pixel_pos, 0, PALETTE[active_player])
                display.show()
            except ColumnFull:
                print("Column full")
            time.sleep(1)


if __name__ == "__main__":
    main()
