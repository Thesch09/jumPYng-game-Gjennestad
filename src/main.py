import pygame
import random

scridth = 640
screight = 480

screen = pygame.display.set_mode((scridth, screight))

running = True
clock = pygame.time.Clock()
deltaTime = 0.1

clouds = []
class cloud:
    def __init__(self):
        self.width = 32*random.randint(2,4)
        print(f"Cloud size: {self.width}")
        self.x = random.randint(int(0-self.width/2),int(screight-self.width/2))
        self.y = -30
        self.speedMult = random.randint(90,130)/100
        self.hitbox = pygame.Rect(self.x,self.y,self.width,8)
clouds.append(cloud())

choppingCloud = []

scoreBG = pygame.Rect(screight,0,scridth-screight,screight)

while running:
    screen.fill((150,150,255))
    
    if len(clouds) < 10:
        if random.randint(1,200+len(clouds)):
            print("Cloud made")
            clouds.append(cloud())
    for nimbus in clouds:
        nimbus.y += 10*deltaTime*nimbus.speedMult
        nimbus.hitbox = pygame.Rect(nimbus.x,nimbus.y,nimbus.width,8)
        pygame.draw.rect(screen, (255,255,255), nimbus.hitbox)
        if nimbus.y > 510:
            choppingCloud.append(nimbus)
    if len(choppingCloud) > 0:
        for nimbus in choppingCloud:
            clouds.remove(nimbus)
        choppingCloud = []

    pygame.draw.rect(screen, (255,0,0), scoreBG)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min((0.1, deltaTime)))