import sys
sys.path.append("..")
from mylibs.env_cliff_pyglet import EnvCliffPyglet
import sarsa_agent

environment = EnvCliffPyglet()
environment.print_info()

agent = sarsa_agent.SarsaAgent(environment)

training_iterations = 10000

for i in range(0, training_iterations):
    agent.main()

environment.reset_score()
agent.run_best_enabled = True

testing_iterations = 10000
for i in range(0, testing_iterations):
    agent.main()

    if environment.render():
        break
    
    print("i = {}, score = {}".format(i, environment.get_score()))

    
    if (i%10) == 0:
        score = environment.get_score()
        environment.label.text = "[SPACE TO EXIT] i = {}, score = {}".format(i, score)
