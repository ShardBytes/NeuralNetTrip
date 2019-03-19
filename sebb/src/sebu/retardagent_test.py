import sys
sys.path.append("..")
import libs.libs_env.env_cliff_gui
import retardagent

environment = libs.libs_env.env_cliff_gui.EnvCliffGui()
environment.print_info()

agent = retardagent.Agent(environment)

training_iterations = 10000

for i in range(0, training_iterations):
    agent.main()

environment.reset_score()
agent.run_best_enabled = True

testing_iterations = 10000
for i in range(0, testing_iterations):
    agent.main()
    #environment.render()


    if (i%1000) == 0:
        score = environment.get_score()
        print("i = {}, score = {}".format(i, score))
