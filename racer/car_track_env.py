import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import math

class CarTrackEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode=None):
        super().__init__()
        # Action = [steering, throttle]
        self.action_space = spaces.Box(
            low=np.array([-1.0, 0.0], dtype=np.float32),
            high=np.array([1.0, 1.0], dtype=np.float32),
            dtype=np.float32
        )

        # Observation = normalized state vector
        # [x, y, angle, velocity, dx_to_cp, dy_to_cp]
        self.observation_space = spaces.Box(
            low=np.full((6,), -1.0, dtype=np.float32),
            high=np.full((6,), 1.0, dtype=np.float32),
            dtype=np.float32
        )

        # Rendering
        self.render_mode = render_mode
        self.W, self.H = 800, 600
        self.car_size = (20, 10)
        self.track_width = 60

        if render_mode == "human":
            pygame.init()
            self.screen = pygame.display.set_mode((self.W, self.H))
            self.clock = pygame.time.Clock()

        # Smoother 12-point track
        self.track_points = [
            (100, 300), (200, 200), (300, 150), (400, 150),
            (500, 150), (600, 200), (700, 300), (600, 400),
            (500, 450), (400, 450), (300, 450), (200, 400)
        ]
        self.num_checkpoints = len(self.track_points)
        self.reset()

    # ----------------------------------------------------------
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.car_pos = np.array(self.track_points[0], dtype=np.float32)
        vec = np.array(self.track_points[1]) - self.car_pos
        self.car_angle = math.atan2(vec[1], vec[0])
        self.vel = 0.0
        self.current_cp = 1
        self.steps = 0
        self.prev_dist = self._distance_to_cp()
        return self._get_obs(), {}

    # ----------------------------------------------------------
    def step(self, action):
        steer, throttle = action
        self.car_angle += steer * 0.07
        self.vel = np.clip(self.vel + (throttle - 0.5) * 0.15, 0, 5)

        prev_pos = self.car_pos.copy()
        self.car_pos += np.array([math.cos(self.car_angle), math.sin(self.car_angle)]) * self.vel
        self.steps += 1

        next_cp = np.array(self.track_points[self.current_cp])
        dist_to_cp = np.linalg.norm(next_cp - self.car_pos)
        progress = self.prev_dist - dist_to_cp
        self.prev_dist = dist_to_cp

        # --- Reward shaping ---
        reward = 0.0
        reward += 0.05 * self.vel                     # encourage forward motion
        reward += 0.3 * progress                      # reward getting closer to next CP
        reward -= 0.01                                # small time penalty

        # Checkpoint reached
        if dist_to_cp < 20:
            reward += 10
            self.current_cp = (self.current_cp + 1) % self.num_checkpoints
            self.prev_dist = self._distance_to_cp()

        # Off-track penalty
        if not self._on_track(self.car_pos):
            reward -= 50
            done = True
        else:
            done = False

        # Timeout
        if self.steps > 2000:
            done = True

        if self.render_mode == "human":
            self.render()

        return self._get_obs(), reward, done, False, {}

    # ----------------------------------------------------------
    def _distance_to_cp(self):
        return np.linalg.norm(np.array(self.track_points[self.current_cp]) - self.car_pos)

    def _on_track(self, pos):
        min_dist = float("inf")
        for i in range(len(self.track_points)):
            p1 = np.array(self.track_points[i])
            p2 = np.array(self.track_points[(i + 1) % len(self.track_points)])
            min_dist = min(min_dist, self._dist_point_segment(pos, p1, p2))
        return min_dist < self.track_width / 2

    @staticmethod
    def _dist_point_segment(p, a, b):
        ap, ab = p - a, b - a
        t = np.clip(np.dot(ap, ab) / np.dot(ab, ab), 0, 1)
        closest = a + t * ab
        return np.linalg.norm(p - closest)

    # ----------------------------------------------------------
    def _get_obs(self):
        next_cp = np.array(self.track_points[self.current_cp])
        dx, dy = next_cp - self.car_pos
        obs = np.array([
            self.car_pos[0] / self.W * 2 - 1,
            self.car_pos[1] / self.H * 2 - 1,
            math.sin(self.car_angle),
            math.cos(self.car_angle),
            self.vel / 5.0,
            dx / self.W, dy / self.H
        ], dtype=np.float32)
        return obs[:6]  # 6 values (normalized)

    # ----------------------------------------------------------
    def render(self):
        self.screen.fill((20, 20, 20))
        pygame.draw.lines(self.screen, (60, 60, 60), True, self.track_points, self.track_width)

        for i, cp in enumerate(self.track_points):
            color = (0, 255, 0) if i == self.current_cp else (80, 80, 80)
            pygame.draw.circle(self.screen, color, cp, 6)

        car_rect = pygame.Rect(0, 0, *self.car_size)
        car_rect.center = self.car_pos
        pygame.draw.rect(self.screen, (255, 50, 50), car_rect)
        pygame.display.flip()
        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.render_mode == "human":
            pygame.quit()
