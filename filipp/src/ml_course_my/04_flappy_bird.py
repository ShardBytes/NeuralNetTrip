#hľadať knižnice o adresár vyššie
import sys
sys.path.append("..")

import libs.libs_env.env_bird
import dqnAgent
import time

env = libs.libs_env.env_bird.EnvBird()
agent = dqnAgent.DQNAgent(env, "flappy_bird_net.json")

env.print_info()

trainingIterations = 10000
for i in range(0, trainingIterations):
    agent.main()

env.reset_score()

#run the best stuff
testingIterations = 10000
agent.runBestEnable()

for i in range(0, testingIterations):
    agent.main()
    print(env.get_score())
    env.render()
