import libs.libs_env.env as env
import libs.libs_gl_gui.gl_gui as gl_gui

import numpy
import time
import random

class EnvBird(env.Env):
    def __init__(self):
        super().__init__()

        self.width = 1
        self.height = 1
        self.depth = 3

        self.reset()

        self.gui = gl_gui.GLVisualisation()

    def reset(self):

        rnd = random.random() * 0.5 + 0.25

        self.s = rnd  #parrot vertical position
        self.v = 0.0  #vertical velocity (?)

        self.observation = numpy.zeros(self.get_size())

        self.actions_count = 2 #jump or not jump :thinking:
        self.hole_x = 1.0
        self.hole_y = 0.5
        self.hole_width = 0.25 #1.0 / 4.0

        self.dt = 0.01

    def do_action(self, action):
        print(action)
        action = 0
        if action == 0:
            acc = 0.0
        else:
            #acc = self.fa / self.m #a = F / m
            acc = 0.002 + 0.01

        wind = 0.0
        if random.randint(0, 100) < 10.0:
            wind = (random.random() - 0.5) * 0.01

        self.s = self.s + self.v * self.dt + wind
        self.v = self.v + (acc - 0.001)

        self.v = self.clamp(self.v, -1.0, 1.0)
        self.s = self.clamp(self.s, 0.0, 1.0)

        self.observation[0] = self.s
        self.observation[1] = self.v

        self.reward = -1.0
        if abs(self.s - 0.5) < 0.1:
            self.reward = 2.0

        if self.s >= 1.0 or self.s <= 0.0:
            self.reward = -10.0
            self.set_terminal_state()
            self.reset()

        self.next_move()

    def new_hole(self):
        self.hole_x = 1.0
        self.hole_y = random.random() * 0.5 + 0.25

    def render_hole(self):
        y_top = (1 - (self.hole_y + 0.125)) / 2.0
        height_top = 1.0 - self.hole_y + 0.125

        y_bottom = (self.hole_y - 0.125) / 2.0
        height_bottom = self.hole_y - 0.125

        self.gui.push()
        self.gui.set_color(0.0, 0.8, 0.0)
        self.gui.translate(0.0, y_top, 0.0)
        self.gui.paint_rectangle(0.1, height_top)
        self.gui.pop()

        self.gui.push()
        self.gui.set_color(0.0, 0.8, 0.0)
        self.gui.translate(0.0, y_bottom, 0.0)
        self.gui.paint_rectangle(0.1, height_bottom)
        self.gui.pop()

    def render(self):
        self.gui.init("Flappy bird")
        self.gui.start() #clear buffers

        #sky
        self.gui.push()
        self.gui.translate(0.0, 0.0, -0.01)
        self.gui.set_color(0.0, 0.8, 0.8)
        self.gui.paint_square(2.0)
        self.gui.pop()

        #parrot
        player_x = 0.0
        player_y = self.s * 2.0 - 1.0
        self.gui.push()
        self.gui.translate(player_x, player_y, 0.0)
        self.gui.set_color(1.0, 0.5, 0.0)
        self.gui.paint_square(0.1)
        self.gui.pop()

        self.gui.finish() #swap buffers after drawing

    def clamp(self, number, low, high):
        if number > high:
            return high
        elif number < low:
            return low
        return number
