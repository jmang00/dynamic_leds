#!/bin/bash

echo "Installing dynamic_leds in $PWD- this may break other user installations of numpy."

read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

# Install dependencies
sudo apt-get update
sudo apt-get install python3-opencv
sudo apt-get install libopenblas-dev
sudo apt-get install libssl-dev
pip install pyyaml --break-system-packages
pip install adafruit-circuitpython-neopixel --break-system-packages
pip install RPi.GPIO --break-system-packages
pip install rpi_ws281x --break-system-packages
pip install numpy --break-system-packages
pip install requests --break-system-packages
pip install matplotlib --break-system-packages
pip install opcua --break-system-packages


# Install dynamic_leds as a local package
pip install -e "$PWD/dynamic_leds" --break-system-packages


# Add the location to path
path_line="export DYNAMIC_LEDS_PATH='$PWD/dynamic_leds'"

# Check if the line already exists to avoid duplicates
if ! grep -Fxq "$path_line" ~/.bashrc
then
    # Add to .bashrc
    echo "$path_line" >> ~/.bashrc
    echo "Variable DYNAMIC_LEDS_PATH set in .bashrc"
else
    echo "Variable DYNAMIC_LEDS_PATH already exists in .bashrc"
fi


# Create bash alias for the 'run' command

# Get the directory of the script
SCRIPT_DIR=$(dirname "$0")

# Define the alias line to add to .bashrc
alias_line="alias leds='$PWD/dynamic_leds/scripts/run.sh'"

# Check if the alias already exists to avoid duplicates
if ! grep -Fxq "$alias_line" ~/.bashrc
then
    # Add the alias to .bashrc
    echo "$alias_line" >> ~/.bashrc
    echo "Alias 'leds' added to .bashrc"
else
    echo "Alias 'leds' already exists in .bashrc"
fi


# old venv stuff:
# if ! [ -d venv ]; then
#   echo "Creating virtual environment..."
#   python3 -m venv venv
# fi

# cv2Path=$(python3 -c "import cv2; print(cv2.__file__)")

# if ! [ -d $cv2Path ] then
#     echo "Installing cv2 globally"
#     sudo apt-get update
#     sudo apt-get install python3-opencv
# else
#     echo "Found cv2 installed at $cv2Path, linking it."    
#     ln -s /usr/lib/python3/dist-packages/cv2.cpython-*.so venv/lib/python3.*/site-packages/
# fi

# source venv/bin/activate
# echo "Activated virtual environment: $(which python)"
# pip install pyyaml
# pip install adafruit-circuitpython-neopixel
# pip install RPi.GPIO
# pip install rpi_ws281x
# pip install numpy
# pip install requests
