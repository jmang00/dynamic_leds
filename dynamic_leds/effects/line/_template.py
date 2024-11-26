""" A basic template to follow for creating an effect. """
from ...models.led import LEDArray

# The name of the effect
name = 'Effect Name'

# The frame rate
fps = 30

# The setup function. This is called once at the start of your sketch.
def setup(leds: LEDArray):
    pass

# The draw function. This is called once per frame.
def draw(leds: LEDArray):
    pass
