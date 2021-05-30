import pygame
from pygame.math import enable_swizzling
from pygame.mixer import fadeout
import Bullet


class Player:
    def __init__(self, game, x, y, width, heigh, step, health, folder) -> None:
        self.game = game
        self.pos = [x, y]
        self.size = [width, heigh]
        self.step = step
        self.maxHealth = health
        self.health = health
        self.dam = 1

        self.move = [-step, 0]
        self.isJump = False
        self.jumpCount = 10
        self.left = True
        self.walkCount = 0
        self.isStanding = False
        self.selected = False
        self.bullets = []
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

        self.hitBox = pygame.Rect(
            self.pos[0] + self.size[0] // 4,
            self.pos[1],
            self.size[0] - self.size[0] // 2,
            self.size[1],
        )

    def draw(self):

        # draw self

        if self.walkCount >= 26:
            self.walkCount = 0
        if not (self.isStanding):
            if self.left:
                self.game.board.win.blit(
                    self.walkLeft[self.walkCount // 3], (self.pos[0], self.pos[1])
                )
                self.walkCount += 1
            else:
                self.game.board.win.blit(
                    self.walkRight[self.walkCount // 3], (self.pos[0], self.pos[1])
                )
                self.walkCount += 1
        else:
            self.walkCount = 0
            if self.left:
                self.game.board.win.blit(
                    self.walkLeft[self.walkCount // 3], (self.pos[0], self.pos[1])
                )
            else:
                self.game.board.win.blit(
                    self.walkRight[self.walkCount // 3], (self.pos[0], self.pos[1])
                )
        # draw bullets
        for b in self.bullets:
            b.draw(self.game.board.win)
            b.moving()
            if (
                (b.pos[0] < 0)
                or (b.pos[0] > self.game.board.size[0])
                or b.pos[1] > self.game.board.size[1]
            ):
                self.bullets.remove(b)

        # pygame.draw.rect(self.game.board.win, (255, 0,0), self.hitBox, 6, 1)

        pygame.draw.rect(
            self.game.board.win,
            (255, 0, 0),
            (self.hitBox[0], self.hitBox[1], self.hitBox[2], 5),
        )
        pygame.draw.rect(
            self.game.board.win,
            (2, 171, 92),
            (
                self.hitBox[0],
                self.hitBox[1],
                self.hitBox[2] * self.health / self.maxHealth,
                5,
            ),
        )

    def moving(self):
        self.pos[0] += self.move[0]
        if self.pos[0] < 0:
            self.pos[0] = 0
        elif self.pos[0] > self.game.board.size[0] - self.step - self.size[0]:
            self.pos[0] = self.game.board.size[0] - self.step - self.size[0]

        self.pos[1] += self.move[1]
        if self.pos[1] < 0:
            self.pos[1] = 0
        elif self.pos[1] > self.game.board.size[1] - self.step - self.size[1]:
            self.pos[1] = self.game.board.size[1] - self.step - self.size[1]
        
        # update hitBox
        self.hitBox = pygame.Rect(
            self.pos[0] + self.size[0] // 4,
            self.pos[1],
            self.size[0] - self.size[0] // 2,
            self.size[1],
        )

    def fire(self):
        if len(self.bullets) < 3:
            self.bullets.append(
                Bullet.Bullet(
                    self.pos[0] + self.size[0] // 2,
                    self.pos[1] + self.size[1] // 2,
                    6,
                    (0, 0, 0),
                    self.left,
                )
            )
    def hitAnother(self, enemy):
        return self.hitBox.colliderect(enemy.hitBox)
    
    def isDead(self):
        return self.health <= 0