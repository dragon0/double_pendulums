import pygame
from math import sin, cos, pi
G = 1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Double Pendulumses")
        self.clock = pygame.time.Clock()
        self.running = True
        self.p1 = p1 = Pendulum(320, 20, 200, 40, pi/4)
        self.p2 = Pendulum(p1.x, p1.y, 200, 40, pi/8, p1)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self._events()
            self._update()
            self._draw()

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    def _update(self):
        accelerate(self.p1, self.p2)
        self.p1.update()
        self.p2.update()

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        pygame.display.flip()

class Pendulum:
    def __init__(self, x, y, l, m, t, parent=None):
        self.parent = parent
        self.cx = x
        self.cy = y
        self.x = x + l * sin(t)
        self.y = y + l * cos(t)
        self.m = m
        self.t = t
        self.l = l
        self.v = 0
        self.a = 0

    def update(self):
        if self.parent:
            self.cx = self.parent.x
            self.cy = self.parent.y
        self.v += self.a
        self.t += self.v
        self.x = self.cx + self.l * sin(self.t)
        self.y = self.cy + self.l * cos(self.t)

    def draw(self, surface):
        cx = int(self.cx)
        cy = int(self.cy)
        x = int(self.x)
        y = int(self.y)
        m = int(self.m)
        pygame.draw.line(surface, (255,255,255), (cx, cy), (x, y))
        pygame.draw.circle(surface, (255,0,0), (x, y), m)

    def __str__(self):
        return "Pendulum({self.x}, {self.y}, {self.t})".format(self=self)

def accelerate(p1, p2):
    n1 = -G * (2 * p1.m + p2.m) * sin(p1.t)
    n2 = p2.m * G * sin(p1.t - 2 * p2.t)
    n3 = 2 * sin(p1.t - p2.t) * p2.m * (p2.v**2 * p2.l + p1.v**2 * p1.l * cos(p1.t - p2.t))
    d = p1.l * (2 * p1.m + p2.m - p2.m * cos(2*p1.t - 2*p2.t))
    p1.a = (n1 - n2 - n3) / d

    n1 = 2 * sin(p1.t - p2.t)
    n2 = p1.v**2 * p1.l * (p1.m + p2.m)
    n3 = G * (p1.m + p2.m) * cos(p1.t)
    n4 = p2.v**2 * p2.l * p2.m * cos(p1.t - p2.t)
    d = p2.l * (2 * p1.m + p2.m - p2.m * cos(2 * p1.t - 2 * p2.t))
    p2.a = (n1 * (n2 + n3 + n4)) / d

if __name__ == '__main__':
    game = Game()
    game.run()

