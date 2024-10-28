from ..models.effect import Effect


class TextScroll2D(Effect):
    def __init__(self, leds, positions, color_list, duration=1, fps=60):
        super().__init__(leds, positions, color_list, duration, fps)

        self.direction = direction

    def setup(self):
        '''Run at the start of the effect'''
        self.min_x = min(self.positions, key=lambda x: x[0])[0]
        self.max_x = max(self.positions, key=lambda x: x[0])[0]
        self.min_y = min(self.positions, key=lambda x: x[1])[1]
        self.max_y = max(self.positions, key=lambda x: x[1])[1]

        self.x_rel = (self.positions[:, 0] - self.min_x) / (self.max_x - self.min_x)
        self.y_rel = (self.positions[:, 1] - self.min_y) / (self.max_y - self.min_y)

        self.effect_progress = 0  # goes from 0 to 1

        # self.directions = ['x', 'y']
        # self.direction = random.choice(self.directions)

    def draw(self):
        '''Run every frame'''

        if self.effect_progress >= 1:
            self.effect_progress = 0
            # self.direction = random.choice(self.directions)

        # Set each LED to the right colour
        for i in range(len(self.leds)):

            # Get the LED position
            x, y = self.positions[i]

            if self.direction == 'x':
                # ----- left/right wave -----
                # Relative x position
                p = self.x_rel[i]

            if self.direction == 'y':
                # ----- front/back wave -----
                # Relative y position
                p = self.y_rel[i]

            # Skip if p is nan
            if np.isnan(p):
                continue

            # p is the increase in progress for the current pixel
            # Calculate the color
            color = get_color_in_sequence(
                self.color_list,
                (self.effect_progress + p) % 1
            )

            # Set the colour
            self.leds[i] = color

        # Increment the effect progress
        self.effect_progress += 1 / (self.duration * self.fps)
