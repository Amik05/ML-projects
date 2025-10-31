from stable_baselines3 import PPO
from car_track_env import CarTrackEnv
import pygame, time

env = CarTrackEnv(render_mode="human")
model = PPO.load("ppo_car_track_optimal")

obs, _ = env.reset()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    action, _ = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render()

    if done or truncated:
        obs, _ = env.reset()
        time.sleep(0.3)

env.close()
pygame.quit()
