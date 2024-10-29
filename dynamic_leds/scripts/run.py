import yaml
from ..models.scan import Scan
from ..models.camera import CameraGroup
from ..models.led import LEDArray

from ..effects.WaveEffect2D import WaveEffect2D


print('Initialising dynamic lighting!\n')


# Load settings
with open('../../examples/single_cam/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
print('Loaded settings from config.yaml')

# Setup LEDs
print('\nInitializing LEDs...')
leds = LEDArray(config)

# Setup camera(s)
print('\nInitializing cameras...')
cams = CameraGroup(config)  

# Setup scan object
print('\nLoading data from scan...')
scan = Scan(config['SCENE_NAME'])

print(scan.positions['A'])


# Do a wave effect

full_rgb_cycle_colors_gaps = [(255, 0, 0), (0,0,0), (0,0,0), (255, 255, 0), (0,0,0), (0,0,0), (0, 255, 0), (0,0,0), (0,0,0), (0, 255, 255), (0,0,0), (0,0,0), (0, 0, 255), (0,0,0), (0,0,0),  (255, 0, 255)]
effect = WaveEffect2D(
    leds,
    scan.positions['A'],
    full_rgb_cycle_colors_gaps,
    duration=3
)
effect.run()
