from ...models.led import LEDArray
from ...util.color import get_color_in_sequence, inbetween_color, color_input
from time import sleep

name = 'Simple Line'
fps = 30

duration = 10

def setup(leds: LEDArray):
    pass

def draw(leds: LEDArray):
    while True:
        led_index = input(f'Enter an LED index (0-{leds.count-1}): ')
        
        try:
            n = int(led_index)
            assert 0 <= n <= leds.count - 1
            
            if leds[n] == (255, 255, 255):
                leds[n] = (0, 0, 0)
            else:
                leds[n] = (255, 255, 255)
            leds.show()
        except (ValueError,AssertionError):
            print('Please enter a valid index')

    
