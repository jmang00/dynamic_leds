
import board
import neopixel
from time import sleep
from abc import ABC, abstractmethod


"""
An abstract class for an array of LEDs.

These methods are designed to happen instantly.
"""
class LEDArray(ABC):
    @abstractmethod
    def __init__(self, config):
        self.count = config['NO_LEDS']
        self.brightness = config['BRIGHTNESS']
    
    def __len__(self):
        return self.count
    
    @abstractmethod
    def __getitem__(self, index):
        """ Gets the color of a single LED. """
        pass
    
    @abstractmethod
    def __setitem__(self, index, color):
        """ Sets the color of a single LED."""
        pass
    
    @abstractmethod
    def fill(self, colors):
        """ Fills the LED array with a single color. """
        pass
    
    @abstractmethod
    def set(self, colors):
        """ Sets the color of the whole LED array. """
        pass

    def get_brightness(self, brightness):
        """ Returns the brightness of the LED array."""
        return self.brightness
    
    @abstractmethod
    def set_brightness(self, brightness):
        """ Sets the brightness of the LED array. """
        pass
    
    def set_all_off(self):
        self.fill((0, 0, 0))
        self.show()
        sleep(0.01)
    
    def set_all_white(self):
        self.fill((255, 255, 255))
        self.show()
        sleep(0.01)

    def basic_cycle(self):
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

    
class LocalLEDArray:
    PIXEL_PIN = board.D18
    PIXEL_ORDER = neopixel.GRB

    def __init__(self, config):
        super().__init__(config)
        self.leds = neopixel.NeoPixel(
            self.PIXEL_PIN,
            self.count,
            brightness=self.brightness,
            auto_write=False,
            pixel_order=self.PIXEL_ORDER
        )
    
    def __len__(self):
        return self.count

    def __getitem__(self, index):
        return self.leds[index]

    def __setitem__(self, index, color):
        self.leds[index] = color

    def fill(self, color):
        self.leds.fill(color)
        
    def show(self):
        self.leds.show()

    def set_brightness(self, brightness):
        """
        Set the brightness of the LEDs.
        """
        self.leds.brightness = brightness
        self.brightness = brightness

        
"""
A local array of LEDs. This is really just a wrapper class for Neopixel's led library.
"""
class LocalLEDArray:
    PIXEL_PIN = board.D18
    PIXEL_ORDER = neopixel.GRB

    def __init__(self, config):
        super().__init__(config['NO_LEDS'], config['BRIGHTNESS'])
        self.leds = neopixel.NeoPixel(
            self.PIXEL_PIN,
            config['NO_LEDS'],
            brightness=config['BRIGHTNESS'],
            auto_write=True,
            pixel_order=self.PIXEL_ORDER
        )

    def __getitem__(self, index):
        return self.leds[index]

    def __setitem__(self, index, value):
        self.leds[index] = value

    def fill(self, color):
        self.leds.fill(color)
        
    def show(self):
        self.leds.show()

    def set_brightness(self, brightness):
        """
        Set the brightness of the LEDs.
        """
        self.leds.brightness = brightness
        self.brightness = brightness


# """ A remote LED Array that reponds to OPC UA commands"""        
        
# class OPCUALEDArray:
#     def __init__(self, config):
#         super().__init__(config)
        
#         # Initialise an empty array of LED values
#         self.leds = [(0,0,0)] * self.count
        
#         # Connect to the OPCUA server
#         # self.client = Client("opc.tcp://localhost:4840/freeopcua/server/")
#         # self.client.connect()
#         # self.node = self.client.get_objects_node()
#         # self.leds = self.node.get_child(["0:Objects", "2:LEDs"])

#     def __getitem__(self, index):
#         return self.leds.get_child(["0:Objects", f"2:LEDs.{index}"])

#     def __setitem__(self, index, value):
#         self.leds.get_child(["0:Objects", f"2:LEDs.{index}"]).set_value(value)

#     def fill(self, color):
#         for i in range(len(self)):
#             self[i].set_value(color)
#         self.show()
        
#     def show(self):
#         """ Writes the updated values to the OPCUA server."""
        
#     def set_brightness(self, brightness):
#         """ Sets the brightness variable in OPCUA. """
#         for i in range(len(self)):
#             self[i].set_brightness(brightness)
#         self.brightness = brightness
