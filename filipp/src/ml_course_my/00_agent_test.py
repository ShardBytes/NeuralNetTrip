#hľadať knižnice o adresár vyššie
import sys
sys.path.append("..")

import libs.libs_env.env_cliff_gui
import agent
import time

env = libs.libs_env.env_cliff_gui.EnvCliffGui()
agent = agent.Agent(env)

env.print_info()

trainingIterations = 1
for i in range(0, trainingIterations):
    agent.main()

#in case something fucks up during training
env.reset_score()

#run the best stuff
testingIterations = 10000
agent.runBestEnable()

for i in range(0, testingIterations):
    agent.main()
    time.sleep(0.1)
    env.render()
