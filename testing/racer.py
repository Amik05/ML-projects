import pygame
import math
pygame.init()

# --- Screen setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Track with Lidar Sensors")

clock = pygame.time.Clock()

# --- Load assets ---
track = pygame.image.load("track2.png").convert()
track = pygame.transform.scale(track, (WIDTH, HEIGHT))

car_image = pygame.image.load("car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (35, 30))
car_w, car_h = car_image.get_size()

# --- Car properties ---
x, y = 400, 500
angle = 0
velocity_x, velocity_y = 0, 0
acceleration = 0.25
friction = 0.05
turn_speed = 4
max_speed = 8

def get_rotated_hitbox(center_x, center_y, width, height, angle_deg):
    """Return 4 corner points (x, y) of the rotated rectangle."""
    rad = math.radians(-angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    hw, hh = width / 2, height / 2
    corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    rotated = []
    for cx, cy in corners:
        rx = center_x + (cx * cos_a - cy * sin_a)
        ry = center_y + (cx * sin_a + cy * cos_a)
        rotated.append((rx, ry))
    return rotated

def check_collision(corners, track_surface):
    """Return True if any corner touches black pixels (walls)."""
    for (cx, cy) in corners:
        if 0 <= cx < WIDTH and 0 <= cy < HEIGHT:
            color = track_surface.get_at((int(cx), int(cy)))[:3]
            if color <= (100, 100, 100):  # black wall
                return True
    return False

def cast_lidar(center_x, center_y, angle_deg, track_surface, max_distance=250, step=2):
    """Cast one lidar ray and return the hit point and distance."""
    rad = math.radians(-angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    for dist in range(0, max_distance, step):
        cx = int(center_x + cos_a * dist)
        cy = int(center_y + sin_a * dist)
        if 0 <= cx < WIDTH and 0 <= cy < HEIGHT:
            color = track_surface.get_at((cx, cy))[:3]
            if color <= (100, 100, 100):
                return (cx, cy), dist
    return (int(center_x + cos_a * max_distance), int(center_y + sin_a * max_distance)), max_distance

def get_lidar_readings(x, y, angle, track_surface):
    """Get multiple lidar distances around the car."""
    lidar_angles = [-60, -30, 0, 30, 60]  # relative to car direction
    readings = []
    for a in lidar_angles:
        point, dist = cast_lidar(x, y, angle + a, track_surface)
        readings.append(dist)
        pygame.draw.line(screen, (0, 0, 250), (x, y), point, 2)
        pygame.draw.circle(screen, (255, 0, 0), point, 3)
    return readings

# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        angle += turn_speed
    if keys[pygame.K_d]:
        angle -= turn_speed
    if keys[pygame.K_w]:
        velocity_x += math.cos(math.radians(angle)) * acceleration
        velocity_y -= math.sin(math.radians(angle)) * acceleration
    if keys[pygame.K_s]:
        velocity_x -= math.cos(math.radians(angle)) * acceleration / 2
        velocity_y += math.sin(math.radians(angle)) * acceleration / 2

    # Limit speed
    speed = math.sqrt(velocity_x**2 + velocity_y**2)
    if speed > max_speed:
        scale = max_speed / speed
        velocity_x *= scale
        velocity_y *= scale

    # Apply friction
    velocity_x *= (1 - friction)
    velocity_y *= (1 - friction)

    # Predict next position
    next_x = x + velocity_x
    next_y = y + velocity_y
    corners = get_rotated_hitbox(next_x, next_y, car_w, car_h, angle)

    if check_collision(corners, track):
        print("💥 Crashed!")
        velocity_x = 0
        velocity_y = 0
    else:
        x, y = next_x, next_y

    # --- Draw everything ---
    screen.blit(track, (0, 0))

    # Draw lidar before car (for clarity)
    lidar_readings = get_lidar_readings(x, y, angle, track)
    # Optional: print readings
    print([round(r, 1) for r in lidar_readings])

    # Draw car
    rotated_car = pygame.transform.rotate(car_image, angle)
    rect = rotated_car.get_rect(center=(x, y))
    screen.blit(rotated_car, rect.topleft)

    # Draw red hitbox
    corners = get_rotated_hitbox(x, y, car_w, car_h, angle)
    pygame.draw.polygon(screen, (255, 0, 0), corners, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
