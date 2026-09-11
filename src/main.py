import pygame

scridth = 640
screight = 480
screen = pygame.display.set_mode((scridth, screight))

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((122,122,122))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min((0.1, deltaTime)))