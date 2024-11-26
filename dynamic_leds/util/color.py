"""
Utility functions for handling colors.
"""

import numpy as np
from matplotlib.colors import to_rgb


# Return the colour some fraction of the way between two rgb colours
def inbetween_color(color1, color2, fraction):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * fraction)
    g = int(g1 + (g2 - g1) * fraction)
    b = int(b1 + (b2 - b1) * fraction)
    return r, g, b


# Return the colour some fraction of the way through a whole sequence of colours
def get_color_in_sequence(color_list, fraction):
    list_index = np.floor(fraction * len(color_list))
    color1 = color_list[int(list_index)]
    color2 = color_list[int(list_index + 1) % len(color_list)]
    list_fraction = fraction * len(color_list) - list_index
    return inbetween_color(color1, color2, list_fraction)

""" Returns an RGB colour """
def color_input():
    """Returns an RGB color as a tuple in the range 0-255."""
    while True:
        choice = input("Would you like to enter an RGB color or a CSS color name? (rgb/css): ").strip().lower()
        if choice == "rgb":
            try:
                # Prompt for RGB values in the range 0-255
                r = int(input("Enter red value (0-255): "))
                g = int(input("Enter green value (0-255): "))
                b = int(input("Enter blue value (0-255): "))
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    return (r, g, b)
                else:
                    print("Please enter values between 0 and 255.")
            except ValueError:
                print("Invalid input. Please enter integer values.")
        elif choice == "css":
            # Prompt for a CSS color name
            css_color = input("Enter a CSS color name: ").strip().lower()
            try:
                # Convert to RGB (0-1 range) and scale to 0-255
                rgb_0_1 = to_rgb(css_color)
                rgb_255 = tuple(int(value * 255) for value in rgb_0_1)
                return rgb_255
            except ValueError:
                print(f"'{css_color}' is not a valid CSS color name. Please try again.")
        else:
            print("Invalid choice. Please type 'rgb' or 'css'.")
