import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
import random
import time
from tqdm import tqdm  # Progress bar


env = gym.make('Taxi-v3')

alpha = 0.9 # learning rate, step size
gamma = 0.9 # discount factor, long term
epsilon = 1.0 # exploration rate, 
epsilon_decay = 0.9995
min_epsilon = 0.1
num_episodes = 10000
max_steps = 100

q_table = np.zeros((env.observation_space.n, env.action_space.n))

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample()
    else:
        return np.argmax(q_table[state, :])
    
for episode in tqdm(range(num_episodes)):
    state, _ = env.reset()

    done = False

    for step in range(max_steps):
        action = choose_action(state)

        next_state, reward, done, truncated, info = env.step(action)

        # update Q-table
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state, :])

        q_table[state, action] = (1 - alpha) * old_value + alpha * (reward + gamma * next_max) 

        state = next_state

        if done or truncated:
            break

    # decay epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay )
env.close() 

# Test the agent
env = gym.make('Taxi-v3', render_mode='rgb_array')


for episode in range(5):

    state, _ = env.reset()

    done = False

    print(f'Episode {episode + 1}')

    for step in range(max_steps):
        # rendering
        frame = env.render()
        plt.imshow(frame)
        plt.axis("off")
        plt.show(block=False)
        plt.pause(0.2)
        plt.clf()

        # Action based on Q-table
        action = np.argmax(q_table[state, :])
        next_state, reward, done, truncated, info = env.step(action)
        state = next_state

        if done or truncated:
            break

env.close()