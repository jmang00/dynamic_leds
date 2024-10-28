import numpy as np

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
