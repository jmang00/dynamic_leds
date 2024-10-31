from dynamic_leds import DynamicLeds
from dynamic_leds.effects import WaveEffect2D

DynamicLeds.load_scene('single_cam')


# full_rgb_cycle_colors_gaps = [(255, 0, 0), (0,0,0), (0,0,0), (255, 255, 0), (0,0,0), (0,0,0), (0, 255, 0), (0,0,0), (0,0,0), (0, 255, 255), (0,0,0), (0,0,0), (0, 0, 255), (0,0,0), (0,0,0),  (255, 0, 255)]
# effect = WaveEffect2D(
#     leds,
#     scan.positions['A'],
#     full_rgb_cycle_colors_gaps,
#     duration=3
# )
#
# DynamicLeds.run(WaveEffect2D)