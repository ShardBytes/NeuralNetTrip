import numpy
from agent import Agent

import sys
sys.path.append("..")

import libs.libs_dqn_python_cpu.dqn as dqn


class DQNAgent(Agent):

    # treba mu aj config subor
    def __init__(self, env, config_filename, epsilon_training = 0.2, epsilon_testing = 0.01, epsilon_decay = 1.0):
        super().__init__(env)

        geometry = dqn.sGeometry()
        geometry.w = self.env.width
        geometry.h = self.env.height
        geometry.d = self.env.depth

        self.deep_q_network = dqn.DQN(config_filename, geometry, self.env.get_actions_count())

        self.epsilon_training = epsilon_training
        self.epsilon_testing = epsilon_testing
        self.epsilon_decay = epsilon_decay
