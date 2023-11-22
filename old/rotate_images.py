from PIL import Image, ImageChops


NO_LEDS = 250
cams = ['A', 'B', 'C']
scan_name = 'scan1'

# Rotate every image by 270 degrees

# # Base
for cam in cams:
    img = Image.open(f'{scan_name}/{cam}_base.jpg')
    img = img.rotate(270, expand=True)
    img.save(f'{scan_name}/{cam}_base.jpg')

# Bright
for cam in cams:
    img = Image.open(f'{scan_name}/{cam}_bright.jpg')
    img = img.rotate(270, expand=True)
    img.save(f'{scan_name}/{cam}_bright.jpg')

# # Main
for i in range(NO_LEDS):
    for cam in cams:
        img = Image.open(f'{scan_name}/{cam}_{i}.jpg')
        img = img.rotate(270, expand=True)
        img.save(f'{scan_name}/{cam}_{i}.jpg')