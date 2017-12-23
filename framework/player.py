
from pico2d import *

Player_x = 100

class Boy:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0             # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    font = None
    att, defend, max_hp, heal = 20, 10, 100, 0.25
    hp = max_hp
    gold = 400

    upgrade_att, upgrade_def, upgrade_hp, upgrade_heal = 10, 4, 50, 0.25
    gold_att, gold_def, gold_hp, gold_heal = 100, 100, 200, 100

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self):
        self.x, self.y = Player_x, 150
        self.frame = 0
        self.image = load_image('image/Cuphead_animation.png')
        self.image_damaged = load_image('image/Cuphead_damage.png')
        self.image_dead = load_image('image/Died.jpg')
        self.image_dead2 = load_image('image/cuphead_dead.png')
        self.dir = 1
        self.isalive = True
        self.getdamage = False
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
        if (Monster.x - 75 <= self.x) and Monster.Pdamage_count >= 30:
            self.getdamage = True
            self.hp -= (Monster.att * 10) /self.defend
            Monster.Pdamage_count = 0
        elif self.frame == 7:
            self.getdamage = False



    def upgrade_update(self, mouse_x, mouse_y):
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
                    self.gold = self.gold - self.gold_heal
                    self.gold_heal = self.gold_heal * 2

    def draw(self):
        if self.hp < 0:
            self.image_dead.clip_draw(0, 0, 560, 120, 400, 300)
            self.image_dead2.clip_draw((self.frame%3) * 86, 0, 98, 116, self.x, self.y)
        else:
            if self.getdamage:
                self.image_damaged.clip_draw(15 + self.frame * 100, 0, 98, 100, self.x, self.y)
            else:
                self.image.clip_draw(15 + self.frame * 100, 0, 98, 100, self.x, self.y)
        self.font.draw(50, 575, 'HP: %0.2f' % self.hp, (255, 0, 0))
        self.font.draw(50, 545, 'ATT: %0.2f' % self.att, (125, 0, 0))
        self.font.draw(250, 575, 'DEF: %0.2f' % self.defend, (0, 0, 255))
        self.font.draw(250, 545, 'RES: %0.2f' % self.heal, (255, 0, 100))
        self.font.draw(600, 575, 'GOLD: %d' % self.gold, (150, 100, 0))


class Bullet:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self, boy):
        self.x, self.y = Player_x + 50, 140
        self.type = 1
        self.frame = 0
        self.count = 0
        self.image1 = load_image('image/bullet.png')
        self.image2 = load_image('image/bullet2.png')
        self.image3 = load_image('image/bullet3.png')
        if self.type == 1:
            self.damage = boy.att
            self.Reach = 400
        elif self.type == 2:
            self.damage = boy.att * 1.5
            self.Reach = 600
        elif self.type == 3:
            self.damage = boy.att * 0.5
            self.Reach = 400

    def update(self, frame_time, boy):
        distance = Bullet.RUN_SPEED_PPS * frame_time

        if self.type == 1:
            self.damage = boy.att
        elif self.type == 2:
            self.damage = boy.att * 1.5
        elif self.type == 3:
            self.damage = boy.att * 0.5

        if self.type == 1 or self.type == 2:
            self.x += distance
            if self.x > (Player_x + self.Reach):
                self.x = Player_x + 50
        elif self.type == 3:
            self.count += 1
            self.x =  Player_x + 80
            self.frame += 1
            self.frame = self.frame % 2


    def draw(self):
        if self.type == 1:
            self.image1.clip_draw(0, 0, 75, 75, self.x, self.y)
        if self.type == 2:
            self.image2.clip_draw(0, 0, 214, 96, self.x, self.y)
        if self.type == 3:
            self.image3.clip_draw(500 * self.frame, 0, 500, 50, self.x + 150 , self.y)