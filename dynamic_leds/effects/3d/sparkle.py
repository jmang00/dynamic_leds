""" Was supposed to be a rainbow wave through a plane.
Not exactly what I had in mind but it sparkelsa and looks cool.
"""


import numpy as np
from ...models.led import LEDArray
from ...util.color import get_color_in_sequence

name = '3D Rainbow Wave'
fps = 30
duration = 10  # Duration of one full wave cycle in seconds

# The progress of the effect
progress = 0

# Colors for the rainbow sequence with gaps
full_rgb_cycle_colors_gaps = [
    (255, 0, 0), (0, 0, 0), (0, 0, 0), 
    (255, 255, 0), (0, 0, 0), (0, 0, 0), 
    (0, 255, 0), (0, 0, 0), (0, 0, 0), 
    (0, 255, 255), (0, 0, 0), (0, 0, 0), 
    (0, 0, 255), (0, 0, 0), (0, 0, 0), 
    (255, 0, 255)
]

# Plane variables
plane_normal = None
plane_point = None


def setup(leds: LEDArray, positions: np.ndarray):
    """
    Setup the effect, generating a random plane in 3D space.
    """
    global plane_normal, plane_point, led_positions

    led_positions = positions
    
    # Generate a random normal vector for the plane
    plane_normal = np.random.rand(3) - 0.5  # Random direction
    plane_normal /= np.linalg.norm(plane_normal)  # Normalize to unit vector
    
    # Choose a random point on the plane within the bounding box
    min_coords = np.nanmin(led_positions, axis=0)
    max_coords = np.nanmax(led_positions, axis=0)
    plane_point = np.random.uniform(min_coords, max_coords)


def draw(leds: LEDArray):
    """
    Draw the rainbow effect based on distance from the plane.
    """
    global progress, duration, fps, plane_normal, plane_point, led_positions
    global full_rgb_cycle_colors_gaps

    colors = full_rgb_cycle_colors_gaps

    for i in range(len(leds)):
        position = led_positions[i]
        
        # Skip if position is invalid (e.g., NaN)
        if np.isnan(position).any():
            continue
        
        # Calculate distance from the point to the plane
        distance = np.dot(plane_normal, position - plane_point)
        
        # Normalize the distance to a 0-1 range for wave cycling
        normalized_distance = (distance + progress) % 1

        # Get the color from the rainbow sequence
        color = get_color_in_sequence(colors, normalized_distance)
        
        # Set the LED color
        leds[i] = color

    leds.show()

    # Increment progress for the wave propagation
    progress += 1 / (duration * fps)
