import pygame
from time import sleep
from math import sin, cos, pi
from levels import LEVELS

pygame.init

WIDTH = 400
HEIGHT = 900
FPS = 60
LINELENGTH = 1000000
DLINEY = 800
SPEED = 5
COLOR = (255, 95, 95)
BUTTONCOLOR = (255, 52, 52)
BPOS = (100, 650, 200, 60)
CAPTION = "Line Keys"
PATH = "assets"
ICON = "icon.png"

wd = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(ICON))


class Line(pygame.sprite.Sprite):
    def __init__(self, angle, parent):
        self.angle = angle
        self.parent = parent

    def draw(self):
        pygame.draw.line(
            wd,
            (0, 0, 0),
            (self.parent.x, self.parent.y),
            (
                self.parent.x + cos(2 * pi / 360 * self.angle) * LINELENGTH,
                self.parent.y + sin(2 * pi / 360 * self.angle) * LINELENGTH,
            ),
        )


class Node(pygame.sprite.Sprite):
    def __init__(self, x, angle, delay):
        self.x, self.y = x, -SPEED * delay * 60
        self.delay = delay
        self.angle = angle
        self.live = True
        self.lines = [Line(45 * (i + 1) + self.angle, self) for i in range(8)]

    def loop(self, transition):
        _ = [line.draw() for line in self.lines]
        pygame.draw.circle(wd, (0, 0, 0), (self.x, self.y), 10)
        pygame.draw.circle(wd, (255, 255, 255), (self.x, self.y), 7)
        if not transition:
            self.y += SPEED


def main():
    level_num, level_change = 1, True
    state, transition = "title", None
    hold, click = False, None

    clock = pygame.time.Clock()
    run = True
    while run:
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        wd.fill(COLOR)
        if level_change:
            level = [Node(info[0], info[1], info[2]) for info in LEVELS[level_num - 1]]
            level_change = False
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            click = pygame.mouse.get_pos() if not click and not hold else None
            hold = True
        else:
            hold, click = False, None
        if state == "title":
            pygame.draw.rect(wd, BUTTONCOLOR, BPOS)
            if click:
                if (
                    BPOS[0] <= click[0] <= BPOS[0] + BPOS[2]
                    and BPOS[1] <= click[1] <= BPOS[1] + BPOS[3]
                ):
                    state = "playing"
        elif state == "playing":
            for node in level:
                node.loop(transition)
                if node.y + SPEED >= DLINEY and not transition:
                    sleep(1)
                    transition = [[node.x, DLINEY], 0]
                pygame.draw.line(wd, (255, 255, 255), (0, DLINEY), (WIDTH, DLINEY), 10)
        if transition:
            pygame.draw.circle(wd, BUTTONCOLOR, transition[0], transition[1])
            transition[1] += 10
            print("fhek")
            if transition[1] >= WIDTH * 3 or transition[1] >= HEIGHT * 3:
                transition = None
                state = "title"
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
