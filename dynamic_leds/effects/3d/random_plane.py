import numpy as np
from ...models.led import LEDArray

# The name of the effect
name = 'Rotating Plane'

# The frame rate
fps = 120

# Duration in seconds for a full rotation
duration = 1

# Global variables
normal_vector = None
rotation_matrix = None
center_point = None
positions = None

# The setup function. This is called once at the start of the sketch.
def setup(leds: LEDArray, led_positions: np.ndarray):
    global normal_vector, rotation_matrix, center_point, positions
    
    # Save LED positions and replace NaN values with 1000 (or any value above max)
    positions = np.nan_to_num(led_positions, nan=1000)

    # Generate a random normal vector
    normal_vector = np.random.rand(3)
    normal_vector[0] = 0  # Ensure it has no x component so it faces the lab
    normal_vector /= np.linalg.norm(normal_vector)

    # Calculate the bounding box center using np.nanmin and np.nanmax to handle NaNs
    min_x, max_x = np.nanmin(positions[:, 0]), np.nanmax(positions[:, 0])
    min_y, max_y = np.nanmin(positions[:, 1]), np.nanmax(positions[:, 1])
    min_z, max_z = np.nanmin(positions[:, 2]), np.nanmax(positions[:, 2])

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_z = (min_z + max_z) / 2

    center_point = np.array([center_x, center_y, center_z])

    # Precompute the rotation matrix for each frame
    theta = 2 * np.pi / (fps * duration)
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

# The draw function. This is called once per frame.
def draw(leds: LEDArray):
    global normal_vector, rotation_matrix, center_point, positions

    # Rotate the normal vector
    normal_vector = np.dot(rotation_matrix, normal_vector)

    # Display the plane on the lights
    for i in range(len(leds)):
        point = positions[i]
        expression = np.dot(normal_vector, center_point - point)

        if expression > 0:
            leds[i] = (255, 0, 0)  # Red for one side of the plane
        else:
            leds[i] = (0, 255, 0)  # Green for the other side
