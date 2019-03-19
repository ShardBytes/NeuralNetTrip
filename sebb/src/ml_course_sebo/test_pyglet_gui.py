import sys
sys.path.append("..")
from libs.libs_env.env_cliff_pyglet import EnvCliffPyglet

env = EnvCliffPyglet()

while not env.render():
    pass