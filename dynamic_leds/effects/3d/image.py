import numpy as np
from PIL import Image
from ...models.led import LEDArray

name = "Image Mapping"
fps = 30

# Variables to hold the image and tree bounds
image_path = "/home/campi/leds/monash-automation-logo.png" # TODO generalise
image_data = None
tree_bounds = None
led_positions = None

def setup(leds: LEDArray, positions: np.ndarray):
    """
    Load the image and calculate tree bounds.
    """
    global image_data, tree_bounds, led_positions

    led_positions = positions
    
    # Load the image and convert it to RGB (resize if needed)
    image = Image.open(image_path).convert("RGB")
    image_data = np.array(image)  # Convert to a numpy array for easy access

    # Calculate the tree bounds
    tree_bounds = {
        'x': (np.nanmin(led_positions[:, 0]), np.nanmax(led_positions[:, 0])),
        'y': (np.nanmin(led_positions[:, 1]), np.nanmax(led_positions[:, 1])),
        'z': (np.nanmin(led_positions[:, 2]), np.nanmax(led_positions[:, 2])),
    }

    print("Setup complete. Tree bounds calculated:")
    print(f"  X: {tree_bounds['x']}")
    print(f"  Y: {tree_bounds['y']}")
    print(f"  Z: {tree_bounds['z']}")


def draw(leds: LEDArray,):
    """
    Map the image onto the cylindrical tree surface.
    """
    global image_data, tree_bounds, led_positions

    # Get the dimensions of the image
    img_height, img_width, _ = image_data.shape

    # Tree cylinder parameters
    x_min, x_max = tree_bounds['x']
    y_min, y_max = tree_bounds['y']
    z_min, z_max = tree_bounds['z']
    
    # Calculate the radius of the tree cylinder
    tree_radius = (x_max - x_min) / 2

    # Map each LED position to the image
    for i in range(len(leds)):
        position = led_positions[i]

        # Skip invalid positions
        if np.isnan(position).any():
            continue

        x, y, z = position

        # Calculate cylindrical coordinates
        # Angle theta (wrapped around the cylinder, normalized to 0-1)
        theta = np.arctan2(z, x)  # Angle in radians
        theta_normalized = (theta + np.pi) / (2 * np.pi)  # Normalize to 0-1
        
        # Height (y-axis, normalized to 0-1)
        y_normalized = (y - y_min) / (y_max - y_min)
        
        # Map normalized coordinates to image coordinates
        img_x = int(theta_normalized * img_width) % img_width
        img_y = int(y_normalized * img_height) % img_height

        # Get the corresponding pixel color from the image
        color = image_data[img_y, img_x]

        # Set the LED color
        leds[i] = tuple(color)

    leds.show()
