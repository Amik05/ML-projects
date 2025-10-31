from stable_baselines3 import PPO
from car_track_env import CarTrackEnv

env = CarTrackEnv()  # headless for training
model = PPO(
    "MlpPolicy", env,
    verbose=1,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=128,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2
)

print("🚀 Training...")
model.learn(total_timesteps=1_000_000)
model.save("ppo_car_track_optimal")
env.close()
print("✅ Done! Run watch_trained_car.py to visualize.")
