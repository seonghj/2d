import game_framework
import main_state

from pico2d import *


name = "TitleState"
image = None
running = True

mouse_x, mouse_y = 0, 0

def enter():
    global image
    image = load_image('image/title.png')


def exit():
    global image
    del(image)


def handle_events():
    global running, mouse_x, mouse_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.x, 600 - event.y
            if (mouse_x > 150 and mouse_x < 300) and (mouse_y > 40 and mouse_y < 100):
                game_framework.change_state(main_state)
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                running = False

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






