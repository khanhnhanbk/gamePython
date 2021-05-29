from os import truncate
from typing import AbstractSet, get_origin
import pygame
from pygame import color
from pygame.constants import K_SPACE, K_a, K_c
from pygame.time import Clock
import random

pygame.init()

YELLOW = (255, 255, 0)
BLACK = 0, 0, 0


char = pygame.image.load("./images/standing.png")

windowsSize = 800, 480
bg = pygame.image.load("./images/bg.jpg")


class Bullets(object):
    def __init__(self, x, y, radius, color, facing) -> None:
        self.pos = [x, y]
        self.radius = radius
        self.color = color
        self.facing = -20 if facing else 20
        self.live = 0
        self.hitBox = pygame.Rect(self.pos[0], self.pos[1], self.radius * 2, self.radius * 2)

    def draw(self, windows):
        pygame.draw.circle(windows, self.color, self.pos, self.radius)

    def moving(self):
        self.pos[0] += self.facing
        self.pos[1] += self.live ** 2 * 0.1
        self.live += 1
        self.hitBox = pygame.Rect(self.pos[0], self.pos[1], self.radius * 2, self.radius * 2)



class character(object):
    def __init__(self, x, y, width, heigh, step, folder, health) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.heigh = heigh
        self.step = step
        self.color = YELLOW
        self.isJump = False
        self.jumpCount = 10
        self.left = True
        self.right = False
        self.walkCount = 0
        self.isStanding = True
        self.selected = False
        self.bullets = []
        self.maxHealth = health
        self.health = health
        self.walkRight = [
            pygame.image.load("./images/" + folder + "/R1.png"),
            pygame.image.load("./images/" + folder + "/R2.png"),
            pygame.image.load("./images/" + folder + "/R3.png"),
            pygame.image.load("./images/" + folder + "/R4.png"),
            pygame.image.load("./images/" + folder + "/R5.png"),
            pygame.image.load("./images/" + folder + "/R6.png"),
            pygame.image.load("./images/" + folder + "/R7.png"),
            pygame.image.load("./images/" + folder + "/R8.png"),
            pygame.image.load("./images/" + folder + "/R9.png"),
        ]

        self.walkLeft = [
            pygame.image.load("./images/" + folder + "/L1.png"),
            pygame.image.load("./images/" + folder + "/L2.png"),
            pygame.image.load("./images/" + folder + "/L3.png"),
            pygame.image.load("./images/" + folder + "/L4.png"),
            pygame.image.load("./images/" + folder + "/L5.png"),
            pygame.image.load("./images/" + folder + "/L6.png"),
            pygame.image.load("./images/" + folder + "/L7.png"),
            pygame.image.load("./images/" + folder + "/L8.png"),
            pygame.image.load("./images/" + folder + "/L9.png"),
        ]

        self.hitBox = pygame.Rect(self.x + self.width // 4, self.y, self.width - self.width // 2, self.heigh)

    def draw(self, windows):
        if self.walkCount >= 26:
            self.walkCount = 0
        if not (self.isStanding):
            if self.left:
                windows.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                windows.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            self.walkCount = 0
            if self.left:
                windows.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            else:
                windows.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
        for b in self.bullets:
            b.draw(windows)
            b.moving()
            if (
                (b.pos[0] < 0)
                or (b.pos[0] > windowsSize[0])
                or b.pos[1] > windowsSize[1]
            ):
                self.bullets.remove(b)
        self.hitBox = pygame.Rect(self.x + self.width // 4, self.y, self.width - self.width // 2, self.heigh)
        # pygame.draw.rect(windows, (255, 0,0), self.hitBox, 6, 1)
        pygame.draw.rect(windows, (255, 0, 0), (self.hitBox[0], self.hitBox[1], self.hitBox[2], 5))
        pygame.draw.rect(windows, (2, 171, 92), (self.hitBox[0], self.hitBox[1], self.hitBox[2] * self.health / self.maxHealth, 5))

    def moving(self):
        keys = pygame.key.get_pressed()
        if self.selected:
            if keys[pygame.K_LEFT] and (self.x >= self.step):
                self.x -= self.step
                self.left = True
                self.right = False
                self.isStanding = False
            elif keys[pygame.K_RIGHT] and (
                self.x <= windowsSize[0] - self.width - self.step
            ):
                self.x += self.step
                self.left = False
                self.right = True
                self.isStanding = False
            else:
                # self.left = False
                # self.right = False
                self.walkCount = 0
                self.isStanding = True
            if not self.isJump:
                if keys[pygame.K_UP]:
                    self.isJump = True
            else:
                if self.jumpCount < -10:
                    self.jumpCount = 10
                    self.isJump = False
                else:
                    self.y -= self.jumpCount * abs(self.jumpCount) * 0.5
                    self.jumpCount -= 1
            if keys[K_SPACE]:
                if len(self.bullets) < 5:
                    self.bullets.append(
                        Bullets(
                            self.x + self.width // 2,
                            self.y + self.heigh // 2,
                            6,
                            BLACK,
                            self.left,
                        )
                    )
        else:
            if self.x >= self.step and self.left:
                self.x -= self.step
                self.isStanding = False
            else:
                self.x += self.step
                self.left = not (self.x < windowsSize[0] - self.width - self.step)
            if not self.isJump:
                if random.randrange(0, 100) % 40== 10:
                    self.isJump = True
            else:
                if self.jumpCount < -10:
                    self.jumpCount = 10
                    self.isJump = False
                else:
                    self.y -= self.jumpCount * abs(self.jumpCount) * 0.5
                    self.jumpCount -= 1
        if keys[K_c]:
            self.selected = not self.selected
    def isDead(self) -> bool:
        return self.health <= 0