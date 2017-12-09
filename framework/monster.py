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
        self.defend = 20 + ((Stage - 1) * 5)
        self.att = 20 + ((Stage - 1) * 3)
        self.Pdamage_count = 100
        self.frame = 0
        self.image = load_image('Dog.png')
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
        if self.x + 20  > Bullet.x + 30 and self.x < Bullet.x + 30:
            self.hp -= (Boy.att * 10) / self.defend

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 75, self.x, self.y)
        self.font.draw(self.x - 50, self.y + 50, 'HP: %0.2f' % self.hp, (255, 0, 0))