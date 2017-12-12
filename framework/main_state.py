import game_framework
import title_state
import random
import time

from pico2d import *
from player import Boy
from player import Bullet
from monster import Monster
from monster import Boss_Monster

name = "MainState"

Player_x = 100
boy = None
background = None
bullet = None
status_window = None
upgrade_icon = None
weapon_icon = None
dogs = None
boss_dog = None
Mon_death_count = 0
background_width = 1000
Stage = 1
Mon_number = 5

mouse_x, mouse_y = 0, 0


class Upgrade_icon:
    global mouse_x, mouse_y
    font = None

    def __init__(self):
        self.x1, self.y1 = 100, 50
        self.image1 = load_image('icon_att_up.png')
        self.x2, self.y2 = 200, 50
        self.image2 = load_image('icon_hp_up.png')
        self.x3, self.y3 = 300, 50
        self.image3 = load_image('icon_def_up.png')
        self.x4, self.y4 = 400, 50
        self.image4 = load_image('icon_heal_up.png')
        if self.font == None:
            self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.image1.clip_draw(0, 0, 60, 60, self.x1, self.y1)
        self.image2.clip_draw(0, 0, 60, 60, self.x2, self.y2)
        self.image3.clip_draw(0, 0, 60, 60, self.x3, self.y3)
        self.image4.clip_draw(0, 0, 60, 60, self.x4, self.y4)

class Weapon_icon:
    font = None

    def __init__(self):
        self.x = 700
        self.y = 50
        self.image1 = load_image('bullet.png')
        self.image2 = load_image('bullet2_icon.png')
        self.image3 = load_image('bullet3_icon.png')

    def draw(self, Bullet):
        if Bullet.type == 1:
            self.image1.clip_draw(0, 0, 75, 75, self.x, self.y)
        elif Bullet.type == 2:
            self.image2.clip_draw(0, 0, 75, 75, self.x, self.y)
        elif Bullet.type == 3:
            self.image3.clip_draw(0, 0, 75, 75, self.x, self.y)


class Background:
    global Stage
    font = None
    def __init__(self):
        self.x1, self.x2 = 0, background_width
        self.image1 = load_image('background.png')
        self.image2 = load_image('background2.png')
        self.image3 = load_image('background3.png')
        self.image4 = load_image('background4.png')
        if self.font == None:
            self.font = load_font('ENCR10B.TTF', 20)

    def update(self):
        self.x1 -= 4
        self.x2 -= 4
        if self.x1 <= -background_width:
            self.x1 = background_width
        if self.x2 <= -background_width:
            self.x2 = background_width

    def draw(self):
        if Stage % 20 <= 4 and Stage % 20 >= 0:
            self.image1.draw(self.x1 + (background_width/ 2), 250)
            self.image1.draw(self.x2 + (background_width / 2), 250)
        elif Stage % 20 <= 9 and Stage % 20 >= 5:
            self.image2.draw(self.x1 + (background_width/ 2), 250)
            self.image2.draw(self.x2 + (background_width / 2), 250)
        elif Stage % 20 <= 14 and Stage % 20 >= 10:
            self.image3.draw(self.x1 + (background_width/ 2), 250)
            self.image3.draw(self.x2 + (background_width / 2), 250)
        elif Stage % 20 <= 19 and Stage % 20 >= 15:
            self.image4.draw(self.x1 + (background_width/ 2), 250)
            self.image4.draw(self.x2 + (background_width / 2), 250)
        self.font.draw(600, 525, 'STAGE: %d' % Stage, (255, 255, 255))

class Statuswindow:
    def __init__(self):
        self.image = load_image('status_window.png')

    def draw(self):
        self.image.draw(400, 300)


def enter():
    global boy, dog, background, bullet, status_window, upgrade_icon, weapon_icon, dogs, boss_dog
    boy = Boy()
    background = Background()
    status_window = Statuswindow()
    bullet = Bullet(boy)
    dogs = [Monster(Stage) for i in range(5)]
    upgrade_icon = Upgrade_icon()
    weapon_icon = Weapon_icon()
    boss_dog = Boss_Monster(Stage)



def exit():
    global boy, background, bullet, status_window, icon, dogs, boss_dog
    del(boy)
    del(background)
    del(status_window)
    del(bullet)
    del(upgrade_icon)
    del(dogs)
    del(boss_dog)


def pause():
    pass


def resume():
    pass


def handle_events():
    global mouse_x, mouse_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.x, 600 - event.y
            boy.upgrade_update(mouse_x, mouse_y)


current_time = 0.0


def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def update():
    global current_time, Mon_death_count, Stage, dogs, Mon_number, boss_dog
    frame_time = get_frame_time()

    if boy.hp > 0:
        boy.update(frame_time)
        bullet.update(frame_time, boy)
        background.update()

        if Stage % 5 == 0:
            Mon_number = 6
            if boss_dog.x > 3000:
                boss_dog.__init__(Stage)
            boss_dog.update(frame_time, boy, bullet)
            boy.get_damage(boss_dog)
            if boss_dog.hp <= 0:
                boy.gold += 500 * (1.2 * (Stage - 1))
                boss_dog.__del__()
                bullet.type = random.randint(2, 3)
                Mon_death_count += 1
        else:
            Mon_number = 5
            boss_dog.x = 5000

        for dog in dogs:
            dog.update(frame_time, boy, bullet)
            boy.get_damage(dog)
            if dog.hp <= 0:
                boy.gold += 100 * (1.2*(Stage-1))
                dog.__del__()
                Mon_death_count += 1
        if (Mon_death_count >= Mon_number):
            Stage += 1
            for dog in dogs:
                dog.__init__(Stage)
            Mon_death_count = 0
    # player_damage = (boy.att * 10) / mon.defend
    delay(0.01)

def draw():
    clear_canvas()
    status_window.draw()
    background.draw()
    upgrade_icon.draw()
    weapon_icon.draw(bullet)
    boy.draw()
    for dog in dogs:
        dog.draw()
    boss_dog.draw()
    print(" Mon_death_count: %d" % Mon_death_count)
    bullet.draw()
    update_canvas()