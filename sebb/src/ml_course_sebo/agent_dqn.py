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

    # process method for network
    def main(self):

        if self.is_run_best_enabled():
            epsilon = self.epsilon_testing
        else:
            epsilon = self.epsilon_training
            self.epsilon_training *= self.epsilon_decay # decay epsilon

        state = self.env.get_observation()
        state_vector = dqn.VectorFloat(self.env.get_size())

        for i in range(0, state_vector.size()):
            state_vector[i] = state[i]

        # compute the q values
        self.deep_q_network.compute_q_values(state_vector)
        q_values = self.deep_q_network.get_q_values()

        self.action = self.select_action(q_values, epsilon)
        self.env.do_action(self.action)

        # pouc sa z chyb
        self.reward = self.env.get_reward()

        # plnenie buffera
        if self.env.is_done():
            self.deep_q_network.add_final(state_vector, q_values, self.action, self.reward)
        else:
            self.deep_q_network.add(state_vector, q_values, self.action, self.reward)

        # plny buffer
        if self.deep_q_network.is_full() and not self.run_best_enabled:
            self.deep_q_network.learn()

    # citanie a ukladanie
    def save(self, file_name_prefix):
        self.deep_q_network.save(file_name_prefix)

    def load(self, file_name):
        self.deep_q_network.load_weights(file_name)
