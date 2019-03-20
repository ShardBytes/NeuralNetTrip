#table agent example with opengl GUI
#learn avoid the cliff
#try to compare Q-learning and SARSA trajectory results

import sys
sys.path.append("..") # Adds higher directory to python modules path.

import libs.libs_env.env_pong
import agent
import agent_dqn

#init cliff environment
env = libs.libs_env.env_pong.EnvPong()

#print environment info
env.print_info()

#init Q Learning agent
#agent = agent.Agent(env)
agent = agent_dqn.DQNAgent(env, "pong_network.json")

#init sarsa agent
#agent = libs_agent.agent_table.SarsaAgent(env)

#process training
training_iterations = 100000

for iteration in range(0, training_iterations):
    agent.main()
    #print training progress %, ane score, every 100th iterations
    if iteration%100 == 0:
        print("Progress = ", iteration*100.0/training_iterations, "%  ", "score = ", env.get_score())

print("DONE LEARNING")

#reset score
env.reset_score()
agent.run_best_enable()

print("TESTING ...")

for iteration in range(0, 10000):
    agent.main()

print("testing score = ", env.get_score())

#for iteration in range(0, 2000):
while True:
    agent.main()
    env.render()

print("program done")
print("move=", env.get_move(), " score=",env.get_score())
