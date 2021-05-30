import pygame
from pygame import key
from pygame.constants import K_KP_ENTER, K_SPACE


class Board:
    def __init__(self, game) -> None:
        self.game = game
        self.size = (800, 480)
        self.image = pygame.image.load("./images/bg.jpg")
        self.win = pygame.display.set_mode(self.size)
        pygame.display.set_caption("First game")

    def draw(self):
        self.win.blit(self.image, (0, 0))
        text = pygame.font.SysFont("comicsans", 30, True).render(
            "Score: " + str(self.game.score), 1, (0, 0, 0)
        )
        self.win.blit(text, (self.size[0] - 150, 20))
        text = pygame.font.SysFont("comicsans", 30, True).render(
            "Level: " + str(self.game.level), 1, (0, 0, 0)
        )
        self.win.blit(text, (self.size[0] - 150, 60))

    def drawPrepare(self):
        self.draw()
        text = pygame.font.SysFont("comicsans", 50, True).render(
            "Press 'S' to start!", 1, (0, 0, 255)
        )
        self.win.blit(
            text, (self.size[0] // 2 - text.get_size()[0] // 2, self.size[1] // 2 - 70)
        )
        text = pygame.font.SysFont("comicsans", 50, True).render(
            "Press 'H' to Help!", 1, (0, 0, 255)
        )
        self.win.blit(
            text, (self.size[0] // 2 - text.get_size()[0] // 2, self.size[1] // 2)
        )
        text = pygame.font.SysFont("comicsans", 50, True).render(
            "Press 'Q' to Quit!", 1, (0, 0, 255)
        )
        self.win.blit(
            text, (self.size[0] // 2 - text.get_size()[0] // 2, self.size[1] // 2 + 70)
        )

    def drawGameOver(self):
        self.draw()
        text = pygame.font.SysFont("comicsans", 50, True).render(
            "Gameover", 1, (0, 0, 255)
        )
        self.win.blit(text, (self.size[0] // 2 - 100, self.size[1] // 2))

    def drawLevelUp(self):
        self.draw()
        font = pygame.font.SysFont("comicsans", 50, True)

        text = font.render("Level Up", 1, (0, 0, 255))
        self.win.blit(text, (self.size[0] // 2 - 100, self.size[1] // 2))

    def showHelp(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.draw()
            text = pygame.font.SysFont("comicsans", 50, True).render(
                "Help", 1, (0, 0, 255)
            )
            self.win.blit(text, (self.size[0] // 2 - 100, self.size[1] // 2))
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                break
            pygame.display.update()
            pygame.time.delay(50)
