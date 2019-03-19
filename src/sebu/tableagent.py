import retardagent, numpy

class QLearningAgentTable(retardagent.Agent):

    def __init__(self, environment, gama = 0.9, epsilon_training = 0.3, epsilon_testing = 0.1):
        super().__init__(environment)
        self.gama = gama
        self.alpha = 0.2
        self.epsilon_training = epsilon_training
        self.epsilon_testing = epsilon_testing

        self.state = 0 # s'
        self.state_previous = self.state # s

        self.action = 0 # a'
        self.action_previous = self.action # a

        self.actions_count = self.environment.get_actions_count() # = 4
        self.states_count = self.environment.get_size() # = 32

        self.q_table = numpy.zeros((self.states_count, self.actions_count)) # matica 32x4


    def main(self):
        if self.run_best_enabled:
            epsilon = self.epsilon_testing
        else:
            epsilon = self.epsilon_training

        self.state_prev = self.state
        self.state = self.environment.get_observation().argmax()

        self.action_previous = self.action
        self.action = self.select_action(self.q_table[self.state], epsilon)

        reward = self.environment.get_reward()

        q_tmp = self.q_table[self.state].max()
        d = reward + self.gama*q_tmp - self.q_table[self.state_previous][self.action_previous]

        self.q_table[self.state_previous][self.action_previous] += self.alpha*d

        self.environment.do_action(self.action)
