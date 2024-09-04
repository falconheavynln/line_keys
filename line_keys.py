import pygame as py
from time import sleep
from math import sin, cos, pi
from levels import LEVELS

py.init()

WIDTH = 400
HEIGHT = 900
FPS = 60
LINELENGTH = 1000000
DLINEY = 800
SPEED = 5
COLOR = py.Color(255, 95, 95)
BUTTONCOLOR = py.Color(255, 52, 52)
BPOS = 100, 650, 200, 60
CAPTION = "Line Keys"
PATH = "assets"
ICON = "icon.png"

wd = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(CAPTION)
py.display.set_icon(py.image.load(ICON))


class Line(py.sprite.Sprite):
    def __init__(self, angle, parent):
        self.angle = angle
        self.parent = parent

    def draw(self):
        py.draw.line(
            wd,
            (0, 0, 0),
            (self.parent.x, self.parent.y),
            (
                self.parent.x + cos(2 * pi / 360 * self.angle) * LINELENGTH,
                self.parent.y + sin(2 * pi / 360 * self.angle) * LINELENGTH,
            ),
        )


class Node(py.sprite.Sprite):
    def __init__(self, x, angle, delay):
        self.x, self.y = x, -SPEED * delay * 60
        self.delay = delay
        self.angle = angle
        self.live = True
        self.lines = [Line(45 * (i + 1) + self.angle, self) for i in range(8)]

    def loop(self, transition):
        _ = [line.draw() for line in self.lines]
        py.draw.circle(wd, (0, 0, 0), (self.x, self.y), 10)
        py.draw.circle(wd, (255, 255, 255), (self.x, self.y), 7)
        if not transition:
            self.y += SPEED


def main():
    level_num, level_change = 1, True
    state, transition = "title", None
    hold, click = False, None

    clock = py.time.Clock()
    run = True
    while run:
        py.display.update()
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                break

        wd.fill(COLOR)
        if level_change:
            level = [Node(info[0], info[1], info[2]) for info in LEVELS[level_num - 1]]
            level_change = False
        if py.mouse.get_pressed(num_buttons=3)[0]:
            click = py.mouse.get_pos() if not click and not hold else None
            hold = True
        else:
            hold, click = False, None
        if state == "title":
            py.draw.rect(wd, BUTTONCOLOR, BPOS)
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
                py.draw.line(wd, (255, 255, 255), (0, DLINEY), (WIDTH, DLINEY), 10)
        if transition:
            py.draw.circle(
                wd,
                (BUTTONCOLOR.r, BUTTONCOLOR.g, BUTTONCOLOR.b, 5),
                transition[0],
                transition[1],
            )
            transition[1] += 10
            if transition[1] >= WIDTH * 3 or transition[1] >= HEIGHT * 3:
                transition = None
                state = "title"
    py.quit()
    quit()


if __name__ == "__main__":
    main()
