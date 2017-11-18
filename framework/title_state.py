import game_framework
import main_state

from pico2d import *


name = "TitleState"
image = None
running = True

def enter():
    global image
    image = load_image('title.png')


def exit():
    global image
    del(image)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                running = False
            elif (event.type) == (SDL_KEYDOWN):
                game_framework.change_state(main_state)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def update():
    if not running:
        game_framework.quit()


def pause():
    pass


def resume():
    pass






