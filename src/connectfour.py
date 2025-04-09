import time
from machine import Pin
from neopixel import NeoPixel
import framebuf
import neopixelmatrix as npm
from joystick import Joystick, LEFT, RIGHT, DOWN
from cfgrid import Grid, ColumnFull

PLAYER_LIST = (1, 2)

JS_PIN_HOR = 26
JS_PIN_VER = 27
JS_PIN_BTN = 16

DISP_HEIGHT = 8
DISP_WIDTH = 8
DISP_BRIGHTNESS = 0.05
NO_LEDS = DISP_HEIGHT * DISP_WIDTH  # 8x8 LED matrix
DATA_PIN = 0  # Pin used for NeoPixels
OFFSET = (0, 2)  # Offset (x,y) of the grid on the display

PURPLE_565 = npm.rgb888_to_565(npm.PURPLE)
GREEN_565 = npm.rgb888_to_565(npm.GREEN)
BLUE_565 = npm.rgb888_to_565(npm.BLUE)
YELLOW_565 = npm.rgb888_to_565(npm.YELLOW)
GREY_565 = npm.rgb888_to_565((25, 25, 25))

PALETTE = [0, PURPLE_565, GREEN_565, BLUE_565, YELLOW_565]
BG_COLOR = GREY_565


def grid_to_framebuffer(grid: list[list[int]],
                        fb: framebuf.FrameBuffer,
                        offset: tuple[int, int],
                        palette: list[int],
                        bg: int = 0) -> None:
    """
    Draws a grid to a framebuffer.
    :param grid: Grid to draw
    :param fb: Framebuffer to draw to
    :param offset: Offset (x,y) of the grid on the display
    :param palette: Palette of colors (RGB565 format) to use
    :param bg: Background color (in RGB565 format)
    """
    # Erase area for grid
    fb.rect(offset[0], offset[1], len(grid), len(grid[0]), bg, True)
    num_rows = len(grid[0])
    for row in range(num_rows):
        for column in range(len(grid)):
            value = grid[column][num_rows - row - 1]
            if value != 0:
                fb.pixel(column + offset[0], row + offset[1], palette[value])


def main() -> None:
    grid = Grid()
    np = NeoPixel(Pin(DATA_PIN), NO_LEDS)
    display = npm.NeoPixelMatrix(np, DISP_WIDTH, DISP_HEIGHT, brightness=DISP_BRIGHTNESS)
    j = Joystick(JS_PIN_VER, JS_PIN_HOR, JS_PIN_BTN)

    active_column = grid.columns // 2
    active_player = PLAYER_LIST[0]

    display.pixel(active_column, 0, PALETTE[active_player])
    grid_to_framebuffer(grid.grid, display, OFFSET, PALETTE, bg=BG_COLOR)
    display.show()

    while True:
        time.sleep_ms(250)
        hpos = j.horizontal_position()
        vpos = j.vertical_position()
        if hpos == LEFT and active_column > 0:
            display.pixel(active_column, 0, 0)
            active_column -= 1
            display.pixel(active_column, 0, PALETTE[active_player])
            display.show()
        elif hpos == RIGHT and active_column < (grid.columns - 1):
            display.pixel(active_column, 0, 0)
            active_column += 1
            display.pixel(active_column, 0, PALETTE[active_player])
            display.show()
        # if j.is_sw_down():
        if vpos == DOWN:
            try:
                row = grid.drop_in_column(active_column, active_player)
                grid_to_framebuffer(grid.grid, display, OFFSET, PALETTE, bg=BG_COLOR)
                display.pixel(active_column, 0, 0)
                win = grid.check_win(active_column, row, active_player)
                if win:
                    print(f"ConnectFour! Player {active_player} wins")
                    display.show()
                    for _ in range(10):
                        for cell in win:
                            display.pixel(cell[0] + OFFSET[0], DISP_HEIGHT - cell[1] - OFFSET[1] + 1, BG_COLOR)
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
                    display.pixel(active_column, 0, PALETTE[active_player])
                display.show()
            except ColumnFull:
                print("Column full")
            time.sleep(1)


if __name__ == "__main__":
    main()
