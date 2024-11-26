import yaml
from dynamic_leds.models.scan import Scan

# Load settings
with open('../../examples/single_cam/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
scan_name = config['SCAN_NAME']

# Process scanned images
print('Processing scanned images...')
scan = Scan(scan_name)
scan.generate_camera_frame_positions()
