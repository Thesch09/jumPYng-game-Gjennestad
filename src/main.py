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
gravity = 10
slippery = 0.9

pressedKeys = {"left":False, "right":False, "up":False, "space":False}


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

class playerClass:
    def __init__(self):
        self.maxHealth = 3
        self.health = self.maxHealth
        self.jumpHeight = 500
        self.horSpeed = 25
        self.height = 64
        self.x = screight/2
        self.y = screight/2
        self.bounds = pygame.Rect(self.x,self.y,48, self.height)
        self.feet = pygame.Rect(self.x,self.y+self.height-8, 48, 8)
        self.yVelocity = 0
        self.xVelocity = 0
        self.coyote = 0

    def updateHitboxes(self):
        self.bounds = pygame.Rect(self.x,self.y,48, self.height)
        self.feet = pygame.Rect(self.x,self.y+self.height-8, 48, 8)

player = playerClass()

while running:
    screen.fill((150,150,255))

    speed += 5*deltaTime

    for nimbus in clouds:
        collision = player.feet.colliderect(nimbus.hitbox)
        if collision:
            print("Touched a cloud")
            if player.yVelocity > 0:
                player.yVelocity = 0
                iterations = 0
                player.coyote = 3
                while False:
                    player.y -= 1
                    print(player.y)
                    collision = player.feet.colliderect(nimbus.hitbox)
                    print(collision)
                    if iterations > 12:
                        break
                    else:
                        iterations += 1
                break
    else:
        player.yVelocity += gravity*deltaTime
        player.y += player.yVelocity


    player.updateHitboxes()
    pygame.draw.rect(screen, (0,255,0), player.bounds)
    pygame.draw.rect(screen, (122,122,0), player.feet)
    if pressedKeys["left"]:
        player.xVelocity -= player.horSpeed * deltaTime
    if pressedKeys["right"]:
        player.xVelocity += player.horSpeed * deltaTime
    player.xVelocity = player.xVelocity * slippery
    player.x += player.xVelocity

    if player.coyote > 0:
        player.coyote -= 1*deltaTime
        print(player.coyote)

    if pressedKeys["space"] or pressedKeys["up"]:
        if player.coyote > 0:
            player.yVelocity = player.jumpHeight * deltaTime * -1
            player.coyote = 0
            print("jumpies!")

    if player.y > screight+50:
        player.x = screight/2
        player.y = screight/2
        player.yVelocity = 0
        print("Ow! My leg!")
    
    TICK_CLOUD()
    TICK_SCORE()

    pygame.draw.rect(screen, (255,0,0), scoreBG)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pressedKeys.update({"left":True})
            if event.key == pygame.K_RIGHT:
                pressedKeys.update({"right":True})
            if event.key == pygame.K_UP:
                pressedKeys.update({"up":True})
            if event.key == pygame.K_SPACE:
                pressedKeys.update({"space":True})
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                pressedKeys.update({"right":False})
            if event.key == pygame.K_LEFT:
                pressedKeys.update({"left":False})
            if event.key == pygame.K_UP:
                pressedKeys.update({"up":False})
            if event.key == pygame.K_SPACE:
                pressedKeys.update({"space":False})
            
    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min((0.1, deltaTime)))