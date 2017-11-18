import random
import json
import os

from pico2d import *

import game_framework
import title_state



name = "MainState"

boy = None
background = None
font = None
pause_image = None
ispause = False
count = 0


class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def draw(self):
        self.image.draw(400, 250)


class Boy:
    def __init__(self):
        self.x, self.y = 100, 150
        self.frame = 0
        self.image = load_image('Cuphead_animation.png')
        self.dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        self.image.clip_draw(self.frame * 98, 0, 100, 100, self.x, self.y)


def enter():
    global boy, background, pause_image
    boy = Boy()
    background = Background()
    pause_image = load_image('pause.png')


def exit():
    global boy, grass
    del(boy)
    del(grass)


def pause():
    pass


def resume():
    pass


def handle_events():
    global ispause
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            ispause = not ispause


def update():
    global count, ispause
    boy.update()
    count = (count + 1) % 2
    if (ispause == True):
        boy.dir = 0
    else:
        boy.dir = 1


def draw():
    global ispause, count
    clear_canvas()
    background.draw()
    boy.draw()
    if (ispause == True and count == 0):
        pause_image.draw(400, 300)
    update_canvas()






