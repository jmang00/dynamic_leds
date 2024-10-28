import board
import neopixel
import time

# Define the LED grid properties
num_pixels = 16  # Number of LEDs in your grid
pixel_pin = board.D18  # Change this to your data pin
ORDER = neopixel.RGB  # Order of the LED colors (RGB or GRB)

# Initialize the NeoPixel grid
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER)

# Data points for the letter "A"
letter_A = [
    (7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7),  # Diagonal left
    (9, 0), (8, 1), (7, 2), (10, 2), (5, 3), (11, 3), (4, 4), (12, 4),  # Diagonal right
]

# Function to display a letter on the LED grid
def display_letter(letter_data):
    for data_point in letter_data:
        x, y = data_point
        if 0 <= x < num_pixels and 0 <= y < num_pixels:
            pixel_index = y * num_pixels + x
            pixels[pixel_index] = (255, 255, 255)  # White color
    pixels.show()

try:
    while True:
        display_letter(letter_A)
        time.sleep(1)  # Display for 1 second (adjust as needed)
        for i in range(num_pixels):
            pixels[i] = (0, 0, 0)  # Turn off all LEDs
        pixels.show()
        time.sleep(1)  # Pause for 1 second
except KeyboardInterrupt:
    # Turn off the LEDs and exit gracefully
    for _ in range(num_pixels):
        pixels.fill((0, 0, 0))
        pixels.show()
