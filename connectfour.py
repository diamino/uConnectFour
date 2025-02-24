from machine import Pin
from neopixel import NeoPixel
import neopixelmatrix as npm
from joystick import Joystick, LEFT, RIGHT, DOWN
import framebuf
import time

PURPLE_565 = npm.rgb888_to_565(npm.PURPLE)
GREEN_565 = npm.rgb888_to_565(npm.GREEN)
WHITE_565 = 0xFFFF

ROWS = 6
COLUMNS = 7
PLAYER_LIST = (1, 2)


class ColumnFull(Exception):
    pass


class Grid():
    def __init__(self, rows: int = ROWS, columns: int = COLUMNS):
        self.grid = [[0 for _ in range(rows)] for _ in range(columns)]

    def __str__(self) -> str:
        return '\n'.join([' '.join([str(self.grid[column][row]) for column in range(COLUMNS)]) for row in range(ROWS - 1, -1, -1)])

    def drop_in_column(self, column: int, player: int) -> int:
        if column < 0 or column >= COLUMNS:
            raise IndexError
        try:
            first_free = self.grid[column].index(0)
        except ValueError:
            raise ColumnFull
        self.grid[column][first_free] = player
        return first_free

    def check_vertical(self, column: int, player: int) -> list[tuple[int, int]]:
        count = 0
        cells = []
        for r in self.grid[column]:
            if r == player:
                count += 1
                cells.append((column, r))
                if count >= 4:
                    return cells
            else:
                count = 0
        return []

    def check_horizontal(self, row: int, player: int) -> list[tuple[int, int]]:
        count = 0
        cells = []
        for c in self.grid:
            if c[row] == player:
                count += 1
                cells.append((c, row))
                if count >= 4:
                    return cells
            else:
                count = 0
        return []

    def check_diagonal(self, row: int, column: int, player: int) -> bool:
        ...


def grid_to_framebuffer(grid: list[list[int]], fb: framebuf.FrameBuffer, offset: tuple[int, int], palette: list[int]) -> None:
    # Erase area for grid
    fb.rect(offset[0], offset[1], len(grid), len(grid[0]), 0, True)
    num_rows = len(grid[0])
    for row in range(num_rows):
        for column in range(len(grid)):
            fb.pixel(column + offset[0], row + offset[1], palette[grid[column][num_rows - row - 1]])


def main() -> None:
    DISP_HEIGHT = 8
    DISP_WIDTH = 8
    NO_LEDS = DISP_HEIGHT * DISP_WIDTH  # 8x8 LED matrix
    DATA_PIN = 0
    PALETTE = [0, PURPLE_565, GREEN_565]

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
                grid_to_framebuffer(grid.grid, display, (0, 2), PALETTE)
                if grid.check_vertical(pixel_pos, active_player):
                    print("COnnectFour vertical!")
                    display.show()
                    break
                elif grid.check_horizontal(row, active_player):
                    print("ConnectFour horizontal!")
                    display.show()
                    break
                else:
                    active_player = PLAYER_LIST[(PLAYER_LIST.index(active_player) + 1) % len(PLAYER_LIST)]
                    display.pixel(pixel_pos, 0, PALETTE[active_player])
                display.show()
            except ColumnFull:
                print("Column full")


if __name__ == "__main__":
    main()
