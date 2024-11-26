from run import *

# import matplotlib.pyplot as plt
# from matplotlib.widgets import Button, Slider

x_val = 240
y_val = 240
z_val = 480

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

x_slider = Slider(
    ax=ax,
    label='x',
    valmin=0,
    valmax=480,
    valinit=x_val,
)

y_slider = Slider(
    ax=ax,
    label='y',
    valmin=0,
    valmax=480,
    valinit=y_val,
)

z_slider = Slider(
    ax=ax,
    label='z',
    valmin=0,
    valmax=480,
    valinit=z_val,
)

# The function to be called anytime a slider's value changes
def update():
    for i in range(NO_LEDS):
        x, y, z = positions[i]

        if x < x_val and y < y_val and z < z_val:
            leds[i] = (255, 0, 0)
        
    leds.show()

def x_update(val):
    global x_val
    x_val = val
    update()

def y_update(val):
    global y_val
    y_val = val
    update()

def z_update(val):
    global z_val
    z_val = val
    update()

# register the update function with each slider
x_slider.on_changed(x_update)
y_slider.on_changed(y_update)
z_slider.on_changed(z_update)

plt.show()