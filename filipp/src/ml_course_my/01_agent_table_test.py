#hľadať knižnice o adresár vyššie
import sys
sys.path.append("..")

import libs.libs_env.env_cliff_gui
import tableAgent, sarsaTableAgent
import time

env = libs.libs_env.env_cliff_gui.EnvCliffGui()
agent = tableAgent.TableAgent(env)
#agent = sarsaTableAgent.SarsaTableAgent(env)

env.print_info()

trainingIterations = 10000
for i in range(0, trainingIterations):
    agent.main()
    env.render()

#env.reset_score()

#run the best stuff
testingIterations = 10000
#agent.runBestEnable()

for i in range(0, testingIterations):
    agent.main()
    #time.sleep(0.1)
    env.render()
