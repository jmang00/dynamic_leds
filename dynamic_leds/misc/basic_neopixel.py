# A basic example using the neopixel library
# To run this script, enter into the terminal:
# sudo -E python basic_neopixel.py

import board
import neopixel
from time import sleep

leds = neopixel.NeoPixel(board.D18, 500, brightness=0.3, auto_write=True, pixel_order=neopixel.GRB)

leds.fill((255,0,0))