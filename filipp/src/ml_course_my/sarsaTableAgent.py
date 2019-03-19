import agent
import numpy

class SarsaTableAgent(agent.Agent):
    def __init__(self, environment, gamma = 0.9, epsilon_training = 0.35, epsilon_testing = 0.35, learning_factor = 0.15): #35% chance to mess up
        super().__init__(environment)

        #gamma = farming rate (cycle)
        self.gamma = gamma
        self.epsilon_training = epsilon_training
        self.epsilon_testing = epsilon_testing
        self.learning_factor = learning_factor

        self.state = 0
        self.previous_state = self.state

        self.action = 0
        self.previous_action = self.action

        self.action_count = self.environment.get_actions_count()
        self.state_count = self.environment.get_size() #počet stavov je v tomto prípade veľkosť herného poľa (4*8*1 = 32)

        self.qTable = numpy.zeros((self.state_count, self.action_count)) #prázdna tabuľka Q hodnôt

    #virtual main
    #keď vytvoríme inštanciu tableAgent.TableAgent, tento main "prebije" main z agent.Agent
    def main(self):
        if(self.isBestRunEnabled()):
            epsilon = self.epsilon_testing
        else:
            epsilon = self.epsilon_training

        #posunúť akciu a stav dozadu a zistiť noú akciu a stav

        #vyjadriť aktuálny stav číslom
        #self.state = self.env.get_observation() <--- "nepoctivý" spôsob
        self.previous_state = self.state

        #observation v tomto prípade je [0, 0, 1, 0, 0, 0, 0, 0, ...] = index najvyššieho čísla je pozícia na mape
        #
        #environment je narezaná mapa s pozíciami jednotliých hráčov
        #napríklad 1 matrix s 0 a 1 s pozíciami všetkých pešiakov v šachu
        #potom ďalší matrix s 0 a 1 s pozíciami všetkých strelcov v šachu
        #...
        #môže to byť náročná operácia, hlavne pri hrách s veľa objektami
        #napríklad taký Starcraft
        #
        self.state = self.environment.get_observation().argmax() #toto je numpy metóda!

        self.previous_action = self.action
        self.action = self.selectAction(self.qTable[self.state], epsilon)

        reward = self.environment.get_reward()

        #učenie
        #learning factor
        remembered_stuff = (1.0 - self.learning_factor) * self.qTable[self.previous_state][self.previous_action]
        new_stuff = self.learning_factor * (reward + self.gamma * self.qTable[self.state][self.action]) #not the best possible scenario, take in all scenarios

        self.qTable[self.previous_state][self.previous_action] = remembered_stuff + new_stuff

        self.environment.do_action(self.action)
