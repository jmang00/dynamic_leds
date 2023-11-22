# Analyse the images to find the position of each LED

# Input: a folder of images
# Output: a positions.csv file

from helpers import find_pixel_to_mm_scale, find_led_coords, dist, find_brightest_pixel
from PIL import Image, ImageChops, ImageDraw
import numpy as np


NO_LEDS = 250
cams = ['A', 'B', 'C']
# tree coordinates in each camera frame
tree_top = np.array([(255,53), (264, 36), (305, 18)])
tree_bottom = np.array([(264, 599), (268, 492), (266, 633)])
actual_tree_height_mm = 2130

# Calculate a mm per pixel scale for each camera
# Do I need to do more complex camera properties stuff??
mm_per_pixel = []
for i in range(len(cams)):
    height_pixels = dist(tree_top[i], tree_bottom[i])
    mm_per_pixel.append(
        actual_tree_height_mm / height_pixels
    )

print(mm_per_pixel)
scan_name = 'scan1'


# Load the base images
base_img = {}
for cam in cams:
    img = Image.open(f'{scan_name}/{cam}_base.jpg')
    base_img[cam] = img


# Look through the images for each LED
positions = np.zeros((NO_LEDS, 3))
z_pos = np.zeros((NO_LEDS, 1))

for i in range(NO_LEDS):
    print(f'\nLED {i}')
    
    # Open the images and find diffs
    imgs = [
        Image.open(f'{scan_name}/{cam}_{i}.jpg')
        for cam in cams
    ]

    diff_imgs = [
        ImageChops.difference(imgs[c], base_img[cams[c]])
        for c in range(len(cams))
    ]

    # Find the brightest pixel in each image
    brightness = [0]*3
    brightest_pixel = [None]*3
    for c in range(len(cams)):
        brightness[c], brightest_pixel[c] = find_brightest_pixel(diff_imgs[c])
     
    
    # Get camera with highest brightness
    c = np.argmax(brightness)
    print(f'Using camera {cams[c]}, brightness {brightness[c]}')

    # Coordinates of the brightest pixel in camera frame
    P = brightest_pixel[c]

    # Coordinates of the tree within the camera frame
    B = tree_bottom[c]
    T = tree_top[c]
    
    # Draw these 3 points on the diff image and show it
    img = diff_imgs[c]
    draw = ImageDraw.Draw(img)
    point_size = 3
    # Draw P
    draw.ellipse([P[0] - point_size, P[1] - point_size,
              P[0] + point_size, P[1] + point_size],
             fill="red")
    
    # Draw B and T in green
    draw.ellipse([B[0] - point_size, B[1] - point_size,
                B[0] + point_size, B[1] + point_size],
                 fill="green")
    draw.ellipse([T[0] - point_size, T[1] - point_size,
                T[0] + point_size, T[1] + point_size],
                 fill="green")

    draw.line([B[0], B[1], T[0], T[1]], fill="green", width=1)
    img.show()
    

    # print(P, B, T)
    # # Define the line from B to T
    # r = lambda t: B + (T-B)*t
    # print(r(0), r(1))
    # print(r)
    # print(np.dot(P-r(t),r(t)))
    # tsols = np.linalg.solve(
    #     np.dot(P-r(t),r(t)),
    #     0
    # )
    # P_rel = P-r(tsols[0])

    # Find the coordinates of the LED relative to the tree
    # From Mathematica
    P_rel = [
        (-B[0] + P[0] - ((-B[0] + T[0]) * (2 * B[0]**2 + 2 * B[1]**2 - B[0] * P[0] - B[1] * P[1] - 2 * B[0] * T[0] + P[0] * T[0] - 2 * B[1] * T[1] + P[1] * T[1] + np.sqrt(-4 * (B[0]**2 - B[0] * P[0] + B[1] * (B[1] - P[1])) * (B[0]**2 + B[1]**2 - 2 * B[0] * T[0] + T[0]**2 - 2 * B[1] * T[1] + T[1]**2) + (2 * B[0]**2 + 2 * B[1]**2 + P[0] * T[0] - B[0] * (P[0] + 2 * T[0]) + P[1] * T[1] - B[1] * (P[1] + 2 * T[1]))**2))) / (2 * (B[0]**2 + B[1]**2 - 2 * B[0] * T[0] + T[0]**2 - 2 * B[1] * T[1] + T[1]**2))),
        (-B[1] + P[1] - ((-B[1] + T[1]) * (2 * B[0]**2 + 2 * B[1]**2 - B[0] * P[0] - B[1] * P[1] - 2 * B[0] * T[0] + P[0] * T[0] - 2 * B[1] * T[1] + P[1] * T[1] + np.sqrt(-4 * (B[0]**2 - B[0] * P[0] + B[1] * (B[1] - P[1])) * (B[0]**2 + B[1]**2 - 2 * B[0] * T[0] + T[0]**2 - 2 * B[1] * T[1] + T[1]**2) + (2 * B[0]**2 + 2 * B[1]**2 + P[0] * T[0] - B[0] * (P[0] + 2 * T[0]) + P[1] * T[1] - B[1] * (P[1] + 2 * T[1]))**2))) / (2 * (B[0]**2 + B[1]**2 - 2 * B[0] * T[0] + T[0]**2 - 2 * B[1] * T[1] + T[1]**2)))
    ]

    print(P_rel)

    # Also convert to mm
    P_rel *= mm_per_pixel[c]

    # The relative y then becomes the z coordinate
    print(f'Camera {cams[c]}:', P_rel)
    z_pos[i] = P_rel[1]

    

    # # Save position
    # positions[i] = [x, y, 0]
    
    # np.saveT[0]t('positions.csv', positions, delimiter=",", fmt="%d")

print(z_pos)
