
import board
import neopixel
import time

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

    def set_all_off(self):
        self.leds.fill((0, 0, 0))
        self.leds.show()
        time.sleep(0.01)

    def set_all_white(self):
        self.leds.fill((255, 255, 255))
        self.leds.show()
        time.sleep(0.01)

    def basic_cycle(self):
        self.leds.fill((255, 255, 255))
        self.leds.show()
        time.sleep(2)
        self.leds.fill((255, 0, 0))
        self.leds.show()
        time.sleep(0.5)
        self.leds.fill((0, 255, 0))
        self.leds.show()
        time.sleep(0.5)
        self.leds.fill((0, 0, 255))
        self.leds.show()
        time.sleep(0.5)
