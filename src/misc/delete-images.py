import os

os.remove(f'scans/torquay/0_base.jpg')

for i in range(300):
    os.remove(f'torquay/0_{i}.jpg')