import pygame
import math
import sys

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Movement Fix")
clock = pygame.time.Clock()

# --- Car setup ---
car_image = pygame.Surface((60, 30), pygame.SRCALPHA)
pygame.draw.polygon(car_image, (255, 50, 50), [(0, 0), (60, 15), (0, 30)])  # triangle-shaped car

car_x, car_y = WIDTH // 2, HEIGHT // 2
car_angle = 0
car_speed = 0.0
acceleration = 0.2
max_speed = 6
turn_speed = 3

# --- Game loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # --- Movement ---
    if keys[pygame.K_UP]:
        car_speed = min(car_speed + acceleration, max_speed)
    elif keys[pygame.K_DOWN]:
        car_speed = max(car_speed - acceleration, -max_speed / 2)
    else:
        car_speed *= 0.98  # friction

    # --- Turning ---
    if abs(car_speed) > 0.1:
        if keys[pygame.K_LEFT]:
            car_angle += turn_speed * (car_speed / max_speed)
        if keys[pygame.K_RIGHT]:
            car_angle -= turn_speed * (car_speed / max_speed)

    # --- Update position ---
    # Convert angle to radians
    rad = math.radians(car_angle)

    # The key fix: note the sin/cos swap
    car_x += math.cos(rad) * car_speed
    car_y -= math.sin(rad) * car_speed

    # --- Draw ---
    screen.fill((20, 20, 20))
    rotated_car = pygame.transform.rotate(car_image, car_angle)
    rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, rect.topleft)

    pygame.display.flip()
    clock.tick(60)
