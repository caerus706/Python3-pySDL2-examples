from ctypes import c_long, pointer
import ctypes
from sdl2 import *
from sdl2.sdlttf import *

# screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


# there are better ways to load textures
# I'm just trying to mirror the tutorial lesson as closely as possible
def loadTexture(filePath, renderer):
    # loads bmp image
    # str.encode() converts string to byte type
    texture = IMG_LoadTexture(renderer, str.encode(filePath))

    if not texture:
        # To Do: error check to make sure texture loaded
        print("SDL_CreateTextureFromSurface")

    return texture

"""
Python doesn't really support function overloading. Instead we can set
default values to use if the function call doesn't include it.
"""


def renderTexture(tex, ren, x, y):
    # create destination rectangle to be at position we want
    dst = SDL_Rect(x, y)

    # create pointers to pass width and height to.
    w = pointer(c_long(0))
    h = pointer(c_long(0))

    # Query texture to get its width and height to use
    SDL_QueryTexture(tex, None, None, w, h)
    dst.w = w.contents.value
    dst.h = h.contents.value

    SDL_RenderCopy(ren, tex, None, dst)


def renderText(message, fontFile, color, fontSize, renderer):
    # open the font, remember to encode the fontFile for Python3
    font = TTF_OpenFont(str.encode(fontFile), fontSize)
    if not font:
        # To Do: Error checking, SDL_Destroy(*)
        SDL_Quit()
    # create text surface, encode the message to byte format
    surf = TTF_RenderText_Blended(font, str.encode(message), color)

    # create texture
    texture = SDL_CreateTextureFromSurface(renderer, surf)
    if not texture:
        # To Do: Error check for problem
        print("no texture")

    # Clean up loaded font and surface
    SDL_FreeSurface(surf)
    TTF_CloseFont(font)
    return texture


# This is an attempt to follow C++ Syntax on my conversion
def main():
    SDL_Init(SDL_INIT_VIDEO)

    # Forgot to initialize TTF
    # didn't throw error but refused to work
    tfi = TTF_Init()
    if tfi != 0:
        print("TTF_Init")
        exit(1)

    # there's no error checking at the moment
    # the interpreter will throw an error if there is a problem
    # no cleanup function built yet, will change if made

    win = SDL_CreateWindow(
        b"Lesson 6",
        100,
        100,
        640,
        480,
        SDL_WINDOW_SHOWN
        )

    # init renderer
    ren = SDL_CreateRenderer(
        win,
        -1,
        SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
        )

    # load image and create texture
    resPath = "res/lesson6/"
    color = SDL_Color(255, 255, 255, 255)
    image = renderText("TTF fonts are cool!",
                       resPath + "sample.ttf",
                       color,
                       64,
                       ren)

    # we want to draw image in center of window
    iW = pointer(c_long(0))
    iH = pointer(c_long(0))
    SDL_QueryTexture(image, None, None, iW, iH)
    # cast to int to make sure we don't get a float
    x = int(SCREEN_WIDTH / 2 - iW.contents.value / 2)
    y = int(SCREEN_HEIGHT / 2 - iH.contents.value / 2)

    # create event to check in loop
    event = SDL_Event()

    # running allows us to break out of loop by setting to false
    running = True
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            # check for quit
            if event.type == SDL_QUIT:
                running = False
                break

            if event.type == SDL_MOUSEBUTTONDOWN:
                running = False
                break

            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False

        SDL_RenderClear(ren)

        renderTexture(image, ren, x, y)

        # Update the screen
        SDL_RenderPresent(ren)
        # take short break
        SDL_Delay(1000)

    SDL_DestroyTexture(image)
    SDL_DestroyRenderer(ren)
    SDL_DestroyWindow(win)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    main()
