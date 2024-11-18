import os

for i in range(301):
    os.rename(f'torquay-flat/0_{i}.jpg', f'torquay-flat/0_0_{i}.jpg')

for i in range(301):
    os.rename(f'scan/0_{i}.jpg', f'torquay-flat/0_0_{i}.jpg')