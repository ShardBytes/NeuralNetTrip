from mylibs.env_cliff_empty import EnvCliffEmpty
from random import random

import pyglet
from pyglet.gl import *
from pyglet.window import key

class EnvCliffPyglet(EnvCliffEmpty):
    
    def __init__(self):
        super().__init__()
        self.win = pyglet.window.Window(resizable=True)
        self.has_exit = False

        # setup maximal dimension
        dim_max = self.win.width
        if self.win.height < dim_max:
            dim_max = self.win.height

        # calculate pixel size of one square
        self.size = dim_max/self.width

        self.label = pyglet.text.Label('',
                            font_name='Times New Roman',
                            font_size=20,
                            x=20,
                            y=self.win.height - 40)

        self.win.clear()

        # setup events using decorators of window

        @self.win.event
        def on_mouse_press(x, y, button, modifiers):
            # get x,y in q matrix
            qx = int(x*1.0/self.size)
            qy = self.height - int(y*1.0/self.size) - 1

            # add reward to environment
            self.rewards[qy][qx] = -1.0 + abs(self.rewards[qy][qx])
            self.reset_score()

        @self.win.event
        def on_key_press(keycode, modifiers):
            if keycode == key.SPACE:
                self.has_exit = True
    

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

                # calculate xy on screen
                x_ = x*self.size
                y_ = (self.height - y)*self.size

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
                self.draw_square(x_, y_, self.size)

                glPopMatrix()

        glPopMatrix()

        self.label.draw()

        self.win.flip()
        self.win.dispatch_events()

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