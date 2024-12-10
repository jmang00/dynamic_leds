# A basic example using the dynamic leds library
# To run this script, enter into the terminal:
# sudo -E python basic_dynamic.py

from dynamic_leds.dynamic_leds import DynamicLeds
from time import sleep

dl = DynamicLeds()

dl.load_scene('line')

l = dl.scene.leds

while True:
    l.basic_cycle()