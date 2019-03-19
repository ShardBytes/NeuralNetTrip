import sys
sys.path.append("..")
import libs.libs_env.env_cliff_gui
import tableagent

environment = libs.libs_env.env_cliff_gui.EnvCliffGui()
environment.print_info()

agent = tableagent.QLearningAgentTable(environment)

training_iterations = 100000

for i in range(0, training_iterations):
    agent.main()

environment.reset_score()
agent.run_best_enabled = True

testing_iterations = 100000
for i in range(0, testing_iterations):
    agent.main()
    environment.render()


    if (i%1000) == 0:
        score = environment.get_score()
        print("i = {}, score = {}".format(i, score))
