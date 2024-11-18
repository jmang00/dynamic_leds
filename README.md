This library provides tools for scanning and running effects on individually addressable LEDs.

It is designed to be installed and run on a Raspberry Pi.

# Installation


# Usage

## Control using the text interface
1. Connect to 'DT-ML_Main'
2. Open a terminal and ssh into the pi (`ssh campi@ledpi`, password is `ledpi`)
3. Once you have remote access, run the 'leds' command


## Manually
To remotely start an interactive Python shell, run
```
sudo -E python
```

Then to setup the LEDs:
```
from dynamic_leds import DynamicLeds
l = DynamicLeds()
```

Basic Usage:
```
l.load_scene('basic')
l.run_effect('wave')
l.off()
```

# Concepts
A 'scene' will be stored as:
- a folder
- a config file

'layout':
- line
    - just some leds in a line
- flat
    - some leds spread out on a flat surface
- 3d
    - some leds in any 3d arrangement
- tree
    - some leds on a Christmas tree
    - assumes the tree is a cone
    - requires you to specify the dimensions of the tree

# Things to add:
- 




# Random Notes/ might neeed later

The `/examples` directory contains examples of using the library in different scenarios.

Originally inspired by [this Matt Parker video](https://youtu.be/TvlpIojusBE?si=Raabp9wFT22sQVxp).


- I chose NOT to use a virtual environment because adafruit needs to run as root.

sudo apt update
sudo apt install cmake
pip install --upgrade pip setuptools wheel