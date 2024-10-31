"""
A scene - a physical setup of LEDs & cameras.
"""

import os
import yaml

from .effect import Effect
from .led import LEDArray
from .scan import Scan
from ..models.camera import CameraGroup


class Scene:
    def __init__(self, scene_name):
        self.name = scene_name
        self.path = os.path.join(os.getcwd(), scene_name)

        print('Loading scene...')
        config_path = os.path.join(self.path,  'config.yaml')

        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"No config file found.")

        print('Found config file.\n')

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        print('Initializing LEDs...')
        self.leds = LEDArray(config)

        print('Initializing cameras...')
        self.cams = CameraGroup(config)

        scan_path = os.path.join(self.path, 'scan')
        if not os.path.isfile(config_path):
            print('No scan found. You will need to scan the scene before running effects.')
            return

        print('Loading data from scan...')
        scan = Scan(scan_path)

    # """ Create a new scan of the scene. """
    # def scan(self):
    #
    #     # self.scan.scan()

    # def load(
    #         scenes/{self.name}/details.yaml', 'r') as f:
    #
    #     details = yaml.safe_load(f)
    #
    #     self.cams = CameraGroup(details)
    #     self.no_leds = details['NO_LEDS']
    #     self.duration = details['DURATION_SECONDS']
    #
    #     self.load_camera_frame_positions()

    def run(self, effect: Effect):
        pass

    def load_camera_frame_positions(self):
        try:
            # Load the positions of each LED in each camera frame
            self.positions = {}
            for cam in self.cams:
                self.positions[cam.id] = np.genfromtxt(f'scans/{self.name}/camera_frame_positions/{cam.id}.csv',
                                                       delimiter=',')

        except OSError:
            print('No camera frame positions found')
            # self.generate_camera_frame_positions()
            # self.load_camera_frame_positions()

    def generate_camera_frame_positions(self):
        # Analyse the images to find the position of each LED in each camera frame

        for cam in self.cams:
            # Setup positions array
            positions = np.zeros((self.no_leds, 2))

            # Open camera base image
            base_img = cv2.imread(f'scans/{self.name}/images/{cam.id}_base.jpg')

            for i in range(self.no_leds):
                # Open image
                img = cv2.imread(f'scans/{self.name}/images/{cam.id}_{i}.jpg')

                # Find location of LED in image
                # print(img)
                # print(base_img)

                # print(img.shape)
                # print(base_img.shape)

                diff_img = cv2.subtract(img, base_img)
                # cv2.imshow('Difference Image', diff_img)

                # # Using the brightest pixel
                # x, y = find_brightest_pixel(  diff_img)

                # Using the circular light source
                intensity_threshold = 130  # Adjust this value based on your images
                shitter_intensity_threshold = 70  # Adjust this value based on your images
                min_radius = 5  # Adjust as needed based on the expected size of the circular light sources
                max_radius = 25  # Adjust as needed based on the expected size of the circular light sources
                avoid_left_region = 150  # Specify the x-coordinate to avoid circles on the left side

                coordinates = find_circular_light_pixels(diff_img, intensity_threshold, min_radius, max_radius,
                                                         avoid_left_region)

                # Show coordinate
                # # Display the image with circles
                # cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # cv2.imshow('Circles', img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

                if coordinates is None:
                    print(f'LED {i} on camera {cam.id} not found, repeat with a lower threshhold')
                    coordinates = find_circular_light_pixels(diff_img, shitter_intensity_threshold, min_radius,
                                                             max_radius, avoid_left_region)

                # Save position
                if coordinates is not None:
                    positions[i] = coordinates[0]

            # Save as a numpy object (for the next python script)
            np.save(f'scans/{self.name}/camera_frame_positions/{cam.id}.npy', positions)

            # Save as a csv
            np.round(positions)
            np.savetxt(
                f'scans/{self.name}/camera_frame_positions/{cam.id}.csv',
                positions,
                delimiter=','
            )


