from time import sleep
import numpy as np
from dynamic_leds import DynamicLeds

dl = DynamicLeds()
dl.load_scene('automation-tree')

s = dl.scene
l = dl.scene.leds
p = dl.scene.led_positions

print('''
Variables Available:
- dl: DynamicLeds object
- s: Scene object
- l: LEDArray object
- p: LED positions (numpy array)
''')