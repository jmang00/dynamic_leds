"""
Contains everything to do with scanning.
"""

from datetime import datetime
from time import sleep
import yaml
import numpy as np
import cv2
import os
from abc import ABC, abstractmethod

from ..models.led import LEDArray
from ..models.camera import CameraGroup
from ..util.image import find_circular_light_pixels


"""
An abstract scanner class.

Output: A file containing the **positions** of the leds
"""
class Scanner(ABC):
    def __init__(self, leds: LEDArray, cams: CameraGroup, scan_path: str):
        self.scan_path = scan_path
        self.leds = leds
        self.cams = cams
        
        self.old_brightness = leds.brightness
        leds.set_brightness(1.0)

    def run(self):
        self.take_photos()
        self.photos_to_frame_positions()
        self.frame_positions_to_3d_positions() # also saves to CSV
        self.leds.set_brightness(self.old_brightness)
    
    @abstractmethod
    def take_photos(self):
        pass
    
    @abstractmethod
    def photos_to_frame_positions(self):
        pass
    
    @abstractmethod
    def frame_positions_to_3d_positions(self):
        pass
    


class Scanner3DSpinning(Scanner):
    """
    Currently only works for a SINGLE camera, MANUALLY.
    """
    name = '3d-spinning-manual'
    def __init__(self, leds, cams, scan_path, angles):
        super().__init__(leds, cams, scan_path)
        
        self.angles = angles

    def take_photos(self):
        # Record start time
        start_time = datetime.now()
        
        images_path = os.path.join(self.scan_path, 'images')
        
        # Create directory if it doesn't exist
        os.makedirs(images_path, exist_ok=True)
        
        try:
            for angle in self.angles:
                print(f'\nScanning at an angle of {angle} degrees...')
    
                print('\n~~ Make sure the room is dark ~~')
                input('Then press Enter to start the scan')
    
                x = None
                while x != '':
                    # Take a base image from each camera
                    for cam in self.cams:
                        cam.save_photo(os.path.join(images_path, f'{cam.id}_{angle}_base.jpg'))
    
                    # Check base image
                    print('\n~~ Confirm the base image looks okay ~~')
                    x = input('Press Enter to accept, or type "r" to retake it')
    
                # Turn on each light one by one, take a photo
                for i in range(len(self.leds)):
                    print(f'Scanning LED {i}')
                    
                    # Turn on white
                    self.leds[i] = (255, 255, 255)
                    self.leds.show()
                    sleep(0.1)
    
                    # Read camera
                    for cam in self.cams:
                        cam.save_photo(os.path.join(images_path, f'{cam.id}_{angle}_{i}.jpg'))
    
                    # Turn off
                    self.leds[i] = (0, 0, 0)
                    self.leds.show()
    
                input('Rotate the tree to the next angle, make the room bright again, then press enter to continue')
    
        except Exception as e:
            print(e)
    
            # Release cams
            for cam in self.cams:
                cam.release()
    
        # Release cams
        for cam in self.cams:
            cam.release()
    
        end_time = datetime.now()
        duration_s = (end_time - start_time).total_seconds()
    
        # Save scan details to a yaml file
        scan_details = {
            'START_TIME': start_time,
            'END_TIME': end_time,
            'DURATION_SECONDS': duration_s
        }
    
        with open(os.path.join(self.scan_path, 'details.yaml'), 'w') as f:
            yaml.dump(scan_details, f)
    def photos_to_frame_positions(self):
        # Open base images
        base_img = {}
        for angle in self.angles:
            base_img[angle] = cv2.imread(os.path.join(self.scan_path,f'{angle}_base.jpg'))


        # Setup positions array
        # positions_camera_frame[angle, led, x/y/z]
        positions_camera_frame = np.zeros((4, self.leds.count, 2))

        for i in range(self.leds.count):
            for angle in self.angles:
                # Find location of LED in image
                img = cv2.imread(os.path.join(self.scan_path,f'0_{angle}_{i}.jpg'))
                base_img = cv2.imread(os.path.join(self.scan_path,f'0_{angle}_base.jpg'))

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
                
                coordinates = find_circular_light_pixels(diff_img, intensity_threshold, min_radius, max_radius, avoid_left_region)


                # Show coordinate
                # # Display the image with circles
                # cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)  
                # cv2.imshow('Circles', img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
                if coordinates is None:
                    print(f'LED {i} at angle {angle} not found, repeat with a lower threshhold')
                    coordinates = find_circular_light_pixels(diff_img, shitter_intensity_threshold, min_radius, max_radius, avoid_left_region)

                # Save position
                if coordinates is not None:
                    positions_camera_frame[self.angles.index(angle), i] = coordinates[0]

            # TODO - check how many angles worked and redo

        # Print info
        no_cameras = [
            np.count_nonzero(positions_camera_frame[:,i,:])/2
            for i in range(self.leds.count)
        ]

        freq_no_cameras = np.unique(no_cameras, return_counts=True)
        freq_no_cameras = np.array(freq_no_cameras).T
        print(freq_no_cameras)

        # Save as a numpy object (for the next python script)
        np.save(os.path.join(self.scan_path, 'positions_camera_frame.npy'), positions_camera_frame)

        # Split into 4 CSVs and save (so Mathematica can read them)
        for angle in self.angles:
            file_path = os.path.join(self.scan_path, f'positions_camera_frame_{angle}.csv')
            np.savetxt(
                file_path,
                positions_camera_frame[self.angles.index(angle)],
                delimiter=','
            )
    
    def frame_positions_to_3d_positions(self):
        # Open the positions_camera_frame.npy file
        positions_camera_frame = np.load(os.path.join(self.scan_path, 'positions_camera_frame.npy'))
    
        # Create an empty array for the 3D positions
        positions_global = np.zeros((self.leds.count, 3)) 
    
        # Convert the set of 2D coordinates into 3D coordinates
        for i in range(self.leds.count):
            coords = positions_camera_frame[:, i, :]
    
            xF, yF = coords[0]
            xB, yB = coords[2]
            xL, yL = coords[1]
            xR, yR = coords[3]
    
            # Calculate the 3D coordinates
            X = [xF, 480 - xB]  # multiple ways to calculate
            X = [x for x in X if x != 0]  # filter out zeros
            if not X:
                print(f"Couldn't figure out position of LED {i}")
                positions_global[i] = [None, None, None]
                continue
            else:
                X = np.mean(X)  # take the average
    
            Y = [xL, 480 - xR]
            Y = [y for y in Y if y != 0]
            if not Y:
                print(f"Couldn't figure out position of LED {i}")
                positions_global[i] = [None, None, None]
                continue
            else:
                Y = np.mean(Y)
    
            Z = [yF, yB, yL, yR]
            Z = [z for z in Z if z != 0]
            if not Z:
                print(f"Couldn't figure out position of LED {i}")
                positions_global[i] = [None, None, None]
                continue
            else:
                Z = np.mean(Z)
    
            print(X, Y, Z)
    
            # Save position
            positions_global[i] = [X, Y, Z]
    
        # Save the positions to a CSV file
        np.savetxt(os.path.join(self.scan_path, 'positions.csv'), positions_global, delimiter=',')


      
