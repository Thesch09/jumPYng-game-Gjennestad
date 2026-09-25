# Theodor Schaathun bruker ikke AI/KI, hvis den nyeste version av en del av koden er skrevet av han er det fri for AI/KI

import os
import math
import pygame

scridth = 640
screight = 480

screen = pygame.display.set_mode((scridth, screight))

sprites = {}
assets = os.listdir(r"assets/sprites")
class spriteMaker:
    def __init__(self, sprite, sizeMult):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,
                                (self.sprite.get_width() * sizeMult,
                                self.sprite.get_height() * sizeMult))
        sprites.update({sprite.split("/")[-1].split(".png")[0]:self.sprite})

def addSprite(assets):
    for img in assets:
        sprite = spriteMaker(f"assets/sprites/{img}",2)
        print(sprites)
    for img in sprites:
        print(img)
    return sprites

showSpritesDEBUG = False # show a "sheet" of all the sprites

if showSpritesDEBUG:
    addSprite(assets)
    while True:
        x = 0
        y = 0
        for sprite in sprites:
            screen.blit(sprites[sprite], (x,y))
            x += sprites[sprite].get_width()
            if x > screight:
                y += 64
                x = 0
        pygame.display.flip()