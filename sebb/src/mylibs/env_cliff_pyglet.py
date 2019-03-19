from libs.libs_env.env_cliff import EnvCliff
from random import random

import pyglet
from pyglet.gl import *
from pyglet.window import key

class EnvCliffPyglet(EnvCliff):
    
    def __init__(self):
        super().__init__()
        self.win = pyglet.window.Window(resizable=True)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.has_exit = False

        self.label = pyglet.text.Label('',
                            font_name='Times New Roman',
                            font_size=20,
                            x=20,
                            y=self.win.height - 40)

        self.win.clear()

    

    def render(self):
        self.win.clear()

        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glPushMatrix()
        glColor3f(0, 0, 0)

        w = self.win.width
        h = self.win.height

        # draw stuff
        for y in range(0, self.height):
            for x in range(0, self.width):
                glPushMatrix()

                # setup maximal dimension
                dim_max = w
                if h < dim_max:
                    dim_max = h

                # calculate xy on screen
                size = dim_max/self.width
                x_ = x*size
                y_ = (self.height - y)*size

                # determine color
                if (y == self.agent_y) and (x == self.agent_x):
                    glColor3f(1.0, 1.0, 0.0)
                elif self.rewards[y][x] < 0.0:
                    glColor3f(1.0, 0.0, 0.0)
                elif self.rewards[y][x] > 0.0:
                    glColor3f(0.0, 1.0, 0.0)
                else:
                    glColor3f(0.5, 0.5, 0.5)
                # draw the rectangle
                self.draw_square(x_, y_, size)

                glPopMatrix()

        glPopMatrix()

        self.label.draw()

        self.win.flip()
        self.win.dispatch_events()
        self.win.push_handlers(self.keys)

        if self.keys[key.SPACE]:
            self.has_exit = True
            self.win.close()
        
        return self.has_exit

    def draw_square(self, x, y, size):
        glPushMatrix()
        glBegin(GL_POLYGON)
        glVertex2f(x, y)
        glVertex2f(x + size, y)
        glVertex2f(x + size, y - size)
        glVertex2f(x, y - size)
        glEnd()
        glPopMatrix()