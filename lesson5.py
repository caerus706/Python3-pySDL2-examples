from ctypes import c_long, pointer
import ctypes
from sdl2 import *
from sdl2.sdlimage import *

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
        # error check to make sure texture loaded
        print("SDL_CreateTextureFromSurface")

    return texture

"""
Python doesn't really support function overloading. Instead we can set
default values to use if the function call doesn't include it.
"""


def renderTexture(tex, ren, x, y, clip=None):
    # create destination rectangle to be at position we want
    dst = SDL_Rect(x, y)

    # create pointers to pass width and height to.
    w = pointer(c_long(0))
    h = pointer(c_long(0))

    # Query texture to get its width and height to use
    SDL_QueryTexture(tex, None, None, w, h)
    dst.w = w.contents.value
    dst.h = h.contents.value
    if not clip:
        SDL_RenderCopy(ren, tex, None, dst)
    else:
        SDL_RenderCopy(ren, tex, clip, dst)


# This is an attempt to follow C++ Syntax on my conversion
def main():
    SDL_Init(SDL_INIT_VIDEO)

    # there's no error checking at the moment
    # the interpreter will throw an error if there is a problem
    # no cleanup function built yet, will change if made

    win = SDL_CreateWindow(
        b"Lesson 5",
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
    resPath = "res/lesson5/"
    image = loadTexture(resPath + 'image.png', ren)

    # check if images loaded, destroy if not
    if not image:
        SDL_DestroyRenderer(ren)
        SDL_DestroyWindow(win)
        SDL_Quit()

    # Initial clip to use
    useClip = 0
    # clip width and height is 100 and will simply be preset
    cW, cH = 100, 100
    # create list for rectangles
    clips = []
    # make loop to define the position
    """
    this one was difficult, numbers act different in python than c++
    in c++ it's already an int from the for loop, but python doesn't
    determine type until after the math is done. The solution is to make
    sure i is kept as an int after division to have this calculate correctly.
    """
    for i in range(4):
        clip = SDL_Rect(
            int(i / 2) * cW,
            i % 2 * cH,
            cW,
            cH)
        clips.append(clip)

    # using cW, cH set me offscreen slightly
    iW, iH = 200, 200

    x = int(SCREEN_WIDTH / 2 - iW / 2)
    y = int(SCREEN_HEIGHT / 2 - iH / 2)

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
                if event.key.keysym.sym == SDLK_1:
                    useClip = 0
                if event.key.keysym.sym == SDLK_2:
                    useClip = 1
                if event.key.keysym.sym == SDLK_3:
                    useClip = 2
                if event.key.keysym.sym == SDLK_4:
                    useClip = 3
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False

        SDL_RenderClear(ren)

        renderTexture(image, ren, x, y, clips[useClip])

        # Update the screen
        SDL_RenderPresent(ren)
        # take short break
        SDL_Delay(350)

    SDL_DestroyTexture(image)
    SDL_DestroyRenderer(ren)
    SDL_DestroyWindow(win)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    main()
