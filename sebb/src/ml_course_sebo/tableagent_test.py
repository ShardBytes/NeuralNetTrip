import sys
sys.path.append("..")
from mylibs.env_cliff_pyglet import EnvCliffPyglet
from agent_table import QLearningAgent

environment = EnvCliffPyglet()
environment.print_info()

agent = QLearningAgent(environment)

training_iterations = 100000

for i in range(0, training_iterations):
    agent.main()

environment.reset_score()
agent.run_best_enabled = True

testing_iterations = 100000
for i in range(0, testing_iterations):
    agent.main()
    
    if environment.render():
        break

    if (i%10) == 0:
        score = environment.get_score()
        environment.label.text = "i = {}, score = {}".format(i, score)
