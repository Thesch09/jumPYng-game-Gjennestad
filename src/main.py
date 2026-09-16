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
    def __init__(self, guaranteedPink, pinkGoal):
        self.width = 48*random.randint(2,4)
        print(f"Cloud size: {self.width}")
        self.pink = False
        self.guaranteedPink = guaranteedPink
        if guaranteedPink or random.randint(1,7) == 1:
            self.pink = True

        self.goalPos = 0
        if self.pink:
            self.goalPos = pinkGoal

        self.x = random.randint(int(0-self.width/2),int(screight-self.width/2))
        self.y = -30
        if guaranteedPink:
            self.x = screight/2-self.width/2
            self.y = pinkGoal

        self.speedMult = random.randint(90,110)/100
        if self.pink:
            self.speedMult = random.randint(290,310)/100
        
        self.hitbox = pygame.Rect(self.x,self.y,self.width,12)
        self.playerLanded = False
        if guaranteedPink:
            self.cloudLife = 222
        else:
            self.cloudLife = 10
clouds.append(cloud(True, 380))
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
    global player
    choppingCloud = []

    if len(clouds) < 10:
        if cloudCooldown > 5:
            print("Cloud made")
            clouds.append(cloud(False,random.randint(int(screight/2),screight-48)))
            cloudCooldown = 0
        else:
            cloudCooldown += random.randint(1,3)*deltaTime
    for nimbus in clouds:
        if nimbus.pink and nimbus.y >= nimbus.goalPos and nimbus.cloudLife > 0:
            nimbus.y = nimbus.goalPos
            nimbus.cloudLife -= 1 * deltaTime
            if nimbus.cloudLife <= 0:
                nimbus.speedMult += 2
        else:
            nimbus.y += speed/10*deltaTime*nimbus.speedMult
        

        nimbus.hitbox = pygame.Rect(nimbus.x,nimbus.y-2,nimbus.width,12)
        if nimbus.hitbox.colliderect(player.feet) and nimbus.pink and nimbus.y >= nimbus.goalPos:
            if nimbus.guaranteedPink:
                if nimbus.cloudLife > 20:
                    nimbus.cloudLife = 20
            else:
                if nimbus.cloudLife > 3:
                    nimbus.cloudLife = 3

        # Visual
        colour = (255,255,255)
        if nimbus.pink:
            colour = (255,200,200)
        nimbus.hitbox = pygame.Rect(nimbus.x,nimbus.y,nimbus.width,12)
        pygame.draw.rect(screen, colour, nimbus.hitbox)

        # Deletion
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
        self.width = 48
        self.x = screight/2-self.width/2
        self.y = screight/2
        self.bounds = pygame.Rect(self.x,self.y, self.width, self.height)
        self.feet = pygame.Rect(self.x,self.y+self.height-8, self.width, 8)
        self.yVelocity = 0
        self.xVelocity = 0
        self.coyote = 0

    def updateHitboxes(self):
        self.bounds = pygame.Rect(self.x,self.y,48, self.height)
        self.feet = pygame.Rect(self.x,self.y+self.height-8, 48, 8)

    def goToStart(self):
        global clouds
        global cloud
        clouds.append(cloud(True, 380))
        self.x = screight/2-self.width/2
        self.y = screight/2
        self.updateHitboxes()
        self.yVelocity = 0
        self.xVelocity = 0
        self.coyote = 0
        self.health -= 1
        print("Ow! My leg!")

player = playerClass()

while running:
    screen.fill((150,150,255))

    speed += 5*deltaTime

    for nimbus in clouds:
        player.y += 1
        player.updateHitboxes()
        collision = player.feet.colliderect(nimbus.hitbox)
        if collision:
            player.y -= 1
            player.updateHitboxes()
            if player.yVelocity > 0:
                if nimbus.pink and nimbus.cloudLife > 0:
                    player.y -= 1
                player.yVelocity = 0
                iterations = 0
                player.coyote = 3
                break
        player.y -= 1
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

    if pressedKeys["space"] or pressedKeys["up"]:
        if player.coyote > 0:
            player.yVelocity = player.jumpHeight * deltaTime * -1
            player.coyote = 0
            print("jumpies!")

    if player.y > screight+50:
        player.goToStart()
        if player.health == 0:
            running = False
    if player.x < 0-player.width/2:
        player.x = 0-player.width/2
    if player.x > screight-player.width/2:
        player.x = screight-player.width/2
    
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