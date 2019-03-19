import sys
sys.path.append("..")
from mylibs.env_cliff_pyglet import EnvCliffPyglet
from agent_table import QLearningAgent

environment = EnvCliffPyglet()
environment.print_info()
agent = QLearningAgent(environment)

def train():
    print("TRAINING THE AGENT...")
    environment.reset_score()
    environment.label.text = "Training agent ..."
    agent.run_best_enabled = False # switch to training
    while True:
        agent.main()
        
        if environment.render():
            break

def test():
    print("TESTING TRAINED AGENT...")
    testing_active = True

    environment.reset_score()
    environment.has_exit = False
    environment.print_info()
    agent.run_best_enabled = True # switch to testing

    i = 0
    while testing_active:
        i += 1

        agent.main()

        if environment.render():
            break
        
        if (i%10) == 0:
            score = environment.get_score()
            environment.label.text = "TRAINED [SPACE TO EXIT] i = {}, score = {}".format(i, score)


train()
test()