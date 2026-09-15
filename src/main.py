import pygame
import random
import math

scridth = 640
screight = 480

screen = pygame.display.set_mode((scridth, screight))

running = True
clock = pygame.time.Clock()
deltaTime = 0.1

clouds = []
class cloud:
    def __init__(self):
        self.width = 48*random.randint(2,4)
        print(f"Cloud size: {self.width}")
        self.x = random.randint(int(0-self.width/2),int(screight-self.width/2))
        self.y = -30
        self.speedMult = random.randint(90,110)/100
        self.hitbox = pygame.Rect(self.x,self.y,self.width,12)
clouds.append(cloud())
cloudCooldown = 0

scoreBG = pygame.Rect(screight,0,scridth-screight,screight)

speed = 100
score = 0
scoreTick = 0

def TICK_CLOUD():
    global clouds
    global cloudCooldown
    global speed
    choppingCloud = []

    if len(clouds) < 10:
        if cloudCooldown > 5:
            print("Cloud made")
            clouds.append(cloud())
            cloudCooldown = 0
        else:
            cloudCooldown += random.randint(1,3)*deltaTime
    for nimbus in clouds:
        nimbus.y += speed/10*deltaTime*nimbus.speedMult
        nimbus.hitbox = pygame.Rect(nimbus.x,nimbus.y,nimbus.width,12)
        pygame.draw.rect(screen, (255,255,255), nimbus.hitbox)
        if nimbus.y > 510:
            choppingCloud.append(nimbus)
    if len(choppingCloud) > 0:
        for nimbus in choppingCloud:
            clouds.remove(nimbus)
            cloudCooldown += 5
        choppingCloud = []

def TICK_SCORE():
    global scoreTick
    global score
    global speed

    if scoreTick > 3:
        score += speed/(350-math.floor(speed/500))
        scoreTick = 0
        print(f"Speed: {speed}")
        print(f"Score formula: {speed}/{350-math.floor(speed/500)})")
        print(f"Score: {math.floor(score)}")
        print(f"Not Floored: {score}")
    else:
        scoreTick += 1*deltaTime

while running:
    screen.fill((150,150,255))

    speed += 5*deltaTime
    
    TICK_CLOUD()
    TICK_SCORE()

    pygame.draw.rect(screen, (255,0,0), scoreBG)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min((0.1, deltaTime)))