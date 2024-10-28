from abc import ABC, abstractmethod
import time


class Effect(ABC):
    def __init__(self, leds, positions, fps=60):
        self.leds = leds
        self.positions = positions
        self.fps = fps

    def run(self):
        self.leds.set_all_off()
        self.setup()

        try:
            while True:
                self.draw()
                self.leds.show()
                time.sleep(1 / self.fps)

        except:
            self.leds.set_all_off()
            raise

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def draw(self):
        pass