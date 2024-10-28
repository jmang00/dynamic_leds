# Scans the lights, and saves the image scenes to a folder.
import os
import datetime
import yaml
from models.camera import LocalCamera
from models.leds import LEDArray

print('Starting a new scan...')

scan_name = input('Enter scan name: ')

try:
    os.mkdir(f'scans/{scan_name}')
except FileExistsError:
    pass

scan_time = datetime.now().strftime("scan_%H_%M_%d_%m_%Y") 


# Open camera from settings file
f = open('settings.yaml', 'r')
config = yaml.safe_load(f)
cam = LocalCamera('webcam', config['cam_index'])

# For flat lights, just one angle
angles = [0]

# Add support for multiple cameras later
# Multiple cameras on the Automation lab networks
# cams = [
#     Camera('A', 'http://172.32.1.225:8080/?action=snapshot'),
#     Camera('B', 'http://172.32.1.226:8080/?action=snapshot'),
#     Camera('C', 'http://172.32.1.227:8080/?action=snapshot')
# ]

# 1 camera on the Automation lab network
# cams = [
#     Camera(0, 'http://172.32.1.226:8080/?action=snapshot'),
# ]

# For the tree, rotate 90 degrees within scenes
# angles = [
#     0,
#     90,
#     180,
#     270
# ]




input('Press Enter to start')

try:
    for angle in angles:
        print(f'\nScanning at an angle of {angle} degrees...')

        # # Take an image from each camera with the lights ON
        # for cam in cams:
        #     # base_img = cam.take_photo()
        #     # base_img.save(f'{scan_name}/{cam.id}_bright.jpg')
        #     cam.save_photo(f'{scan_name}/{cam.id}_{angle}_bright.jpg')

        print('\n~~ Make the room dark ~~')
        input('Press Enter to start the scan')

        x = None
        while x != '':
            # Take a base image from each camera
            for cam in cams:
                cam.save_photo(f'{scan_name}/{cam.id}_{angle}_base.jpg')
                # base_img = cam.take_photo()
                # cv2.imshow('Base Image', base_img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # base_img.save(f'{scan_name}/{cam.id}_{angle}_base.jpg')

            # Check base image
            print('\n~~ Confirm the base image looks okay ~~')
            x = input('Press Enter to accept, or enter anything else to take it again')



        # Turn on each light one by one, take a photo
        for i in range(NO_LEDS):
            print(f'Scanning LED {i}')
            
            # Turn on white
            leds[i] = (255, 255, 255)
            leds.show()
            time.sleep(0.1)

            # Read camera
            for cam in cams:
                cam.save_photo(f'{scan_name}/{cam.id}_{angle}_{i}.jpg')

            # Turn off
            leds[i] = (0, 0, 0)
            leds.show()

        input('Rotate the tree to the next angle, make the room bright again, then press enter to continue')

except Exception as e:
    print(e)

    # Release cams
    for cam in cams:
        cam.release()

# Release cams
for cam in cams:
    cam.release()