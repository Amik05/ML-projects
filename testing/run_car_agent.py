from stable_baselines3 import PPO
from car_lidar_env import CarLidarEnv
import time

# Load trained model
model = PPO.load("ppo_car_lidar")

# Use human render to see it
env = CarLidarEnv(render_mode="human", track_num=2)

obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, _ = env.step(action)
    env.render()
    done = terminated or truncated
    time.sleep(0.02)

env.close()
