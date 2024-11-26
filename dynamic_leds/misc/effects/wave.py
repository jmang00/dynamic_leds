
from run import *
# from scipy.spatial.transform import Rotation

# Define a list of colors for the rainbow
def gap(w):
    return [(0,0,0)]*w

rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
full_rgb_cycle_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
full_rgb_cycle_colors_gaps = [(255, 0, 0), (0,0,0), (0,0,0), (255, 255, 0), (0,0,0), (0,0,0), (0, 255, 0), (0,0,0), (0,0,0), (0, 255, 255), (0,0,0), (0,0,0), (0, 0, 255), (0,0,0), (0,0,0),  (255, 0, 255)]
monash = [(10,0,190), (0, 0, 0), (0, 0, 0), (80, 0, 230), (0,0,0), (0, 0, 0), (180, 180, 180), (0,0,0), (0, 0, 0)]
#grb
# christmas = [(255,0,0)] + gap(3) + [(0, 255, 0)] + gap(3)
# christmas = [(255,0,0)] + [(255,0,0)] + [(255,255,255)] + [(0, 255, 0)] + [(0, 255, 0)] + [(255,255,255)]
#christmas = [(50,50,255)] + gap(1) + [(0,255,0)] + gap(1) #popo
christmas = [(0, 255, 0)]+[(127, 255, 0)]+[(255, 255, 0)]+ [(255, 0, 0)]+[(0, 0, 255)]+[(75, 0, 130)]+[(148, 0, 211)] #rainbow

single_wave = [(3, 182,  252)] + [(0,0,0)]*10


# Effect Settings
duration = 1 # time in seconds to go through the whole cycle
fps = 60
directions = 'z'
# directions = ['x', 'y', 'z']
COLOR_LIST = christmas


# Return the colour some fraction of the way betwen two rgb colours
def inbetween_color(color1, color2, fraction):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * fraction)
    g = int(g1 + (g2 - g1) * fraction)
    b = int(b1 + (b2 - b1) * fraction)
    return (r, g, b)

# Return the colour some fraction of the way through a whole sequence of colours
def get_color_in_sequence(color_list, fraction):
    list_index = np.floor(fraction * len(color_list))
    color1 = color_list[int(list_index)]
    color2 = color_list[int(list_index + 1) % len(color_list)]
    list_fraction = fraction * len(color_list) - list_index
    return inbetween_color(color1, color2, list_fraction)

def apply_random_plane_rotation(positions):
    # Generate a random normal vector for the plane
    normal_vector = np.random.rand(3)
    normal_vector /= np.linalg.norm(normal_vector)

    # Generate a random angle of rotation
    angle = np.random.uniform(0, 2 * np.pi)

    # Create a rotation matrix based on the normal vector and angle
    rotation_matrix = Rotation.from_rotvec(normal_vector * angle).as_matrix()

    # Apply the rotation to the positions
    rotated_positions = np.dot(positions, rotation_matrix.T)

    return rotated_positions


min_x = min(positions, key=lambda x: x[0])[0]
max_x = max(positions, key=lambda x: x[0])[0]
min_y = min(positions, key=lambda x: x[1])[1]
max_y = max(positions, key=lambda x: x[1])[1]
min_z = min(positions, key=lambda x: x[2])[2]
max_z = max(positions, key=lambda x: x[2])[2]

center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2
center_z = (min_z + max_z) / 2

print(center_x, center_y, center_z)

dist_from_center = [np.sqrt((x - center_x)**2 + (y - center_y)**2 + (z - center_z)**2) for x, y, z in positions]
dist_from_center_rel = dist_from_center / max(dist_from_center)

x_rel = (positions[:, 0] - min_x) / (max_x - min_x)
y_rel = (positions[:, 1] - min_y) / (max_y - min_y)
z_rel = (positions[:, 2] - min_z) / (max_z - min_z)

try:
    while True:
        direction = random.choice(directions)
        # if direction == 'random':
        #     rotated_positions = apply_random_rotation(positions)

        # Update lights to the next frame
        effect_progress = 0 # goes from 0 to 1
        while effect_progress < 1:
            # Set each LED to the right colour
            for i in range(NO_LEDS):

                # Get the LED position
                x, y, z = positions[i]

                if direction == 'x':
                    # ----- left/right wave -----
                    # Relative x position
                    p = x_rel[i]

                if direction == 'y':
                    # ----- front/back wave -----
                    # Relative y position
                    p = y_rel[i]
                
                if direction == 'z':
                    # ----- up/down wave -----
                    # Relative z position
                    p = z_rel[i]
                
                if direction == 'radial':
                    # ----- Center circle wave -----
                    # relative dist from center
                    p = dist_from_center_rel[i]
                
                if direction == 'random':
                    pass


                # Skip if p is nan
                if np.isnan(p):
                    continue

                # p is the increase in progress for the current pixel
                # Calculate the color
                color = get_color_in_sequence(
                    COLOR_LIST, 
                    (effect_progress + p) % 1
                )

                # Set the colour
                leds[i] = color
            
            
            # Wait and then increment the effect progress
            leds.show()
            time.sleep(1 / fps)
            effect_progress += 1 / (duration * fps)

except:
    set_all_off()
    raise