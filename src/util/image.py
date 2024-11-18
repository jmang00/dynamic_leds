"""
Utility functions for image processing.
"""

import cv2

def find_brightest_pixel(image):
    width, height = image.shape[:2]
    brightest_pixel = (0, 0)
    max_brightness = 0

    for x in range(width):
        for y in range(height):
            pixel = [y, x]
            # Calculate the brightness of the pixel (you can use different formulas)
            brightness = sum(pixel)  # Sum of R, G, and B values

            if brightness > max_brightness:
                max_brightness = brightness
                brightest_pixel = (x, y)

    return brightest_pixel


def find_circular_light_pixels(image, intensity_threshold, min_radius, max_radius, avoid_left_region, debug=False):
    # Input:
    # image
    # intensity_threshold
    # min_radius
    # max_radius
    # avoid_left_region

    # Convert image to a cv2 image
    image = np.array(image)
    # # Convert RGB to BGR
    # open_cv_image = open_cv_image[:, :, ::-1].copy()

    # Check if the image is successfully loaded
    if image is not None:
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Apply intensity thresholding to the blurred image
        _, binary_image = cv2.threshold(blurred_image, intensity_threshold, 255, cv2.THRESH_BINARY)

        # Apply Hough Circle Transform
        circles = cv2.HoughCircles(
            binary_image, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
            param1=40, param2=5, minRadius=min_radius, maxRadius=max_radius
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))

            # Filter circles based on the left region to avoid
            filtered_circles = [circle[0:2] for circle in circles[0, :] if circle[0] > avoid_left_region]

            if filtered_circles:
                pixel_coordinates = [tuple(coord) for coord in filtered_circles]

                if debug:
                    # Visualize the circles on the original image
                    for i in circles[0, :]:
                        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)

                    # Display the image with circles
                    cv2.imshow('Circle', image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                return pixel_coordinates
            else:
                print("No circular light sources found in the specified region.")
                return None
        else:
            print("No circular light sources found.")
            return None
