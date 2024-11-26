import yaml
from dynamic_leds.models.led import LEDArray

# Load settings
with open('settings.yaml', 'r') as f:
    config = yaml.safe_load(f)


# Setup LEDs
print('Initializing LEDs...')
leds = LEDArray(config)


print('w: increase brightness')
print('s: decrease brightness')
print('i <increment>: set increment')
print('or enter a number between 0 and 1.\n')

increment = 0.05

while True:
    
    x = input()

    try:
        if x == 'w':
            BRIGHTNESS += increment
        
        elif x == 's':
            BRIGHTNESS -= increment

        elif x.startswith('i'):
            new_increment = x.split(' ')[1]
            increment = float(new_increment)

        else:
            BRIGHTNESS = float(x)
            assert 0 <= BRIGHTNESS <= 1

        leds.brightness = BRIGHTNESS
        leds.show()
        print(f'Brightness: {BRIGHTNESS}.\n')
    
    except:
        print('Invalid input.')
        continue
    
    