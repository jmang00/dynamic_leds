import board
import neopixel
import time

from run import *


# Function to smoothly transition from one color to another
def color_transition(color1, color2, steps):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    color_list = []
    for step in range(steps):
        r = int(r1 + (r2 - r1) * step / steps)
        g = int(g1 + (g2 - g1) * step / steps)
        b = int(b1 + (b2 - b1) * step / steps)
        color_list.append((r, g, b))
    return color_list

# Define a list of colors for the rainbow
rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

# Time (in seconds) for each transition
transition_time = 2


set_all_off()

# Main loop to cycle through the rainbow
while True:
    for i in range(len(rainbow_colors)):
        current_color = rainbow_colors[i]
        next_color = rainbow_colors[(i + 1) % len(rainbow_colors)]
        transition_steps = int(transition_time * 60)  # Adjust this value for desired transition speed
        transition_colors = color_transition(current_color, next_color, transition_steps)
        for color in transition_colors:
            leds.fill(color)
            leds.show()
            time.sleep(1 / 60)  # 60 FPS