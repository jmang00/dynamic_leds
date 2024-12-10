#!/bin/bash

cd $DYNAMIC_LEDS_PATH

while getopts "i" flag; do
    case $flag in
        i)
            echo "Starting leds in interactive mode..."
            sudo -E python -i "scripts/run_interactive.py"
        ;;
    esac
done

# Default - no flags passed
if (( $OPTIND == 1 )); then
    echo "Opening leds interface..."
    sudo -E python "scripts/run_interface.py"
fi