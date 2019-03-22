import libs.libs_env.env as libs_env
import libs.libs_gl_gui.gl_gui as libs_gl_gui

import numpy
import time
import random

class EnvBirds(libs_env.Env):

    def __init__(self):
        super().__init__()

        # state vector
        self.width = 1
        self.height = 1
        self.depth = 3
        self.actions_count = 2 # jump and do_nothing
        self.observation = numpy.zeros(self.get_size())

        self.reset()
        self.gui = libs_gl_gui.GLVisualisation()

    def reset(self):

        rnd = random.random()*0.5 + 0.25

        self.s = rnd # position (height)
        self.v = 0.0 # vertical velocity

        self.new_hole()

    def do_action(self, action):

        dt = 0.01

        if action == 0:
            acc = 0.0 # acceleration
        else:
            acc = 0.002 + 0.00001

        wind = 0.0
        if random.randint(0, 100) < 10:
            wind = (random.random() - 0.5)*0.01

        self.s = self.s + self.v*dt + wind
        self.v = self.v + (acc - 0.001)

        if self.v > 1.0:
            self.v = 1.0

        if self.v < -1.0:
            self.v = -1.0

        if self.s > 1.0:
            self.s = 1.0

        if self.s < 0.0:
            self.s = 0.0

        self.observation[0] = self.s
        self.observation[1] = self.v

        #self.reward = - abs(self.s - 0.5) + 0.1
        self.reward = 0.0
        center_distance = abs(self.s - 0.5)

        if center_distance < 0.2:
            self.reward = 2.0

        # punish
        if self.s >= 1.0 or self.s <= 0.0:
            self.reward = -1.0
            self.set_terminal_state()
            self.reset()

        self.next_move()

    def new_hole(self):
        self.hole_x = 1.0
        self.hole_y = random.random()*0.5 + 0.25

    def render_hole(self):
        y_top = 1 - (self.hole_y + 0.125)/2.0
        height_top = 1.0 - self.hole_y + 0.125

        y_bottom = (self.hole_y - 0.125)/2.0
        height_bottom = self.hole_y - 0.125


        g = self.gui
        g.push()
        g.set_color(0.0, 0.8, 0.0)

        g.translate(0.0, y_top, 0.0)
        g.paint_rectangle(0.1, height_top)

        g.translate(0.0, y_bottom, 0.0)
        g.paint_rectangle(0.1, height_bottom)

        g.pop()

    def render(self):
        g = self.gui
        g.init("flappy birds")
        g.start()

        g.push()
        g.translate(0.0, 0.0, -0.01)
        g.set_color(0.0, 0.0, 0.8)
        g.paint_square(3.0)
        g.pop()

        player_x = -1.0
        player_y = self.s*2.0 - 1.0

        g.push()
        g.translate(player_x, player_y, 0.0)
        g.set_color(1.0, 1.0, 0.0)
        g.paint_square(0.1)
        g.pop()

        self.render_hole()

        g.finish()
