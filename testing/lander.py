import gymnasium as gym

# init env
env = gym.make("LunarLander-v3", render_mode="human")

# reset env
observation, info = env.reset(seed=42)

for i in range(1000):
    action =  env.action_space.sample()

    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset() 
env.close()
