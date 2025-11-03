import pygame

pygame.init()
clock = pygame.time.Clock()
fps = 60

# screen
screen_width = 864
screen_length = 936
screen = pygame.display.set_mode((screen_width, screen_length))
pygame.display.set_caption('Flappy Bird')

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False

# load images
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1, 4):
            img = pygame.image.load(f'img/bird{i}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        # gravity
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not game_over:
            # jumping
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
        
            # animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1            
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)



bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_length/2))

bird_group.add(flappy)



# game loop
run = True

while run:
    # lock in fps
    clock.tick(fps)

    # draw background
    screen.blit(bg, (0, 0))

    # draw bird
    bird_group.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), flappy.rect, 1)
    bird_group.update()

    # draw moving ground
    screen.blit(ground, (ground_scroll, 768))

    # check if bird hit ground
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if not game_over:
        # ground animation    
        ground_scroll -= scroll_speed
        if ground_scroll <= -35:
            ground_scroll = 0

    # event listener
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True
    
    # updating display
    pygame.display.update()

pygame.quit()