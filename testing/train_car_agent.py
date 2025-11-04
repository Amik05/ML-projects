from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from car_lidar_env import CarLidarEnv

# Create env (no render for faster training)
env = CarLidarEnv(render_mode='human')

# Check compatibility
check_env(env, warn=True)

# Define PPO model
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=3e-4,
    batch_size=64,
    n_steps=1024,
    gamma=0.99,
)

# Train agent
model.learn(total_timesteps=10_000)

# Save model
model.save("ppo_car_lidar")

env.close()
