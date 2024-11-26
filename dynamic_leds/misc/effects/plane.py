from run import *

# This effect chooses a random plane

# Generate a random normal vector
normal_vector = np.random.rand(3)
normal_vector[0] = 0 # make it have no x component so it faces the lab
normal_vector /= np.linalg.norm(normal_vector)

# # Generate a random middle point 
# middle_point = np.random.rand(3)
# middle_point = np.linalg.norm(middle_point)

min_x = min(positions, key=lambda x: x[0])[0]
max_x = max(positions, key=lambda x: x[0])[0]
min_y = min(positions, key=lambda x: x[1])[1]
max_y = max(positions, key=lambda x: x[1])[1]
min_z = min(positions, key=lambda x: x[2])[2]
max_z = max(positions, key=lambda x: x[2])[2]

center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2
center_z = (min_z + max_z) / 2

center_point = np.array([center_x, center_y, center_z])

def get_rotation_matrix(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])


fps = 120
duration = 1 # time in seconds for a full rotation
rotation_matrix = get_rotation_matrix(2 * np.pi / (fps * duration)) # rotation from one frame to the next


try:
    while True:
        # Rotate the normal
        normal_vector = np.dot(rotation_matrix, normal_vector)

        print(normal_vector)

        # Display the plane on the lights
        for i in range(NO_LEDS):
            point = positions[i]

            # print(normal_vector, center_point, point)
            expression = np.dot(normal_vector, center_point - point)

            if expression > 0:
                leds[i] = (255, 0, 0)
            
            if expression < 0:
                leds[i] = (0, 255, 0)
        
        leds.show()
        time.sleep(1/fps)

except:
    set_all_off()
    raise