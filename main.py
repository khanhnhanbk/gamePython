from os import putenv, truncate
import sys
from typing import AbstractSet, get_origin
import pygame
from pygame import color
from pygame import draw
from pygame.constants import K_KP_ENTER, K_LEFT, K_RIGHT, K_SPACE, K_a, K_c, K_s
from pygame.mixer import fadeout
from pygame.time import Clock
import math
import random
import board
import player

pygame.init()


class Game:
    def __init__(self) -> None:
        self.board = board.Board(self)
        self.man = player.Player(self, 200, 400, 64, 64, 10, 10, "man")
        self.enemys = []

        for i in range(1):
            self.enemys.append(
                player.Player(
                    self, random.randrange(100, 800), 400, 64, 64, 5, 10, "enemy"
                )
            )
        # self.enemys = []
        self.score = 0
        self.level = 0
        self.numberOfEnemy = 1
        self.maxNumberOfEnemy = 5
        self.isGameOver = False
        self.hitSound = pygame.mixer.Sound("./music/hit.mp3")

        self.bulletSound = pygame.mixer.Sound("./music/bullet.mp3")

        self.music = pygame.mixer.music.load("./music/music.mp3")

        pygame.mixer.music.play(-1)

        self.prepareGame()
    def initGame(self):
        self.score = 0
        self.level = 0
        self.numberOfEnemy = 1
        self.maxNumberOfEnemy = 5
        self.isGameOver = False
    def prepareGame(self):
        while not self.isGameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isGameOver = True

            self.board.drawPrepare()
            if pygame.key.get_pressed()[K_s]:
                self.initGame()
                break        
            pygame.display.update()
            pygame.time.delay(50)
        self.loop()

    def loop(self):
        while not self.isGameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isGameOver = True
            # check key press

            self.pressKey(self.man)
            for enemy in self.enemys:
                self.randomControl(enemy, random.randrange(100, 10000))

                if self.man.hitAnother(enemy):
                    self.man.health -= 1

                for b in self.man.bullets:
                    if enemy.hitAnother(b):
                        self.hitSound.play()
                        enemy.health -= self.man.dam
                        self.man.bullets.remove(b)
                        if enemy.isDead() and (enemy in self.enemys):
                            self.score += enemy.maxHealth
                            self.man.health += enemy.maxHealth // 10
                            self.man.maxHealth += enemy.maxHealth // 10
                            self.enemys.remove(enemy)
            # level up
            if not self.enemys:
                self.level += 1
                self.numberOfEnemy += 1
                self.man.dam *= 1.3
                if self.man.dam > 100:
                    self.man.dam / 1.2
                self.man.health = self.man.maxHealth
                for i in range(self.numberOfEnemy):
                    self.enemys.append(
                        player.Player(
                            self,
                            random.randrange(100, 800),
                            400,
                            64,
                            64,
                            5 + random.randrange(10, 100) % 5,
                            round(10 * 1.1 ** self.level),
                            "enemy",
                        )
                    )

                self.board.drawLevelUp()
                self.man.draw()
                pygame.display.update()
                pygame.time.delay(1000)

            if self.man.isDead():
                self.isGameOver = True
                self.gameOver()

            self.draw()
            pygame.time.delay(50)

    def draw(self):
        self.board.draw()
        self.man.draw()
        self.man.moving()
        for enemy in self.enemys:
            enemy.draw()
            enemy.moving()
        pygame.display.update()
        # draw boar
        # draw charater

    def pressKey(self, man: player.Player):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            man.isStanding = False
            man.move[0] = -man.step
            man.move[1] = 0
            man.left = True
        elif keys[K_RIGHT]:
            man.isStanding = False
            man.move[0] = man.step
            man.move[1] = 0
            man.left = False
        else:
            man.move[0] = 0
            man.isStanding = True

        if not man.isJump:
            man.move[1] = 0
            if keys[pygame.K_UP]:
                man.isJump = True
        else:
            if man.jumpCount < -10:
                man.jumpCount = 10
                man.isJump = False
            else:
                man.move[1] = -man.jumpCount * abs(man.jumpCount) * 0.5
                man.jumpCount -= 1
        if keys[K_SPACE]:
            self.bulletSound.play()
            man.fire()

    def randomControl(self, man: player.Player, randomKey):
        # randomKey = random.randrange(1, 10000)
        if man.pos[0] > 0 and man.left:
            man.isStanding = False
            man.move[0] = -man.step
            man.move[1] = 0
            man.left = True
        elif randomKey % 10 > 5:
            man.isStanding = False
            man.move[0] = man.step
            man.move[1] = 0
            man.left = False
            if man.pos[0] > 500 + randomKey % 300:
                man.left = True

        if not man.isJump:
            man.move[1] = 0
            if randomKey % 100 == 5:
                man.isJump = True
        else:
            if man.jumpCount < -10:
                man.jumpCount = 10
                man.isJump = False
            else:
                man.move[1] = -man.jumpCount * abs(man.jumpCount) * 0.5
                man.jumpCount -= 1

    def gameOver(self):
        self.board.drawGameOver()
        pygame.display.update()
        self.prepareGame()
        pygame.time.delay(3000)


g = Game()
