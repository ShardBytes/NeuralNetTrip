"""
Retardovany agent.
by Plasmoxy
"""

import random, numpy

class Agent:

    # v konstruktore dostane prostredie, aky je pociatocny stav, kolko akcii etc
    def __init__(self, environment):
        self.environment = environment
        self.run_best_enabled = False # trenovaci (nahodnost aj) / ostro (full)

    # main metoda, tu sa deju vzorce
    def main(self):
        action = random.randint(0, self.environment.get_actions_count() - 1)
        self.environment.do_action(action)

    # run_best_enable, run_best_disable, is_run_best_enabled -> atribut

    # nejake pole, da nam na akom indexe sa nachadza najvacsi prvok
    def argmax(self, arr):
        jmax = 0
        for i in range(0, len(arr)):
            if arr[i] > arr[jmax]:
                result = i
        return jmax

    # epsilon sluzi na preskumavanie prostredia
    def select_action(self, q_values, epsilon = 0.1):
        # vyberiem najvyssie q
        action = self.argmax(q_values)
        r = numpy.random.uniform(0.0, 1.0)

        if r <= epsilon:
            action = random.randint(0, self.environment.get_actions_count() - 1)

        return action
