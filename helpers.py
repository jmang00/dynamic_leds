
from PIL import Image, ImageChops
import cv2
import numpy as np

def find_pixel_to_mm_scale(image_path, reference_length_mm=75):
    # Load the image
    image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Use a color threshold to detect the pink strip (you may need to adjust the threshold values)
    lower_pink = np.array([245, 153, 187])
    upper_pink = np.array([255, 255, 255])

    mask = cv2.inRange(cv2.cvtColor(image, cv2.COLOR_BGR2HSV), lower_pink, upper_pink)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it corresponds to the pink strip)
    try:
        largest_contour = max(contours, key=cv2.contourArea)
    except:
        return None
    
    # Find the bounding box of the contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Display the contour
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Calculate pixels per mm
    pixels_per_mm = w / reference_length_mm

    return pixels_per_mm

def find_brightest_pixel(image):
    width, height = image.size
    brightest_pixel = None
    max_brightness = 0

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            # Calculate the brightness of the pixel (you can use different formulas)
            brightness = sum(pixel)  # Sum of R, G, and B values

            if brightness > max_brightness:
                max_brightness = brightness
                brightest_pixel = np.array((x, y))

    return brightness, brightest_pixel

def find_led_coords(image):
    # Input: an image
    # Output: the coorrdinates of the LED, or None if there isn't one visible

    # Just use a brightness threshold
    brightness, brightest_pixel = find_brightest_pixel(image)

    print(brightness)
    print(brightest_pixel)
    if brightness < 20:
        return None
    return brightest_pixel

def dist(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)