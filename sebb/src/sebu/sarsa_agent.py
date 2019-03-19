"""
 Q-learning agent coded from scratch
 table is used to store Q values
 state vector is converted to table index into table as idx = argmax(state)

 parameters
 gamma - RL discount factor
 alpha - learning rate
 epsilon_training - probability of choosing random action during training
 epsilon_testing  - probability of choosing random action during testing
"""

import numpy, random

class Agent():
    """!@brief initialise agent
        @param env - environment instance where agent exists
    """
    def __init__(self, env):
        self.env = env
        self.run_best_disable()

    """!@brief main agent action - learning method
        call this in loop, as many iterations as you need

        - this method looks at the observation (env.get_observation())
        - select action
        - execute action env.do_action(action)
        - obtain reward env.get_reward()
        - learn from exepriences

        overload this method with your own - this basic agent
        isn't learning, just selecting random actions
    """
    def main(self):
        action = random.randint(0, self.env.get_actions_count()-1)
        self.env.do_action(action)


    """!@brief set run_best_enabled = True
        usually call after training, before testing
    """
    def run_best_enable(self):
        self.run_best_enabled = True

    """!@brief set run_best_enabled = False
        usually call before training
    """
    def run_best_disable(self):
        self.run_best_enabled = False

    """!@brief return if run_best_enabled
        this can agent use to choose policy - if running in training mode or testing mode
        in training mode is better to choose not only the best actions
        in testing mode (agent trained and deployment) is better to choose the best actions
    """
    def is_run_best_enabled(self):
        return self.run_best_enabled


    """!@brief select action using q_values as probabilities and epsilon as parameter

        @param q_values - list or vector of q_values for each action in current state
        @param epsilon - probability of choosing non best action, value in range <0, 1>
    """
    def select_action(self, q_values, epsilon = 0.1):
        action = self.__argmax(q_values)

        r = numpy.random.uniform(0.0, 1.0)
        if r <= epsilon:
            action = random.randint(0, self.env.get_actions_count()-1)

        return action

    """!@brief private method, return idx where is the highest value of given vector (or list)
        @param v - vector, list or numpy array
    """
    def __argmax(self, v):
        result = 0
        for i in range(0, len(v)):
            if v[i] > v[result]:
                result = i

        return result


#basic Q learning reinforcement learning algorithm
class SarsaAgent(Agent):


    """!@brief initialise agent
        @param env - environment instance where agent exists
    """
    def __init__(self, env):

        #init parent q_tmp
        Agent.__init__(self, env)

        #init Q learning algorithm parameters
        self.gamma      = 0.9
        self.alpha      = 0.2

        #init probabilities of choosing random action
        #different for training and testing
        self.epsilon_training   = 0.1
        self.epsilon_testing    = 0.01

        #init state
        self.state      = 0
        self.state_prev = self.state;

        #init action ID
        self.action      = 0;
        self.action_prev = 0;

        #get state size, and actions count
        self.states_count  = self.env.get_size()
        self.actions_count = self.env.get_actions_count()


        #init Q table, using number of states and actions
        self.q_table = numpy.zeros((self.states_count, self.actions_count))

    """!@brief learning method
        call this in loop, as many iterations as you need

        - this method looks at the observation (env.get_observation())
        - select action, using q_table
        - execute action env.do_action(action)
        - obtain reward env.get_reward()
        - learn from exepriences - fill q_table
    """
    def main(self):

        #choose epsilon - depends on training or testing mode
        if self.is_run_best_enabled():
            epsilon = self.epsilon_testing
        else:
            epsilon = self.epsilon_training

        #QLearning needs to remember current state + action and previous state + action
        self.state_prev = self.state
        self.state      = self.env.get_observation().argmax()

        self.action_prev    = self.action
        #select action is done by probality selection using epsilon
        self.action         = self.select_action(self.q_table[self.state], epsilon)

        #obtain reward from environment
        reward = self.env.get_reward()

        #process Q learning
        # qmax = self.q_table[self.state].max() -> NOPE, max is NOT used in sarsa

        self.q_table[self.state_prev][self.action_prev] = (1.0 - self.alpha)*self.q_table[self.state_prev][self.action_prev] + self.alpha*(reward + self.gamma*self.q_table[self.state][self.action])

        #execute action
        self.env.do_action(self.action)

    #print Q table values
    def print_table(self):
        print(self.q_table)
