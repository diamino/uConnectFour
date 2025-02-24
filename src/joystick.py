'''
Simple MicroPython module for KY-023 joystick modules
'''
from machine import Pin, ADC

CENTER = 0
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


class Joystick():

    def __init__(self, vadc_pin: int, hadc_pin: int, sw_pin: int):
        self.vadc = ADC(Pin(vadc_pin))
        self.hadc = ADC(Pin(hadc_pin))
        self.sw = Pin(sw_pin, Pin.IN, pull=Pin.PULL_UP)
        self.sw.irq(self._sw_down_handler, trigger=Pin.IRQ_FALLING)
        self.sw_down = False

    def _sw_down_handler(self, _: Pin) -> None:
        self.sw_down = True

    def is_sw_down(self) -> bool:
        value = self.sw_down
        self.sw_down = False
        return value

    def _sample_vadc(self) -> int:
        return self.vadc.read_u16()

    def _sample_hadc(self) -> int:
        return self.hadc.read_u16()

    def vertical_position(self) -> int:
        value = self._sample_vadc()
        pos = CENTER
        if value < 5000:
            pos = DOWN
        elif value > 60000:
            pos = UP
        return pos

    def horizontal_position(self) -> int:
        value = self._sample_hadc()
        pos = CENTER
        if value < 5000:
            pos = LEFT
        elif value > 60000:
            pos = RIGHT
        return pos
