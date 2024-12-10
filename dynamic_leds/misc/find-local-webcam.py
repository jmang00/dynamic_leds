# Finds the index of the first working webcam and saves it to the current scene's config file.
import yaml
from dynamic_leds.models.camera import LocalCamera

# Loop through camera index to find one that works
cam_index = 0
MAX_INDEX = 5

while cam_index < MAX_INDEX:
    print(f'\nTrying index {cam_index}')
    cam = LocalCamera(cam_index)
    if cam.is_open():
        print(f'Found a working webcam at index {cam_index}!')
        cam.release()
        break

    cam_index += 1

else:
    print('No working webcams found.')


# Write to config.yaml
with open('../../examples/single_cam/config.yaml', 'w') as file:
    yaml.dump({'cam_index': cam_index}, file)
    print('Saved to settings file.')