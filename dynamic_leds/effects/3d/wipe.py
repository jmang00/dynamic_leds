""" A color wipe effect in 3D (x, y, z directions). """
import numpy as np
from ...models.led import LEDArray

# The name of the effect
name = '3D Color Wipe'

# The frame rate
fps = 60

# Global variables
wipe_progress = 0
wipe_axis = 0  # 0 = x, 1 = y, 2 = z
wipe_duration = 1  # Duration in seconds for the wipe to traverse the tree
wipe_width_ratio = 0.05  # Width of the wipe relative to the tree size
tree_bounds = None
led_positions = None
last_printed_step = -1  # Tracks the last printed step for progress bars

# The setup function. This is called once at the start of your sketch.
def setup(leds: LEDArray, positions: np.ndarray):
    global wipe_progress, wipe_axis, tree_bounds, led_positions

    # Replace all nans with 1000
    led_positions = positions = np.nan_to_num(positions, nan=0)

    wipe_progress = 0
    wipe_axis = 0
        

    # Determine the bounds of the tree along each axis
    tree_bounds = {
        'x': (np.nanmin(positions[:, 0]), np.nanmax(positions[:, 0])),
        'y': (np.nanmin(positions[:, 1]), np.nanmax(positions[:, 1])),
        'z': (np.nanmin(positions[:, 2]), np.nanmax(positions[:, 2])),
    }

    print("Setup complete. Tree bounds calculated:")
    print(f"  X: {tree_bounds['x']}")
    print(f"  Y: {tree_bounds['y']}")
    print(f"  Z: {tree_bounds['z']}")

# The draw function. This is called once per frame.
def draw(leds: LEDArray):
    global wipe_progress, wipe_axis, tree_bounds, led_positions, fps, wipe_duration, wipe_width_ratio, last_printed_step

    # Determine the bounds and width of the current wipe
    axis_key = ['x', 'y', 'z'][wipe_axis]
    min_bound, max_bound = tree_bounds[axis_key]
    tree_range = max_bound - min_bound
    wipe_width = wipe_width_ratio * tree_range

    # Calculate the current wipe position
    wipe_pos = min_bound + (wipe_progress / (fps * wipe_duration)) * tree_range

    # Apply colors based on the current wipe position and width
    for i, position in enumerate(led_positions):
        axis_value = position[wipe_axis]
        if wipe_pos - wipe_width / 2 <= axis_value <= wipe_pos + wipe_width / 2:
            c = [0,0,0]
            c[wipe_axis] = 255
            leds[i] = c
        else:
            leds[i] = (0, 0, 0)  # Off for LEDs outside the wipe

    leds.show()

    # Debug: Print progress every 10% of the duration
    total_steps = fps * wipe_duration
    step_size = total_steps // 10
    if wipe_progress % step_size == 0 and wipe_progress != last_printed_step:
        last_printed_step = wipe_progress
        progress_bar = "|" * (wipe_progress // step_size + 1)
        print(f"Progress on {axis_key.upper()} wipe: {progress_bar}", end="\r")

    # Update progress
    wipe_progress += 1

    # Reset or switch axis when the wipe completes
    if wipe_progress > total_steps:
        print(f"Completed {axis_key.upper()} wipe. Moving to next axis.")
        wipe_progress = 0
        wipe_axis = (wipe_axis + 1) % 3
        print(f"Starting {['X', 'Y', 'Z'][wipe_axis]} wipe.")
