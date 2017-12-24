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

Pause = False
mouse_x, mouse_y = 0, 0
button_sound = None

class Upgrade_icon:
    global mouse_x, mouse_y
    font = None

    def __init__(self):
        self.x1, self.y1 = 100, 57
        self.image1 = load_image('image/icon_att_up.png')
        self.x2, self.y2 = 200, 57
        self.image2 = load_image('image/icon_hp_up.png')
        self.x3, self.y3 = 300, 57
        self.image3 = load_image('image/icon_def_up.png')
        self.x4, self.y4 = 400, 57
        self.image4 = load_image('image/icon_heal_up.png')
        if self.font == None:
            self.font = load_font('ENCR10B.TTF', 14)

    def draw(self):
        self.image1.clip_draw(0, 0, 60, 60, self.x1, self.y1)
        self.image2.clip_draw(0, 0, 60, 60, self.x2, self.y2)
        self.image3.clip_draw(0, 0, 60, 60, self.x3, self.y3)
        self.image4.clip_draw(0, 0, 60, 60, self.x4, self.y4)
        self.font.draw(80, 17, '%d' % boy.gold_att, (255, 255, 255))
        self.font.draw(180, 17, '%d' % boy.gold_hp, (255, 255, 255))
        self.font.draw(280, 17, '%d' % boy.gold_def, (255, 255, 255))
        self.font.draw(380, 17, '%d' % boy.gold_heal, (255, 255, 255))

class Weapon_icon:
    font = None

    def __init__(self):
        self.x = 700
        self.y = 50
        self.image = load_image('image/white.png')
        self.image1 = load_image('image/bullet.png')
        self.image2 = load_image('image/bullet2_icon.png')
        self.image3 = load_image('image/bullet3_icon.png')

    def draw(self, Bullet):
        self.image.clip_draw(0, 0, 75, 75, self.x, self.y)
        if Bullet.type == 1:
            self.image1.clip_draw(0, 0, 75, 75, self.x, self.y)
        elif Bullet.type == 2:
            self.image2.clip_draw(0, 0, 75, 75, self.x, self.y)
        elif Bullet.type == 3:
            self.image3.clip_draw(0, 0, 75, 75, self.x, self.y)


class Background:
    global Stage, Pause
    font = None
    def __init__(self):
        self.x1, self.x2 = 0, background_width
        self.image1 = load_image('image/background1.png')
        self.image2 = load_image('image/background2.png')
        self.image3 = load_image('image/background3.png')
        self.image4 = load_image('image/background4.png')
        self.Pause_image = load_image('image/pause.png')
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

        if Pause == True:
            self.Pause_image.clip_draw(0, 0, 300, 300, 400, 300)

class Statuswindow:
    def __init__(self):
        self.image = load_image('image/status_window.png')

    def draw(self):
        self.image.draw(400, 300)


def enter():
    global boy, dog, background, bullet, status_window\
        , upgrade_icon, weapon_icon, dogs, boss_dog, Mon_death_count, Stage, button_sound
    boy = Boy()
    background = Background()
    status_window = Statuswindow()
    bullet = Bullet(boy)
    dogs = [Monster(Stage) for i in range(5)]
    upgrade_icon = Upgrade_icon()
    weapon_icon = Weapon_icon()
    boss_dog = Boss_Monster(Stage)
    Mon_death_count = 0
    Stage = 1
    Bullet.type = 1
    button_sound = load_wav('sound/button_sound.wav')
    button_sound.set_volume(32)



def exit():
    global boy, background, bullet, status_window\
        , upgrade_icon, weapon_icon, dogs, boss_dog, Mon_death_count, Stage
    del(boy)
    del(background)
    del(status_window)
    del(bullet)
    del(upgrade_icon)
    del(weapon_icon)
    del(dogs)
    del(boss_dog)


def pause():
    pass


def resume():
    pass


def handle_events():
    global mouse_x, mouse_y, Mon_death_count, Stage, Pause, button_sound
    events = get_events()
    for event in events:
        if boy.isalive:
            if event.type == SDL_QUIT:
                exit()
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                if Pause == True:
                    Pause = False
                else:
                    Pause = True
            elif event.type == SDL_MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.x, 600 - event.y
                boy.upgrade_update(mouse_x, mouse_y, button_sound)
                if boy.find_weapon == True:
                    if mouse_y > 150 and 250 > mouse_y:
                        if mouse_x < 370 and mouse_x > 270:
                            bullet.type = boy.find_weapon_type
                            boy.find_weapon = False
                            Pause = False
                            button_sound.play()
                        elif mouse_x > 430 and mouse_x < 530:
                            boy.find_weapon = False
                            Pause = False
                            button_sound.play()

        elif boy.isalive == False:
            if event.type == SDL_KEYDOWN and event.key == SDLK_r:
                for dog in dogs:
                    dog.__init__(Stage)
                Mon_death_count = 0
                if Stage > 3:
                    Stage -= 3
                else:
                    Stage = 1
                boy.hp = boy.max_hp
                boy.isalive = True
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)


current_time = 0.0


def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def update():
    global current_time, Mon_death_count, Stage, dogs,\
        Mon_number, boss_dog, Pause
    frame_time = get_frame_time()

    if boy.hp <= 0:
        boy.isalive = False
        boy.hp = 0
        if boy.hp == 0:
            boy.death_sound.play(1)
            boy.hp = 0.001

    if boy.isalive and Pause == False:
        boy.update(frame_time)
        bullet.update(frame_time, boy)
        background.update()

        if Stage % 5 == 0:
            Mon_number = 6
            if boss_dog.x > 3000:
                boss_dog.__init__(Stage)
            boss_dog.update(frame_time, boy, bullet, Stage)
            boy.get_damage(boss_dog)
            if boss_dog.hp <= 0:
                boy.gold += 500 * (1.2 * (Stage - 1))
                boss_dog.__del__()
                Mon_death_count += 1
                boy.find_weapon_type = random.randint(1, 3)
                if boy.find_weapon_type == 1 and bullet.type != 1:
                    boy.find_weapon = True
                    Pause = True
                elif boy.find_weapon_type == 2 and bullet.type != 2:
                    boy.find_weapon = True
                    Pause = True
                elif boy.find_weapon_type == 3 and bullet.type != 3:
                    boy.find_weapon = True
                    Pause = True

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
        dog.draw(Stage)
    boss_dog.draw(Stage)
    print(" Mon_death_count: %d" % Mon_death_count)
    bullet.draw(boy)
    update_canvas()