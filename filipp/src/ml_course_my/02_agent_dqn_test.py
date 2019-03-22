import sys
sys.path.append("..")

import libs.libs_env.env_pong
import libs.libs_env.env_cliff_gui
import libs.libs_env.env_arkanoid
import agent
import dqnAgent

environment = libs.libs_env.env_pong.EnvPong()
#environment = libs.libs_env.env_cliff_gui.EnvCliffGui()
#environment = libs.libs_env.env_arkanoid.EnvArkanoid()
environment.print_info()

agent = dqnAgent.DQNAgent(environment, "pong_network.json")

training_iterations = 50000

for i in range(0, training_iterations):
    agent.main()
    if not i % 10:
        print("Progress: ", 100.0 * i / training_iterations, "%, Score: ", environment.get_score())

environment.reset_score()
agent.runBestEnable()

print("Training done")
print("Testing...")

testing_iterations = 10000
for i in range(0, testing_iterations):
    agent.main()

print("Testing done")
print("Score achieved: ", environment.get_score())

while True:
    agent.main()
    environment.render()
