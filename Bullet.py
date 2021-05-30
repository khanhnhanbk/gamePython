import pygame


class Bullet:
    def __init__(self, x, y, radius, color, toLeft) -> None:
        self.pos = [x, y]
        self.radius = radius
        self.color = color
        self.facing = -20 if toLeft else 20
        self.live = 0
        self.hitBox = pygame.Rect(self.pos[0], self.pos[1], self.radius * 2, self.radius * 2)

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.pos, self.radius)
    
    def moving(self):
        self.pos[0] += self.facing
        self.pos[1] += self.live ** 2 // 20
        self.live += 1
        self.hitBox = pygame.Rect(self.pos[0], self.pos[1], self.radius * 2, self.radius * 2)
