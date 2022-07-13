# StartMenu
# 1.[1pt] Start - Instead of starting the game directly add a button / key for it.
#   For example, the bird should start moving only after space is pressed.
#   In such a case, you should also display text to let players know what to press to start the game.

# Ending
# 1. [1pt] End screen - Instead of closing the application on colliding, display the ending screen with the result: win/lose.

# Audio
#  [0.5pt] Crash sound -  Add sound when collision happens.


import random
import time
import pygame

class Bird:
    def __init__(self, X, Y, R, screen):
        self.X = X
        self.Y = Y
        self.R = R
        self.screen = screen

    def render(self):
        pygame.draw.circle(self.screen, pygame.Color("red"), (self.X, self.Y), self.R)

    def move(self):
        self.X += 4

    def fall_down(self):
        self.Y += 3

    def win(self):
        return self.X > 1200 - self.R

    def collide_border(self):
        return self.Y <= self.R or self.Y >= 700 - self.R


class Pipes:
    def __init__(self, screen):
        self.X = [random.randint(150, 200), random.randint(500, 550), random.randint(800, 900), random.randint(350, 400), random.randint(650, 700), random.randint(1050, 1100)]
        self.Y = [random.randint(400, 500),  random.randint(400, 550), random.randint(400, 650)]
        self.screen = screen
        self.height = [random.randint(100, 300), random.randint(100, 300), random.randint(100, 400)]
        self.width = 50

    def render_Up(self):
        for i in range(3):
            pygame.draw.line(self.screen, pygame.Color((84, 5, 168)), [self.X[i], 0],
                             [self.X[i], self.height[i]], self.width)

    def render_Down(self):
        for i in range(3):
            pygame.draw.line(self.screen, pygame.Color((84, 5, 168)), [self.X[i+3], self.Y[i]],
                            [self.X[i+3], 700], self.width)

    def collide(self, x, y):
        for i in range(3):
            if self.X[i] - 20 <= x <= self.X[i] + self.width + 20 and y < self.height[i] + 20:
                return True
        for i in range(3):
            if self.X[i+3] - 20 <= x <= self.X[i+3] + self.width + 20 and y > self.Y[i] - 20:
                return True


pygame.init()

class App:
    
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.bird = None
        self.pipe = None
        self.start = False
        self.end = False

    def run(self):
        while not self.start:
            self.init()
            time.sleep(0.1)
        while self.running:
            self.update()
            self.render()
        while self.end:
            self.cleanUp()
            time.sleep(2.)

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Flappy Bird")

        self.screen.fill((18, 204, 255))

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 100)

        self.screen.blit(font.render('--Flappy Bird--', False, pygame.Color(84, 5, 168)), (250, 150))

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 50)

        self.screen.blit(font.render('Press Space to Play!', False, pygame.Color(84, 5, 168)), (360, 350))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.start = True

        if self.start:
            self.clock = pygame.time.Clock()
            self.running = True

            self.bird = Bird(30, 350, 20, self.screen)
            self.pipe = Pipes(self.screen)


    def update(self):
        self.events()
        self.bird.move()
        self.bird.fall_down()

        if self.bird.win():
            self.end = True
            self.running = False

        if self.bird.collide_border():
            pygame.mixer.Sound.play(pygame.mixer.Sound("hit.mp3"))
            self.end = True
            self.running = False

        if self.pipe.collide(self.bird.X, self.bird.Y):
            pygame.mixer.Sound.play(pygame.mixer.Sound("hit.mp3"))
            self.end = True
            self.running = False


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.bird.Y -= 90

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.bird.Y -= 15
            self.bird.X += 4


    def render(self):
        self.screen.fill((18, 204, 255))
        self.bird.render()
        self.pipe.render_Up()
        self.pipe.render_Down()
        pygame.display.flip()
        self.clock.tick(60)

    def cleanUp(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Flappy Bird")

        self.screen.fill((18, 204, 255))

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 100)
        if self.bird.win():
            self.screen.blit(font.render('You Won!', False, pygame.Color(84, 5, 168)), (400, 250))
        else:
            self.screen.blit(font.render('You Lost', False, pygame.Color(84, 5, 168)), (400, 250))
        pygame.display.flip()

        self.end = False

if __name__ == "__main__":
    app = App()
    app.run()