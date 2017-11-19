
from pico2d import *

Player_x = 100
class Boy:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0             # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    Reach = 400

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self):
        self.x, self.y = Player_x, 150
        self.frame = 0
        self.image = load_image('Cuphead_animation.png')
        self.dir = 1
        self.total_frames = 0.0

    def update(self, frame_time):
        self.total_frames += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8

    def draw(self):
        self.image.clip_draw(self.frame * 98, 0, 100, 100, self.x, self.y)

class Bullet:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.x, self.y = 175, 150
        self.image = load_image('bullet.png')

    def update(self, frame_time, Reach):
        distance = Bullet.RUN_SPEED_PPS * frame_time
        self.x += distance
        if self.x > (Player_x + Reach):
            self.x = Player_x + 75

    def draw(self):
        self.image.clip_draw(0, 0, 75, 75, self.x, self.y)

class Upgrade_icon:
    def __init__(self):
        self.x1, self.y1 = 100, 50
        self.image1 = load_image('icon_att_up.png')
        self.x2, self.y2 = 200, 50
        self.image2 = load_image('icon_hp_up.png')
        self.x3, self.y3 = 300, 50
        self.image3 = load_image('icon_def_up.png')
        self.x4, self.y4 = 400, 50
        self.image4 = load_image('icon_heal_up.png')

    def draw(self):
        self.image1.clip_draw(0, 0, 60, 60, self.x1, self.y1)
        self.image2.clip_draw(0, 0, 60, 60, self.x2, self.y2)
        self.image3.clip_draw(0, 0, 60, 60, self.x3, self.y3)
        self.image4.clip_draw(0, 0, 60, 60, self.x4, self.y4)
