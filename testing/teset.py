from car_lidar_env import CarLidarEnv

env = CarLidarEnv(render_mode="human")
obs, _ = env.reset()
print("Observation:", obs)
env.close()
