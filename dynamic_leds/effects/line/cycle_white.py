from ...models.led import LEDArray
from time import sleep

name = 'Simple Line'
fps = 30

def setup(leds: LEDArray):
    pass

def draw(leds: LEDArray):
    for i in range(len(leds)):

        # Set the colour
        leds[i] = (255, 255, 255)
        
        leds[(i-2) % leds.count] = (0,0,0)
        sleep(0.1)
        
        leds.show()
