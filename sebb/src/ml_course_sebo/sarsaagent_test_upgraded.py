import sys
sys.path.append("..")
from mylibs.env_cliff_pyglet import EnvCliffPyglet
import sarsa_agent

environment = EnvCliffPyglet()
environment.print_info()
agent = sarsa_agent.SarsaAgent(environment)

TRAINING_ITERATIONS = 10000
TRAINING_RENDERING_ENABLED = True

def train():
    print("TRAINING THE AGENT...")
    environment.reset_score()
    environment.label.text = "Training agent ..."
    agent.run_best_enabled = False # switch to training
    for i in range(0, TRAINING_ITERATIONS):
        agent.main()
        
        if TRAINING_RENDERING_ENABLED:
            if environment.render():
                break

def test():
    print("TESTING...")
    testing_active = True

    environment.reset_score()
    agent.run_best_enabled = True # switch to testing

    i = 0
    while testing_active:
        i += 1

        agent.main()

        if environment.render():
            break
        
        if (i%10) == 0:
            score = environment.get_score()
            environment.label.text = "[SPACE TO EXIT] i = {}, score = {}".format(i, score)


train()