import gymnasium as gym

#create env
env = gym.make("CartPole-v1", render_mode="human")

obersvation, info = env.reset()

# Example output: [ 0.01234567 -0.00987654  0.02345678  0.01456789]
# [cart_position, cart_velocity, pole_angle, pole_angular_velocity]
print(f"Starting obersvation: {obersvation}")

episode_over = False
total_reward = 0

while not episode_over:
    action = env.action_space.sample()  # chose a random action

    observation, reward, terminated, truncated, info = env.step(action)

    total_reward += reward
    episode_over = terminated or truncated

print(f"Episode finished! Total reward: {total_reward}")

# print(f"Action space: {env.action_space}")
# print(f"Sample Action space: {env.action_space.sample()}")

# print(f"Obseravation space: {env.observation_space}")
# print(f"Sample Obseravation space: {env.observation_space.sample()}")

env.close()