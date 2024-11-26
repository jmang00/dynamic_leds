"""
Defines a scene - a physical setup of LEDs & cameras.
"""

import os
import importlib
import yaml
import time

from .effect import Effect
from .led import LEDArray
from .scan import Scanner3DSpinning
from ..models.camera import CameraGroup


class Scene:
    def __init__(self, scene_name):
        self.name = scene_name

        print(f"Loading scene '{scene_name}'.")
        self.path = os.path.join(os.getcwd(), 'scenes', scene_name)

        if not os.path.isdir(self.path):
            raise FileNotFoundError(f"No config file found.")
        
        config_path = os.path.join(self.path,  'config.yaml')

        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"No config file found.")

        print('Loaded config file.\n')

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.fps = self.config['FPS']
        self.layout = self.config['LAYOUT']
        self.current_effect_file = None
        
        self.effects_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '../effects',
            self.layout
        ))
        
        self.effects_path_relative = os.path.join('../effects', self.layout)

        print('Initializing LEDs.')
        self.leds = LEDArray(self.config)

        if self.config['CAMS'] is not None:
            print('Initializing cameras.')
            self.cams = CameraGroup(self.config)
        else:
            self.cams = None

        self.scan_path = os.path.join(self.path, 'scan')
        if self.layout != 'LINE' and not os.path.isfile(self.scan_path):
            print('\nNo scan found. To run effects, you need to scan this scene.')
            input('Press Enter when you are ready to start scanning...')
            self.scan()
        else:
            print('Loading led positions from previous scan...')
            self.load_positions()
        
    def load_positions(self):
        # Load the led positions from a scan
        self.led_positions = os.path.join(self.scan_path, 'positions.csv')
        
    def scan(self):
        print('\n-----SCANNING------')
        Scanner3DSpinning(self.leds, self.cams, self.scan_path, self.config['SCAN']['ANGLES'],).run() # TODO: allow you to select the scan method in menu or in config file.
        self.load_positions()
        
    """ Returns a list of effects (python modules) that can be run on this scene. """
    def list_effects(self):
        return sorted(
            [f.split('.')[0] for f in os.listdir(self.effects_path) if f.endswith('.py') and not f.startswith('_')]
        )
    
    """ Loads an effect file and runs it """
    def run_effect(self, effect_name: str):
        effect_module_path_relative = os.path.join(self.effects_path_relative, effect_name)
        effect_module_path = effect_module_path_relative.replace(os.sep, '.')
        
        if effect_module_path.startswith('.'):
            effect_module_path = effect_module_path[1:]
        
        package = 'dynamic_leds.models'
        effect = importlib.import_module(effect_module_path, package)
        
        self.leds.set_all_off()
        effect.setup(self.leds)

        try:
            print('Running effect... press Ctrl+C to stop.')
            while True:
                effect.draw(self.leds)
                self.leds.show()
                time.sleep(1 / self.fps)
        except KeyboardInterrupt:
            self.leds.set_all_off()
    

    # def load_camera_frame_positions(self):
    #     try:
    #         # Load the positions of each LED in each camera frame
    #         self.positions = {}
    #         for cam in self.cams:
    #             self.positions[cam.id] = np.genfromtxt(f'scans/{self.name}/camera_frame_positions/{cam.id}.csv',
    #                                                    delimiter=',')

    #     except OSError:
    #         print('No camera frame positions found')
    #         # self.generate_camera_frame_positions()
    #         # self.load_camera_frame_positions()

    # def generate_camera_frame_positions(self):
    #     # Analyse the images to find the position of each LED in each camera frame

    #     for cam in self.cams:
    #         # Setup positions array
    #         positions = np.zeros((self.no_leds, 2))

    #         # Open camera base image
    #         base_img = cv2.imread(f'scans/{self.name}/images/{cam.id}_base.jpg')

    #         for i in range(self.no_leds):
    #             # Open image
    #             img = cv2.imread(f'scans/{self.name}/images/{cam.id}_{i}.jpg')

    #             # Find location of LED in image
    #             # print(img)
    #             # print(base_img)

    #             # print(img.shape)
    #             # print(base_img.shape)

    #             diff_img = cv2.subtract(img, base_img)
    #             # cv2.imshow('Difference Image', diff_img)

    #             # # Using the brightest pixel
    #             # x, y = find_brightest_pixel(  diff_img)

    #             # Using the circular light source
    #             intensity_threshold = 130  # Adjust this value based on your images
    #             shitter_intensity_threshold = 70  # Adjust this value based on your images
    #             min_radius = 5  # Adjust as needed based on the expected size of the circular light sources
    #             max_radius = 25  # Adjust as needed based on the expected size of the circular light sources
    #             avoid_left_region = 150  # Specify the x-coordinate to avoid circles on the left side

    #             coordinates = find_circular_light_pixels(diff_img, intensity_threshold, min_radius, max_radius,
    #                                                      avoid_left_region)

    #             # Show coordinate
    #             # # Display the image with circles
    #             # cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    #             # cv2.imshow('Circles', img)
    #             # cv2.waitKey(0)
    #             # cv2.destroyAllWindows()

    #             if coordinates is None:
    #                 print(f'LED {i} on camera {cam.id} not found, repeat with a lower threshhold')
    #                 coordinates = find_circular_light_pixels(diff_img, shitter_intensity_threshold, min_radius,
    #                                                          max_radius, avoid_left_region)

    #             # Save position
    #             if coordinates is not None:
    #                 positions[i] = coordinates[0]

    #         # Save as a numpy object (for the next python script)
    #         np.save(f'scans/{self.name}/camera_frame_positions/{cam.id}.npy', positions)

    #         # Save as a csv
    #         np.round(positions)
    #         np.savetxt(
    #             f'scans/{self.name}/camera_frame_positions/{cam.id}.csv',
    #             positions,
    #             delimiter=','
    #         )


