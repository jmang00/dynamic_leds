
import board
import neopixel
from time import sleep
"""
An array of LEDs. This is really just a wrapper class for Neopixel's led library.
"""
class LEDArray:
    PIXEL_PIN = board.D18
    PIXEL_ORDER = neopixel.GRB

    def __init__(self, config):
        self.count = config['NO_LEDS']
        self.brightness = config['BRIGHTNESS']
        self.leds = neopixel.NeoPixel(
            self.PIXEL_PIN,
            config['NO_LEDS'],
            brightness=config['BRIGHTNESS'],
            auto_write=False,
            pixel_order=self.PIXEL_ORDER
        )
    
    def __len__(self):
        return self.count

    def __getitem__(self, index):
        return self.leds[index]

    def __setitem__(self, index, value):
        self.leds[index] = value

    def fill(self, color):
        self.leds.fill(color)
        self.leds.show()
        
    def show(self):
        self.leds.show()

    def set_brightness(self, brightness):
        """
        Set the brightness of the LEDs.
        """
        self.leds.brightness = brightness
        self.brightness = brightness
        self.leds.show()

    def clear(self):
        self.leds.fill((0, 0, 0))

    def white(self):
        self.leds.fill((255, 255, 255))

    def test_cycle(self):
        self.fill((255, 255, 255))
        self.show()
        sleep(2)
        self.fill((255, 0, 0))
        self.show()
        sleep(0.5)
        self.fill((0, 255, 0))
        self.show()
        sleep(0.5)
        self.fill((0, 0, 255))
        self.show()
        sleep(0.5)
