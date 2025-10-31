import pygame
import numpy as np
from car_track_env import CarTrackEnv

# Create the environment in human render mode
env = CarTrackEnv(render_mode="human")
obs, _ = env.reset()

# Pygame key controls
# ↑ / W = throttle up
# ↓ / S = brake (reverse throttle)
# ← / A = steer left
# → / D = steer right

print("Use arrow keys or WASD to drive. Press ESC to quit.")

running = True
while running:
    # Handle events (quit + keypress)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()

    # Initialize action
    steer = 0.0
    throttle = 0.5  # neutral (0.5 means no acceleration)
    
    # Steering
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        steer = -1.0
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        steer = 1.0

    # Throttle control
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        throttle = 1.0   # accelerate
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        throttle = 0.0   # brake

    # Step environment
    action = np.array([steer, throttle], dtype=np.float32)
    obs, reward, done, truncated, info = env.step(action)
    env.render()

    if done:
        obs, _ = env.reset()

env.close()
