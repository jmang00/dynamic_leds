"""
A scan of a scene.
"""

import yaml
import numpy as np
# import cv2
from ..models.camera import CameraGroup

class Scan:
    def __init__(self, scan_path):
        self.path = scan_path
        
        with open(scan_path, 'r') as f:
            details = yaml.safe_load(f)

        self.name = details['SCAN_NAME']
        self.no_leds = details['NO_LEDS']
        self.led_positions = None # TODO: load positions
        self.cams = None # TODO: load camera positions

    def run(self):
        # Load the camera frame positions
        self.load_camera_frame_positions()

        # Generate the camera frame positions if they do not exist
        if not self.positions:
            self.generate_camera_frame_positions()
            self.load_camera_frame_positions()

        # Run the scan
        self.run_scan()




