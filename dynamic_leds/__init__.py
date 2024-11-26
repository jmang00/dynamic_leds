"""
The main interface for the dynamic_leds module.

Currently only supports a single scene.

"""

from dynamic_leds.models.effect import Effect
from dynamic_leds.models.scene import Scene


class DynamicLeds:
    def __init__(self):
        self.scene = None

    def load_scene(self, scene_name: str):
        self.scene = Scene(scene_name)

    def scan(self):
        self.scene.scan()

    def run(self, effect: Effect):
        self.scene.run(effect)

    def off(self):
        self.scene.leds.set_all_off()

