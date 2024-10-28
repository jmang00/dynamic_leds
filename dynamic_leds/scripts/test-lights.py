import yaml
import time
import random
from dynamic_leds.models.led import LEDArray

# Load settings
with open('../../examples/single_cam/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
print('Loaded settings from config.yaml')


# Setup LEDs
print('\nInitializing LEDs...')
leds = LEDArray(config)

leds.set_all_white()
leds.basic_cycle()

time.sleep(20)

    
# # Random green/red cycling
while True:
    for i in range(len(leds)):
        r = random.randint(1,2)

        if r == 1:
            leds[i] = (255, 0, 0)
        else:
            leds[i] = (0, 255, 0)

    leds.show()
    time.sleep(2)


# Turn on in batches
# batch = 10
# for i in range(50):
#     leds[i*batch:(i+1)*batch] = (255, 0, 0)
#     leds.show()
#     time.sleep(1)
#     leds[i*batch:(i+1)*batch] = (0, 0, 0)