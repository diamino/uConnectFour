# uConnectFour

MicroPython version of the Connect Four ('Vier Op Een Rij' in Dutch) game.

## Requirements

* MicroPython (tested on v1.24.1 on Raspberry Pi Pico)
* neopixel python module (included in RP2 build)

* Neopixel (WS2812B) LED matrix (tested on 8x8)
* Joystick module (KY-023)

## Usage

Copy all the files in the `src` directory to the MicroPython filesystem. Rename the `src/connectfour.py` file to `main.py`.

Make sure to set the `Pin` values to the correct pins used for the Neopixel matrix and the joystick.  
