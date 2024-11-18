# import board
# import neopixel
# from PIL import Image
# from PIL import ImageChops
# import requests
# from io import BytesIO
# import numpy as np
# import time

# class LightSet:
# PIXEL_PIN = board.D18
# PIXEL_COUNT = 50
# URL = 'http://172.32.1.166:8080/?action=snapshot'

# pixels = neopixel.NeoPixel(PIXEL_PIN, PIXEL_COUNT, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# def get_snapshot():
#     response = requests.get(URL)
#     img = Image.open(BytesIO(response.content))
#     return img

# def turn_off_all():
#     pixels.fill((0, 0, 0))
#     pixels.show()

# def find_brightest_pixel(image):
#     width, height = image.size
#     brightest_pixel = (0, 0)
#     max_brightness = 0

#     for x in range(width):
#         for y in range(height):
#             pixel = image.getpixel((x, y))
#             # Calculate the brightness of the pixel (you can use different formulas)
#             brightness = sum(pixel)  # Sum of R, G, and B values

#             if brightness > max_brightness:
#                 max_brightness = brightness
#                 brightest_pixel = (x, y)

#     return brightest_pixel

# def scan_lights():
#     # Scans the lights
#     # Returns a list of positions
#     #TODO: add an option to save it to a csv/import it

#     positions = np.zeros((PIXEL_COUNT, 2))

#     base_img = get_snapshot()
#     base_img.save('base_img.jpg')

#     # Turn on each light one by one, take a photo
#     for i in range(PIXEL_COUNT):
#         # Turn on white
#         pixels[i] = (255, 255, 255)
#         pixels.show()
#         time.sleep(0.1)

#         # Read camera
#         img = get_snapshot()
#         img.save('img.jpg')

#         # Turn off
#         pixels[i] = (0, 0, 0)
#         pixels.show()
#         time.sleep(0.1)

#         # Find brightest pixel
#         diff_img = ImageChops.difference(img, base_img)
#         diff_img.save('diff.jpg')

#         x, y = find_brightest_pixel(img)
#         print(f'Brightest in image: ({x}, {y})')

#         x, y = find_brightest_pixel(diff_img)
#         print(f'Brightest in diff image: ({x}, {y})')


#         # Save position
#         positions[i] = [x, y]
    
#     print(positions)
#     return positions

# # Return the colour some fraction of the way betwen two rgb colours
# def inbetween_color(color1, color2, fraction):
#     r1, g1, b1 = color1
#     r2, g2, b2 = color2
#     r = int(r1 + (r2 - r1) * fraction)
#     g = int(g1 + (g2 - g1) * fraction)
#     b = int(b1 + (b2 - b1) * fraction)
#     return (r, g, b)

# # Return the colour some fraction of the way through a whole sequence of colours
# def get_color_in_sequence(color_list, fraction):
#     list_index = np.floor(fraction * len(color_list))
#     color1 = color_list[int(list_index)]
#     color2 = color_list[int(list_index + 1) % len(color_list)]
#     list_fraction = fraction * len(color_list) - list_index
#     return inbetween_color(color1, color2, list_fraction)

# # Define a list of colors for the rainbow
# rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
# full_rgb_cycle_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
# christmas = [(255,0,0), (0, 255, 0)]
# monash = [(100,100,100), (0, 0, 255),(100,100,100)]

# # # get_snapshot().save('test.jpg')
# # turn_off_all()
# # time.sleep(0.1)
# # positions = scan_lights()

# positions = [
#     [103, 367],
#     [40, 356],
#     [33, 290],
#     [96, 264],
#     [156, 268],
#     [64, 207],
#     [100, 179],
#     [79, 139],
#     [115, 112],
#     [169, 165],
#     [125, 121],
#     [166, 142],
#     [205, 151],
#     [248, 153],
#     [343, 394],
#     [322, 176],
#     [363, 189],
#     [397, 133],
#     [452, 173],
#     [489, 163],
#     [543, 141],
#     [577, 119],
#     [559, 88],
#     [486, 190],
#     [515, 155],
#     [541, 213],
#     [523, 239],
#     [473, 298],
#     [478, 312],
#     [468, 358],
#     [428, 376],
#     [389, 392],
#     [348, 425],
#     [315, 431],
#     [297, 386],
#     [268, 369],
#     [245, 347],
#     [77, 215],
#     [168, 261],
#     [222, 253],
#     [278, 315],
#     [318, 297],
#     [320, 257],
#     [336, 222],
#     [342, 251],
#     [330, 236],
#     [330, 281],
#     [330, 312],
#     [386, 368],
#     [338, 385]
# ]

# min_x = min(positions, key=lambda x: x[0])[0]
# max_x = max(positions, key=lambda x: x[0])[0]
# min_y = min(positions, key=lambda x: x[1])[1]
# max_y = max(positions, key=lambda x: x[1])[1]

# effect_progress = 0 # goes from 0 to 1
# speed = 2 # time in seconds to go through the whole cycle
# fps = 60

# while True:
#     # Set each LED to the right colour
#     for i in range(PIXEL_COUNT):

#         # Get the LED position
#         x, y = positions[i]

#         x_rel = (x - min_x) / (max_x - min_x)

#         # Calculate the color
#         color = get_color_in_sequence(
#             monash, 
#             (effect_progress + x_rel) % 1
#         )

#         # print(color)

#         # Set the colour
#         pixels[i] = color
    
    
#     # Wait and then increment the effect progress
#     pixels.show()
#     time.sleep(1 / fps)
#     effect_progress = (effect_progress + 1 / (speed * fps)) % 1
