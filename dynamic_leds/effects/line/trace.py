from ...models.led import LEDArray
from math import ceil

name = 'Trace'

colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]

# Vars
frame = 0
color_index = 0
led_index = 0

tail_length = 5
speedup = 0.5

def setup(leds: LEDArray):
    pass

def draw(leds: LEDArray):
    global frame, led_index, color_index, tail_length, speedup
    
    frame += 1
    
    if frame % ceil((1/speedup)) == 0:
        # Increment led index
        led_index += 1
        if led_index == leds.count:
            leds.clear()
            led_index = 0
            color_index = (color_index + 1) % len(colors)

        # Set next led to color
        leds[led_index] = colors[color_index]

        # Remove colour from end of tail
        tail_index = led_index - tail_length
        if tail_index > 0:
            leds[tail_index] = (0, 0, 0)

    