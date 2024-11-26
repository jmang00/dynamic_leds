""" A basic template to follow for creating a 2D effect. """

name = 'Effect Name'

duration = 10
fps = 30

def setup(leds: LEDArray):
    # VSCode Tip: Ctrl+Click on 'LEDArray' above to go to the class definition
    pass

def draw(leds: LEDArray):
    global duration, fps

    for i in range(len(leds)):

        # Set the colour
        leds[i] = (255, 255, 255)
        
        leds[(i-2) % leds.count] = (0,0,0)
        sleep(0.1)
        
        leds.show()
