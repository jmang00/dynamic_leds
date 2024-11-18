from ...util.color import get_color_in_sequence, inbetween_color

name = 'Rainbow Wave'


full_rgb_cycle_colors_gaps = [(255, 0, 0), (0,0,0), (0,0,0), (255, 255, 0), (0,0,0), (0,0,0), (0, 255, 0), (0,0,0), (0,0,0), (0, 255, 255), (0,0,0), (0,0,0), (0, 0, 255), (0,0,0), (0,0,0),  (255, 0, 255)]
progress = 0
duration = 10
fps = 30

def setup(leds):
    pass

def draw(leds):
    global progress, duration, fps
    global full_rgb_cycle_colors_gaps
    
    colors = full_rgb_cycle_colors_gaps
    
    for i in range(len(leds)):
        # p is the increase in progress for the current pixel
        p = i / len(leds)
        
        # Calculate the color
        color = get_color_in_sequence(
            colors,
            (progress + p) % 1
        )

        # Set the colour
        leds[i] = color
    
    leds.show()

    # Increment the effect progress
    progress += 1 / (duration * fps)