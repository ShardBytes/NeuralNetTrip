#Dummy agent
#by me, plajdo, hey

import random
import numpy

class Agent():

    #počiatočné akcie & stavy - environment
    #nastaviť parametre triedy
    def __init__(self, environment):
        self.environment = environment
        self.runBestDisable()

    #vnútorný main, počíta sa tu rovnica & everything
    #napr. výber akcie
    def main(self):
        action = random.randint(0, self.environment.get_actions_count() - 1)
        self.environment.do_action(action)

    #prepínanie medzi tréningovým a run módom
    def runBestEnable(self):
        self.runBestEnabled = True

    def runBestDisable(self):
        self.runBestEnabled = False

    def isBestRunEnabled(self):
        return self.runBestEnabled

    #yes
    #self-explanatory
    def getMaxArrayElementIndex(self, array):
        maxValueIndex = 0
        for i in range(0, len(array)):
            if(array[i] > array[maxValueIndex]):
                maxValueIndex = i


        return maxValueIndex

    #epsilon je variabilnosť rozhodnutí, 0 = najlepšie akcie, nenulový = "prieskum prostredia", vyberá aj horšie akcie
    def selectAction(self, qValues, epsilon = 0.1):
        action = self.getMaxArrayElementIndex(qValues)
        rnd = numpy.random.uniform(0.0, 1.0)

        if rnd <= epsilon:
            action = random.randint(0, self.environment.get_actions_count() - 1)

        return action
