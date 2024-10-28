# Scans the lights, and saves the image scenes to a folder.
import yaml
import os
import shutil
from datetime import datetime
import time
from dynamic_leds.models.camera import CameraGroup
from dynamic_leds.models.led import LEDArray
from dynamic_leds.models.scan import Scan

print('Starting a scan!\n')

# Load settings
with open('../../examples/single_cam/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print('Loaded settings from config.yaml')


# Check if scan already exists
scan_name = config['SCAN_NAME']

if os.path.isdir(f'scans/{scan_name}'):
    input('Scan of that name already exists. Press Enter to overwrite, or Ctrl+C to cancel')
    input('Sure?')

    shutil.rmtree(f'scans/{scan_name}')


# Setup scan directorys
os.mkdir(f'scans/{scan_name}')
os.mkdir(f'scans/{scan_name}/images')
os.mkdir(f'scans/{scan_name}/camera_frame_positions')
print('Setup scan directory.')


# Setup LEDs
print('\nInitializing LEDs...')
leds = LEDArray(config)
leds.set_all_off()

# Setup camera(s)
print('\nInitializing cameras...')
cams = CameraGroup(config)
cams.test_all()

# Record start time
start_time = datetime.now()


try:
    input('\nMake the room dark, then press Enter to start the scan')

    
    # Check base images
    x = None
    while x != '':  
        # Base images
        for cam in cams:
            cam.save_photo(f'scans/{scan_name}/images/{cam.id}_base.jpg')
        
        print('\nSaved base image(s), check them now')
        x = input('Type \'r\' to restart, or press Enter to accept')
    

    # Turn on each light one by one, take a photo
    for i in range(len(leds)):
        print(f'Scanning LED {i}')
        
        # Turn on white
        leds[i] = (255, 255, 255)
        leds.show()
        time.sleep(0.1)

        # Read camera
        for cam in cams:
            cam.save_photo(f'scans/{scan_name}/images/{cam.id}_{i}.jpg')

        # Turn off
        leds[i] = (0, 0, 0)
        leds.show()

    # Could have multiple angles/rotation
    # input('Rotate the tree to the next angle, make the room bright again, then press enter to continue')

except Exception as e:
    print(e)

    # Release cam
    cam.release()

# Release camera
cam.release()

end_time = datetime.now()
duration_s = (end_time - start_time).total_seconds()


# Save scan details to a yaml file
scan_details = config
scan_details['START_TIME'] = start_time
scan_details['END_TIME'] = end_time
scan_details['DURATION_SECONDS'] = duration_s

with open(f'scans/{scan_name}/details.yaml', 'w') as f:
    yaml.dump(scan_details, f)


# Process scanned images
print('Processing scanned images...')
scan = Scan(scan_name)
scan.generate_camera_frame_positions()

print('Done!')