# Theodor Schaathun bruker ikke AI/KI, hvis den nyeste version av en del av koden er skrevet av han er det fri for AI/KI

import pygame
import random
import math
import os
import json
import time
from spriteAdd import addSprite

scridth = 640
screight = 480

flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((scridth, screight), flags)

print(pygame.font.get_init())
pygame.font.init()
font = pygame.font.Font(None,40)
writtenText = ""

running = True
clock = pygame.time.Clock()
deltaTime = 0.1
gameState = "menu" # or "game" or "write"

# sprites
assets = os.listdir(r"assets/sprites")
sprites = addSprite(assets, 3)

clouds = []
class cloud:
    def __init__(self, guaranteedPink, pinkGoal):
        self.width = random.randint(2,4)
        print(f"Cloud size: {self.width}")
        self.pink = False
        self.guaranteedPink = guaranteedPink
        if guaranteedPink or random.randint(1,7) == 1:
            self.pink = True

        # sprite
        if self.width == 1:
            spritey = "small"
        elif self.width == 2:
            spritey = "med"
        else:
            spritey = "big"
        spritey += "Cloud"
        if self.pink:
            spritey += "Pink"
        self.sprite = sprites[spritey]
        self.width = self.sprite.get_width()

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

obstaclesList = []
class obstacles: # Pronounced like Heracles
    def __init__(self, objID, sprite, passThrough, projectiles, speedMult, life = 0, score = 0, speedAdd = 0):
        self.objID = objID
        self.sprite = sprite
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        #self.width = width
        #self.height = height
        if type(projectiles) == list:
            self.hasProjectiles = True
            self.prType = projectiles[0]
            self.prAmount = projectiles[1]
            self.prSpread = projectiles[2]
            self.prSpreadStart = projectiles[3]
        else:
            self.hasProjectiles = False
        self.x = random.randint(int(0-self.width/2),int(screight-self.width/2))
        self.y = 0-self.height*2
        self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.passThrough = passThrough
        self.speedMult = speedMult
        self.score = score
        self.life = life
        self.speedAdd = speedAdd
        self.touchedPlayer = False
        self.touchedClouds = []
        self.startTime = 2

        obstaclesList.append(self)
obstaclesCooldown = -20

obstacleTypes = {
    "coin":{"ID":0, "sprite":sprites["coin"], "passThrough":True,"projectiles":"None", "speedMult":(70,90), "healthAdd":0, "score":100, "speedAdd":150, "replace chance":40},
    "heart":{"ID":1, "sprite":sprites["heartObs"], "passThrough":True,"projectiles":"None", "speedMult":(290,310), "healthAdd":1, "score":0, "speedAdd":0, "replace chance":65},
    "rock":{"ID":10, "sprite":sprites["boulder"], "passThrough":False,"projectiles":"None", "speedMult":(90,110), "healthAdd":0, "score":0, "speedAdd":0, "replace chance":0} # boulder I hardly know her
    }
# New obstacle format:
# "coin":{"ID":0, "sprite":"sprite", "passThrough":True,"projectiles":["type, uses a different obstacle", amount, gap between bullets, gap between direction of source and first projectile], "speedMult":(min,max), "healthAdd":how much new health, "score": how much score gets added, "speedAdd": how much speed gets added, "replace chance": the chance of an obstacle being rerolled}
# This is to make easier to port it to JSON and add new
# Width and Height gets mathed using the size of the sprite
obsTypeList = []
for teyepe in obstacleTypes:
    obsTypeList.append(teyepe)

scoreBG = pygame.Rect(screight,0,scridth-screight,screight)

speed = 100
score = 0
lastScore = 0
highScore = 0
scoreTick = 0
gravity = 10
slippery = 0.9

# J(a)SON
def loadJSON():
    global score
    global highScore
    global jsonScored
    with open(r"leaderboard/leaderboard.json", "r") as jsonScores:
        jsonScored = json.loads(jsonScores.read())
        print(jsonScored)
        print(type(jsonScored))
    for scoringPlayer in jsonScored:
        if scoringPlayer["score"] > highScore:
            highScore = scoringPlayer["score"]
def writeJSON():
    global jsonScored
    with open(r"leaderboard/leaderboard.json", "w") as jsonScores:
        jsonScores.write(json.dumps(jsonScored, indent=4))
        print("blub")
    with open(r"leaderboard/leaderboard.json", "r") as jsonScore:
        for line in jsonScore:
            print(f"asd {line}")
loadJSON()
writeJSON()
pressedKeys = {"left":False, "right":False, "up":False, "space":False}

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
        global speed
        # This function gets called whenever you fall. Little does the player know, the guy goes to the hospital for 4 months
        speed = speed/2
        clouds.append(cloud(True, 380))
        self.x = screight/2-self.width/2
        self.y = screight/2
        self.updateHitboxes()
        self.yVelocity = 0
        self.xVelocity = 0
        self.coyote = 0
        self.health -= 1
        print("Ow! My leg!")

    def checkCollisionWithClouds(self, cloud): # pretty self-explanetory
        self.y += 1
        self.updateHitboxes()
        collision = self.feet.colliderect(cloud.hitbox)
        if collision:
            self.y -= 1
            self.updateHitboxes()
            if self.yVelocity > 0:
                if cloud.pink and cloud.cloudLife > 0:
                    self.y -= 1
                self.yVelocity = 0
                self.coyote = 0.5
                return True
        self.y -= 1

    def movement(self, clouds):
        global gravity
        for nimbus in clouds:
            if self.checkCollisionWithClouds(nimbus):
                break
        else:
            # Fall
            self.yVelocity += gravity*deltaTime
            self.y += self.yVelocity

        # Horizontal
        if pressedKeys["left"]:
            self.xVelocity -= self.horSpeed * deltaTime
        if pressedKeys["right"]:
            self.xVelocity += self.horSpeed * deltaTime
        self.xVelocity = self.xVelocity * slippery
        self.x += self.xVelocity

    def jumpies(self):
        if self.coyote > 0:
            self.coyote -= 1*deltaTime
    
        if pressedKeys["space"] or pressedKeys["up"]:
            if self.coyote > 0:
                self.yVelocity = self.jumpHeight * deltaTime * -1
                self.coyote = 0
                print("jumpies!")

    def theBoundsThatBindUs(self):
        # Falling off-screen and collision with the edges.
        if self.y > screight+50:
            self.goToStart()
        if self.x < 0-self.width/2:
            self.x = 0-self.width/2
        if self.x > screight-self.width/2:
            self.x = screight-self.width/2

player = playerClass()

def spawnObstacle(OT,OTL, retries):
    obs = OTL[random.randint(0,len(OTL)-1)]
    if random.randint(1,100) <= OT[obs]["replace chance"] and retries < 7:
        print(retries)
        spawnObstacle(OT,OTL, retries+1)
        return
    print(f"Spawned obstacle {obs}")
    obstaclesList.append(obstacles(obstacleTypes[obs]["ID"],
        obstacleTypes[obs]["sprite"],
        obstacleTypes[obs]["passThrough"],
        obstacleTypes[obs]["projectiles"],
        obstacleTypes[obs]["speedMult"],
        obstacleTypes[obs]["healthAdd"],
        obstacleTypes[obs]["score"],
        obstacleTypes[obs]["speedAdd"]))

def TICK_CLOUD():
    global clouds
    global cloudCooldown
    global speed
    global player
    choppingCloud = []

    # Add clouds
    if len(clouds) < 10:
        if cloudCooldown > 5:
            print("Cloud made")
            clouds.append(cloud(False,random.randint(int(screight/2),screight-48)))
            cloudCooldown = 0
        else:
            cloudCooldown += random.randint(1,3)*deltaTime

    # Move clouds
    for nimbus in clouds:
        if nimbus.pink and nimbus.y >= nimbus.goalPos and nimbus.cloudLife > 0:
            nimbus.y = nimbus.goalPos
            nimbus.cloudLife -= 1 * deltaTime
            if nimbus.cloudLife <= 0:
                nimbus.speedMult += 2
        else:
            nimbus.y += speed/10*deltaTime*nimbus.speedMult
        nimbus.hitbox = pygame.Rect(nimbus.x,nimbus.y+10,nimbus.width,6)

        
        if nimbus.hitbox.colliderect(player.feet) and nimbus.pink and nimbus.y >= nimbus.goalPos:
            if nimbus.guaranteedPink:
                if nimbus.cloudLife > 20:
                    nimbus.cloudLife = 20
            else:
                if nimbus.cloudLife > 3:
                    nimbus.cloudLife = 3

        # Visual
        screen.blit(nimbus.sprite, (nimbus.x,nimbus.y))
        colour = (255,255,255)
        if nimbus.pink:
            colour = (255,200,200)
        #pygame.draw.rect(screen, colour, nimbus.hitbox)

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

    # Increase score, but only once every 3 seconds
    if scoreTick > 1:
        score += max(1,max(1,speed/(350-math.floor(speed/500))))*10
        scoreTick = 0
        print(f"Speed: {speed}")
        print(f"Score formula: {speed}/{350-math.floor(speed/500)})")
        print(f"Score: {math.floor(score)}")
        print(f"Not Floored: {score}")
    else:
        scoreTick += 1*deltaTime

    scoreText = f"{math.floor(score)}"
    scoreText = font.render(scoreText, True, (0,0,0))
    screen.blit(scoreText, (scridth-scoreText.get_width(),0))

def TICK_PLAYER():
    global clouds
    global running
    global gameState
    global score
    global highScore
    global lastScore
    player.movement(clouds)
    player.jumpies()
    player.theBoundsThatBindUs()

    # Death
    if player.health == 0:
        gameState = "write"

    player.updateHitboxes()
    pygame.draw.rect(screen, (0,255,0), player.bounds)
    pygame.draw.rect(screen, (122,122,0), player.feet)

def TICK_OBSTACLES():
    global obstaclesCooldown
    global obstacleTypes
    global obstaclesList
    global obstacles
    global clouds
    global player
    global score
    global speed
    # Spawn an obstacle
    if obstaclesCooldown > max(1,10-highSpeed/1000):
        if len(obstaclesList) < 64:
            spawnObstacle(obstacleTypes, obsTypeList, 0)
            obstaclesCooldown = 0
    else:
        obstaclesCooldown += 1*deltaTime

    # Moving + cloud collision
    choppingCles = []
    for obstacle in obstaclesList:
        if obstacle.startTime > 0:
            target = pygame.Rect(obstacle.x+obstacle.width/2-20,0,40,40)
            pygame.draw.rect(screen, (255,0,0), target)
            obstacle.startTime -= 1*deltaTime
            continue
        obstacle.y += speed/7*deltaTime*random.randint(obstacle.speedMult[0],obstacle.speedMult[1])/100
        obstacle.hitbox = pygame.Rect(obstacle.x,obstacle.y,obstacle.width,obstacle.height)
        choppingCloud = []
        for nimbus in clouds:
            if obstacle.hitbox.colliderect(nimbus.hitbox) and not obstacle.passThrough and obstacle not in choppingCles:
                if obstacle.objID == 10 and random.randint(1,2) == 2:
                    choppingCloud.append(nimbus)
                    continue
                choppingCles.append(obstacle)
        if len(choppingCloud) > 0:
            for nimbus in choppingCloud:
                clouds.remove(nimbus)
        if obstacle.y > 510 and not obstacle in choppingCles:
            choppingCles.append(obstacle)

        # visual
        pygame.draw.rect(screen, (255,0,255), obstacle.hitbox)
        screen.blit(obstacle.sprite,(obstacle.x,obstacle.y))

    # Player collision
    for obstacle in obstaclesList:
        if not obstacle.startTime >0:
            if player.bounds.colliderect(obstacle.hitbox) and not obstacle.touchedPlayer:
                print(f"owchies, {obstacle.objID}")
                if obstacle.objID < 10:
                    player.health += obstacle.life
                    if player.health > player.maxHealth:
                        player.health = player.maxHealth
                    score += obstacle.score
                    speed += obstacle.speedAdd
                else:
                    player.goToStart()
                obstacle.touchedPlayer = True
            if not obstacle in choppingCles and obstacle.touchedPlayer:
                choppingCles.append(obstacle)

    # Removing the obstacles
    if len(choppingCles) > 0:
        for obstacle in choppingCles:
            obstaclesList.remove(obstacle)
        choppingCles = []

def TICK_SIDEPANEL():
    pygame.draw.rect(screen, (255,0,0), scoreBG)
    # health of player
    startPos = screight-sprites["heartHudEmpty"].get_height()
    for life in range(player.maxHealth):
        screen.blit(sprites["heartHudEmpty"],(screight+6,startPos-sprites["heartHudEmpty"].get_height()*life))
    for life in range(player.health):
        screen.blit(sprites["heartHud"],(screight+6,startPos-sprites["heartHud"].get_height()*life))

def startUp():
    global player
    global clouds
    global cloudCooldown
    global obstaclesList
    global obstaclesCooldown
    global speed
    global score
    global scoreTick
    global highSpeed
    player = playerClass()
    clouds = []
    obstaclesList = []
    clouds.append(cloud(True, 380))
    cloudCooldown = 0
    obstaclesCooldown = -20
    speed = 100
    highSpeed = speed
    score = 0
    scoreTick = 0
    

while running:
    if gameState == "game":
        screen.fill((150,150,255))
        
        # Increase speed
        speed += 5*deltaTime
        if speed > highSpeed:
            highSpeed = speed
    
        # Do the things
        TICK_PLAYER()
        TICK_CLOUD()
        TICK_OBSTACLES()
        TICK_SIDEPANEL()
        TICK_SCORE()
    elif gameState == "menu":
        screen.fill((0,0,0))
        scoreText = f"Last Score: {lastScore}"
        scoreText = font.render(scoreText, True, (255,255,255))
        screen.blit(scoreText, (scridth/2-scoreText.get_width()/2,screight/3))
        scoreText = f"High Score: {highScore}"
        scoreText = font.render(scoreText, True, (255,255,255))
        screen.blit(scoreText, (scridth/2-scoreText.get_width()/2,screight/4))
        scoreText = f"Trykk på [MELLOMBAR] for å starte!"
        scoreText = font.render(scoreText, True, (255,255,255))
        screen.blit(scoreText, (scridth/2-scoreText.get_width()/2,screight/3*2))
        if pressedKeys["space"]:
            gameState = "game"
            startUp()
    elif gameState == "write":
        screen.fill((0,0,0))
        scoreText = f"Hva heter du?"
        scoreText = font.render(scoreText, True, (255,255,255))
        screen.blit(scoreText, (scridth/2-scoreText.get_width()/2,screight/4))
        scoreText = f"{writtenText}"
        scoreText = font.render(scoreText, True, (255,255,255))
        screen.blit(scoreText, (scridth/2-scoreText.get_width()/2,screight/3*2))

    pygame.display.flip()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if gameState == "write":
                if event.key == pygame.K_RETURN and len(writtenText)>0:
                    gameState = "menu"
                    jsonScored.append({"name":writtenText,"score":math.floor(score)})
                    print(jsonScored)
                    lastScore = math.floor(score)
                    writeJSON()
                    loadJSON()
                    writtenText = ""
                elif event.key == pygame.K_BACKSPACE:
                    if len(writtenText) > 0:
                        writtenText = writtenText[:-1]
                else:
                    writtenText += event.unicode
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