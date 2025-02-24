'''
Module to use a NeoPixel as a frame buffer.
'''
from neopixel import NeoPixel
import framebuf

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)


def rgb888_to_565(color: tuple[int, int, int]) -> int:
    return ((color[0] & 0xF8) << 8) | ((color[1] & 0xFC) << 3) | ((color[2] & 0xF8) >> 3)


def rgb565_to_888(color: int) -> tuple[int, int, int]:
    red = (color >> 8) & 0xF8
    green = (color >> 3) & 0xFC
    blue = (color << 3) & 0xF8
    return (red, green, blue)


def set_brightness(color: tuple[int, int, int], brightness: float) -> tuple[int, int, int]:
    return (int(color[0] * brightness),
            int(color[1] * brightness),
            int(color[2] * brightness))


class NeoPixelMatrix(framebuf.FrameBuffer):

    def __init__(self, np: NeoPixel, width: int, height: int, brightness: float = 1.0):
        self.np = np
        self.width = width
        self.height = height
        self.brightness = brightness
        self.buffer = bytearray(width * height * 2)
        super().__init__(self.buffer, width, height, framebuf.RGB565)

    def show(self) -> None:
        for i in range(self.width * self.height):
            if (i // self.width) % 2:
                i_prime = i
            else:
                r = i % self.width
                i_prime = i - 1 - (r << 1) + self.width
            self.np[i_prime] = set_brightness(rgb565_to_888(self.buffer[(i << 1)+1] << 8 | self.buffer[i << 1]), self.brightness)
        self.np.write()
