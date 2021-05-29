from random import randrange
from typing import AbstractSet, get_origin
import pygame
from pygame import color, init
from pygame import font
from pygame.constants import K_a, K_c
from pygame.mixer import fadeout
from pygame.time import Clock

import character


windows = pygame.display.set_mode(character.windowsSize)

pygame.display.set_caption("First game")


def rawWindow():
    windows.blit(character.bg, (0, 0))
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    windows.blit(text, (character.windowsSize[0] - 140, 10))
    
    text = font.render("Level: " + str(level), 1, (0, 0, 0))
    windows.blit(text, (character.windowsSize[0] - 140, 40))
    
    man.draw(windows)
    for enemy in enemys:
        enemy.draw(windows)
    pygame.display.update()


score = 0

font = pygame.font.SysFont("comicsans", 30, True)

man = character.character(200, 400, 64, 64, 10, "man", 10)
enemys = []
enemys.append(character.character(00, 400, 64, 64, 5, "enemy", 10))

man.selected = True
hit = True
run = True

level = 0
numberOfEnemy = 2

while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for enemy in enemys:
        if man.hitBox.colliderect(enemy.hitBox):
            if not hit:
                man.health -= 1
                print(hit)
        else:
            hit = False
        for bullet in man.bullets:
            if enemy.hitBox.colliderect(bullet.hitBox):
                man.bullets.remove(bullet)
                enemy.health -= 1
                print("hit af")
        enemy.moving()
        # draw screen
        if enemy.isDead():
            score += enemy.maxHealth
            enemys.remove(enemy)
            man.health += (enemy.maxHealth // 10)
            if man.health > man.maxHealth:
                man.maxHealth = man.health

    if not enemys:
        windows.blit(character.bg, (0, 0))
        text = font.render("Score: " + str(score), 1, (0, 0, 0))
        windows.blit(text, (character.windowsSize[0] - 140, 10))

        text = font.render("LEVEL UP", 1, (255, 255, 255))
        windows.blit(
            text,
            (character.windowsSize[0] // 2 - 50, character.windowsSize[1] // 2),
        )

        man.draw(windows)

        pygame.display.update()
        
        numberOfEnemy = (level % 3)
        level += 1
        
        for i in range(numberOfEnemy + 1):
            posX =  character.random.randrange(0, character.windowsSize[0])
            while  man.x - posX < 50 or man.x - posX > 100:
                posX =  character.random.randrange(0, character.windowsSize[0])
            enemys.append(
                character.character(
                    posX, 400, 64, 64, 5, "enemy", 10 + 5 * (level // 3)
                )
            )
        
        for enemy in enemys:
            enemy.draw(windows)

        pygame.time.delay(1000)

    if man.isDead():
        windows.blit(character.bg, (0, 0))
        text = font.render("Score: " + str(score), 1, (0, 0, 0))
        windows.blit(
            text,
            (character.windowsSize[0] // 2 - 50, character.windowsSize[1] // 2 + 30),
        )

        text = font.render("Gameover", 1, (255, 255, 255))
        windows.blit(
            text, (character.windowsSize[0] // 2 - 50, character.windowsSize[1] // 2)
        )
        for enemy in enemys:
            enemy.draw(windows)

        pygame.display.update()
        run = False
        pygame.time.delay(1000)
    else:
        man.moving()
    rawWindow()
pygame.quit()
