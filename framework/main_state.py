import game_framework
import title_state
import random
import player
import time

from pico2d import *

name = "MainState"

Player_x = 100
boy = None
background = None
bullet = None
status_window = None
icon = None
dogs = None
Mon_death_count = 0
background_width = 1000

mouse_x, mouse_y = 0, 0

class Boy:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0             # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    font = None
    Reach = 400
    att, defend, max_hp, heal = 20, 10, 100, 1
    hp = max_hp
    gold = 10000

    upgrade_att, upgrade_def, upgrade_hp, upgrade_heal = 10, 4, 50, 1
    gold_att, gold_def, gold_hp, gold_heal = 100, 100, 100, 100

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self):
        self.x, self.y = Player_x, 150
        self.frame = 0
        self.image = load_image('Cuphead_animation.png')
        self.dir = 1
        self.total_frames = 0.0
        if self.font == None:
            self.font = load_font('ENCR10B.TTF', 20)

    def update(self, frame_time):
        self.total_frames += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        if self.hp < self.max_hp:
            if (self.hp + self.heal) > self.max_hp:
                self.hp = self.max_hp
            else:
                self.hp += self.heal

    def get_damage(self, Monster):
        Monster.Pdamage_count += 1
        if (Monster.x - 75 <= boy.x) and Monster.Pdamage_count >= 50:
            boy.hp -= (Monster.att * 10) / boy.defend
            Monster.Pdamage_count = 0




    def upgrade_update(self):
        if mouse_y > 20 and mouse_y < 80:
            if mouse_x > 70 and mouse_x < 130:
                if (self.gold >=  self.gold_att):
                    self.att += self.upgrade_att
                    self.upgrade_att = self.upgrade_att * 1.5
                    self.gold = self.gold - self.gold_att
                    self.gold_att = self.gold_att * 2

            elif mouse_x > 170 and mouse_x < 230:
                if (self.gold >= self.gold_hp):
                    self.max_hp += self.upgrade_hp
                    self.upgrade_hp = self.upgrade_hp * 1.5
                    self.gold = self.gold - self.gold_hp
                    self.gold_hp = self.gold_hp * 2

            elif mouse_x > 270 and mouse_x < 330:
                if (self.gold >= self.gold_def):
                    self.defend += self.upgrade_def
                    self.upgrade_def = self.upgrade_def * 1.5
                    self.gold = self.gold - self.gold_def
                    self.gold_def = self.gold_def * 2

            elif mouse_x > 370 and mouse_x < 430:
                if (self.gold >= self.gold_heal):
                    self.heal += self.upgrade_heal
                    self.upgrade_heal = self.upgrade_heal * 1.5
                    gold = self.gold - self.gold_heal
                    self.gold_heal = self.gold_heal * 2

    def draw(self):
        self.image.clip_draw(15 + self.frame * 100, 0, 98, 100, self.x, self.y)
        self.font.draw(50, 575, 'HP: %0.2f' % self.hp, (255, 0, 0))
        self.font.draw(50, 545, 'ATT: %0.2f' % self.att, (125, 0, 0))
        self.font.draw(250, 575, 'DEF: %0.2f' % self.defend, (0, 0, 255))
        self.font.draw(250, 545, 'RES: %0.2f' % self.heal, (255, 0, 100))
        self.font.draw(650, 575, 'GOLD: %d' % self.gold, (255, 100, 0))

class Monster:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 9

    font = None

    def __init__(self):
        self.x, self.y = random.randint(650, 1500) ,150
        self.hp = 50
        self.defend = 40
        self.att = 20
        self.Pdamage_count = 100
        self.frame = 0
        self.image = load_image('Dog.png')
        self.dir = 1
        self.total_frames = 0.0
        if self.font == None:
            self.font = load_font('ENCR10B.TTF', 20)

    def __del__(self):
        global Mon_death_count
        self.x = 5000
        self.hp = 9999999
        Mon_death_count += 1

    def update(self, frame_time, Boy, Bullet):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        if self.x - 75 > Boy.x:
            self.x -= 5
        if self.x + 20  > Bullet.x + 30 and self.x < Bullet.x + 30:
            self.hp -= (Boy.att * 10) / self.defend

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 75, self.x, self.y)
        self.font.draw(self.x, self.y + 50, 'HP: %0.2f' % self.hp, (255, 0, 0))


class Bullet:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.x, self.y = Player_x + 50, 140
        self.image = load_image('bullet.png')

    def update(self, frame_time, Boy):
        distance = Bullet.RUN_SPEED_PPS * frame_time
        self.x += distance
        if self.x > (Player_x + Boy.Reach):
            self.x = Player_x + 50

    def draw(self):
        self.image.clip_draw(0, 0, 75, 75, self.x, self.y)

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


class Background:
    def __init__(self):
        self.x1, self.x2 = 0, background_width
        self.image1 = load_image('background.png')
        self.image2 = load_image('background.png')

    def update(self):
        self.x1 -= 4
        self.x2 -= 4
        if self.x1 <= -background_width:
            self.x1 = background_width
        if self.x2 <= -background_width:
            self.x2 = background_width

    def draw(self):
        self.image1.draw(self.x1 + (background_width/ 2), 250)
        self.image1.draw(self.x2 + (background_width / 2), 250)

class Statuswindow:
    def __init__(self):
        self.image = load_image('status_window.png')

    def draw(self):
        self.image.draw(400, 300)


def enter():
    global boy, dog, background, bullet, status_window, icon, dogs
    boy = Boy()
    background = Background()
    status_window = Statuswindow()
    bullet = Bullet()
    dogs = [Monster() for i in range(5)]
    icon = Upgrade_icon()


def exit():
    global boy, background, bullet, status_window, icon, dogs
    del(boy)
    del(background)
    del(status_window)
    del(bullet)
    del(icon)
    del(dogs)


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
            boy.upgrade_update()


current_time = 0.0


def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def update():
    global current_time, Mon_death_count
    frame_time = get_frame_time()
    boy.update(frame_time)
    bullet.update(frame_time, boy)
    background.update()

    for dog in dogs:
        dog.update(frame_time, boy, bullet)
        boy.get_damage(dog)
        if dog.hp <= 0:
            boy.gold += 200
            dog.__del__()

    if (Mon_death_count >= 5):
        for dog in dogs:
            dog.__init__()
        Mon_death_count = 0
    # player_damage = (boy.att * 10) / mon.defend
    delay(0.02)

def draw():
    clear_canvas()
    status_window.draw()
    background.draw()
    icon.draw()
    boy.draw()
    for dog in dogs:
        dog.draw()
    print(" Mon_death_count: %d" % Mon_death_count)
    bullet.draw()
    update_canvas()