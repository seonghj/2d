
from pico2d import *

Player_x = 100

class Boy:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0             # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    font = None
    gold = 400

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self):
        self.x, self.y = Player_x, 150
        self.frame = 0

        self.image = load_image('image/Cuphead_animation.png')
        self.image_damaged = load_image('image/Cuphead_damage.png')
        self.image_gameover = load_image('image/gameover.png')
        self.image_dead2 = load_image('image/cuphead_dead.png')
        self.bullet1_icon = load_image('image/bullet.png')
        self.bullet2_icon = load_image('image/bullet2_icon.png')
        self.bullet3_icon = load_image('image/bullet3_icon.png')
        self.find_weapon_window = load_image('image/change_weapon.png')

        self.death_sound = load_wav('sound/death.wav')
        self.death_sound.set_volume(100)
        self.damage_sound = load_wav('sound/damage.wav')
        self.damage_sound.set_volume(100)

        self.dir = 1
        self.upgrade_att, self.upgrade_def, self.upgrade_hp, self.upgrade_heal = 10, 0.5, 50, 0.5
        self.gold_att, self.gold_def, self.gold_hp, self.gold_heal = 100, 100, 200, 100
        self.att, self.defend, self.max_hp, self.heal = 20, 10, 100, 0.25
        self.hp = self.max_hp
        self.isalive = True
        self.getdamage = False
        self.find_weapon = False
        self.find_weapon_type = None
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
            self.damage_sound.play()
            self.getdamage = True
            self.hp -= (Monster.att * 10) /self.defend
            Monster.Pdamage_count = 0
        elif self.frame == 7:
            self.getdamage = False



    def upgrade_update(self, mouse_x, mouse_y, button_sound):
        if mouse_y > 35 and mouse_y < 95:
            if mouse_x > 70 and mouse_x < 130:
                button_sound.play()
                if (self.gold >=  self.gold_att):
                    self.att += self.upgrade_att
                    self.upgrade_att = self.upgrade_att * 1.5
                    self.gold = self.gold - self.gold_att
                    self.gold_att = self.gold_att * 2
                    button_sound.play()

            elif mouse_x > 170 and mouse_x < 230:
                button_sound.play()
                if (self.gold >= self.gold_hp):
                    self.max_hp += self.upgrade_hp
                    self.upgrade_hp = self.upgrade_hp * 1.5
                    self.gold = self.gold - self.gold_hp
                    self.gold_hp = self.gold_hp * 2
                    button_sound.play()

            elif mouse_x > 270 and mouse_x < 330:
                button_sound.play()
                if (self.gold >= self.gold_def):
                    self.defend += self.upgrade_def
                    self.upgrade_def = self.upgrade_def * 1.5
                    self.gold = self.gold - self.gold_def
                    self.gold_def = self.gold_def * 2

            elif mouse_x > 370 and mouse_x < 430:
                button_sound.play()
                if (self.gold >= self.gold_heal):
                    self.heal += self.upgrade_heal
                    self.gold = self.gold - self.gold_heal
                    self.gold_heal = self.gold_heal * 2

    def draw(self):
        if self.isalive == False:
            self.image_gameover.clip_draw(0, 0, 295, 295, 400, 300)
            self.image_dead2.clip_draw(80, 0, 90, 116, self.x, self.y)
        else:
            if self.getdamage:
                self.image_damaged.clip_draw(15 + self.frame * 100, 0, 98, 100, self.x, self.y)
            else:
                self.image.clip_draw(15 + self.frame * 100, 0, 98, 100, self.x, self.y)

        if self.find_weapon == True:
            self.find_weapon_window .clip_draw(0, 0, 300, 400, 400, 300)
            if self.find_weapon_type == 1:
                self.bullet1_icon.clip_draw(0, 0, 75, 75, 400, 300)
            elif self.find_weapon_type == 2:
                self.bullet2_icon.clip_draw(0, 0, 75, 75, 400, 300)
            elif self.find_weapon_type == 3:
                self.bullet3_icon.clip_draw(0, 0, 75, 75, 400, 300)

        self.font.draw(50, 575, 'HP: %0.2f' % self.hp, (255, 0, 0))
        self.font.draw(50, 545, 'ATT: %0.2f' % self.att, (125, 0, 0))
        self.font.draw(250, 575, 'DEF: %0.2f' % self.defend, (0, 0, 255))
        self.font.draw(250, 545, 'RES: %0.2f' % (self.heal* 10), (255, 0, 100))
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

        self.bullet1_sound = load_wav('sound/bullet1_sound.wav')
        self.bullet1_sound.set_volume(64)
        self.bullet2_sound = load_wav('sound/bullet2_sound.wav')
        self.bullet2_sound.set_volume(64)
        self.bullet3_sound = load_wav('sound/bullet3_sound.wav')
        self.bullet3_sound.set_volume(64)
        self.bullet3_sound_count = 0

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
            self.Reach = 400
        elif self.type == 2:
            self.damage = boy.att * 1.5
            self.Reach = 600
        elif self.type == 3:
            self.damage = boy.att * 0.5
            self.Reach = 400

        #sound
        if self.x ==  Player_x + 50:
            if self.type == 1:
                self.bullet1_sound.play()
            elif self.type == 2:
                self.bullet2_sound.play()

        if self.type == 1 or self.type == 2:
            self.x += distance
            if self.x > (Player_x + self.Reach):
                self.x = Player_x + 50
        elif self.type == 3:
            self.bullet3_sound_count += 1
            self.bullet3_sound_count = self.bullet3_sound_count % 35
            if self.bullet3_sound_count == 0 and boy.isalive == True:
                self.bullet3_sound.play()
            self.count += 1
            self.x =  Player_x + 80
            self.frame += 1
            self.frame = self.frame % 2



    def draw(self, boy):
        if self.type == 1:
            self.image1.clip_draw(0, 0, 75, 75, self.x, self.y)
        if self.type == 2:
            self.image2.clip_draw(0, 0, 214, 96, self.x, self.y)
        if self.type == 3 and boy.isalive == True:
            self.image3.clip_draw(500 * self.frame, 0, 500, 50, self.x + 150 , self.y)