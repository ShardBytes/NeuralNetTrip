import sys
sys.path.append("..")
import libs.libs_env.env_birds
import agent_dqn

environment = libs.libs_env.env_birds.EnvBirds()
#environment.print_info()

agent = agent_dqn.DQNAgent(environment, "flappy_network.json")

training_iterations = 100000

for iteration in range(0, training_iterations):
    agent.main()
    if iteration%100 == 0:
        print(iteration*100.0/training_iterations, environment.get_score())

environment.reset_score()
agent.run_best_enabled = True

testing_iterations = 10000
for iteration in range(0, testing_iterations):
    agent.main()
    environment.render()
    
    if iteration%100 == 0:
        print(iteration*100.0/training_iterations, environment.get_score())
