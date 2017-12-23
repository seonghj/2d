from pico2d import *
import random

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

    def __init__(self, Stage):
        self.x, self.y = random.randint(650, 2000) ,150
        self.hp = 50 + (25 * (Stage - 1))
        self.defend = 20 + ((Stage - 1) * 2)
        self.att = 20 + ((Stage - 1) * 3)
        self.Pdamage_count = 100
        self.frame = 0
        self.image = load_image('image/Dog.png')
        self.dir = 1
        self.total_frames = 0.0
        if self.font == None:
            self.font = load_font('ENCR10B.TTF', 20)

    def __del__(self):
        self.x = 5000
        self.hp = 9999999

    def update(self, frame_time, Boy, Bullet):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        if self.x - 75 > Boy.x :
            self.x -= 5
        if self.x > 3000:
            self.x += 5


        if Bullet.type == 1 or Bullet.type == 2:
            if self.x + 20  > Bullet.x + 30 and self.x < Bullet.x + 30:
                self.hp -= (Bullet.damage * 10) / self.defend
        elif Bullet.type == 3:
            if self.x < Boy.x + Bullet.Reach and Bullet.count % 5 == 2:
                self.hp -= (Bullet.damage * 10) / self.defend

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 75, self.x, self.y)
        self.font.draw(self.x - 50, self.y + 50, 'HP: %0.2f' % self.hp, (255, 0, 0))

class Boss_Monster:
    PIXEL_PER_METER = (1.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 9

    font = None

    def __init__(self, Stage):
        self.x, self.y = 2000 ,150
        self.hp = 500 + (150 * (Stage - 1))
        self.defend = 50 + ((Stage - 1) * 5)
        self.att = 20 + ((Stage - 1) * 20)
        self.Pdamage_count = 1006
        self.frame = 0
        self.image = load_image('image/Dog_boss.png')
        self.dir = 1
        self.total_frames = 0.0
        if self.font == None:
            self.font = load_font('ENCR10B.TTF', 20)

    def __del__(self):
        self.x = 5000
        self.hp = 9999999

    def update(self, frame_time, Boy, Bullet):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        if self.x - 75 > Boy.x:
            self.x -= 5

        if Bullet.type == 1 or Bullet.type == 2:
            if self.x + 20  > Bullet.x + 30 and self.x < Bullet.x + 30:
                self.hp -= (Bullet.damage * 10) / self.defend
        elif Bullet.type == 3:
            Bullet.count += 1
            if self.x < Boy.x + Bullet.Reach and Bullet.count % 5 == 2:
                self.hp -= (Bullet.damage * 10) / self.defend

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 75, self.x, self.y)
        self.font.draw(self.x - 50, self.y + 50, 'HP: %0.2f' % self.hp, (255, 0, 0))
        self.font.draw(self.x - 10, self.y + 80, 'BOSS', (0, 0, 255))