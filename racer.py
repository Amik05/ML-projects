import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (200, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Car class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.angle = 0  # Degrees
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.2
        self.turn_speed = 5

    def update(self, keys):
        # Forward/backward
        if keys[pygame.K_UP]:
            self.speed += self.acceleration
        elif keys[pygame.K_DOWN]:
            self.speed -= self.acceleration
        else:
            # Friction
            self.speed *= 0.95

        # Clamp speed
        self.speed = max(-self.max_speed, min(self.speed, self.max_speed))

        # Turning
        if keys[pygame.K_LEFT]:
            self.angle += self.turn_speed * (self.speed / self.max_speed)
        if keys[pygame.K_RIGHT]:
            self.angle -= self.turn_speed * (self.speed / self.max_speed)

        # Move car
        rad = math.radians(self.angle)
        self.x += -self.speed * math.sin(rad)
        self.y += -self.speed * math.cos(rad)

    def draw(self, surface):
        # Draw rotated rectangle as car
        rad = math.radians(self.angle)
        car_rect = pygame.Rect(0, 0, self.width, self.height)
        car_rect.center = (self.x, self.y)
        rotated_car = pygame.transform.rotate(
            pygame.Surface((self.width, self.height), pygame.SRCALPHA), self.angle
        )
        rotated_car.fill(RED)
        rotated_rect = rotated_car.get_rect(center=(self.x, self.y))
        surface.blit(rotated_car, rotated_rect.topleft)

# Track (just a simple gray background for now)
def draw_track():
    screen.fill(GRAY)
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH-100, HEIGHT-100), 5)  # track border

# Main loop
def main():
    car = Car(WIDTH // 2, HEIGHT // 2)
    running = True

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        car.update(keys)

        # Draw
        draw_track()
        car.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
