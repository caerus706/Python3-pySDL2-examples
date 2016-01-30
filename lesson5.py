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


# lesson 3 of the c++ uses function overloading
# which doesn't do anything new for this
def renderTexture(tex, ren, x, y, useClip=None, USE_CLIP=False):
    # create destination rectangle to be at position we want

    dst = SDL_Rect(x, y)
    clipRec = SDL_Rect(x, y)

    w = pointer(c_long(0))
    h = pointer(c_long(0))

    if USE_CLIP:
        SDL_QueryTexture(tex, None, None, w, h)
        dst.w = w.contents.value
        dst.h = h.contents.value
        # print(w.contents.value, h.contents.value)
        clipRec.x = int((useClip['x'] * (w.contents.value / 2)))
        clipRec.y = int((useClip['y'] * (h.contents.value / 2)))
        clipRec.w = int(w.contents.value / 2)
        clipRec.h = int(h.contents.value / 2)
        # print(dst)
        # print(clipRec)

    # Query texture to get its width and height to use
    SDL_QueryTexture(tex, None, None, w, h)
    dst.w = w.contents.value
    dst.h = h.contents.value
    if not USE_CLIP:
        SDL_RenderCopy(ren, tex, None, dst)
    else:
        SDL_RenderCopy(ren, tex, clipRec, dst)


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
    useClip = {'x': 0, 'y': 0}

    event = SDL_Event()

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
                    useClip['x'] = 0
                    useClip['y'] = 0
                if event.key.keysym.sym == SDLK_2:
                    useClip['x'] = 1
                    useClip['y'] = 0
                if event.key.keysym.sym == SDLK_3:
                    useClip['x'] = 0
                    useClip['y'] = 1
                if event.key.keysym.sym == SDLK_4:
                    useClip['x'] = 1
                    useClip['y'] = 1
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False

        SDL_RenderClear(ren)

        # we want to draw image in center of window
        iW = pointer(c_long(0))
        iH = pointer(c_long(0))
        SDL_QueryTexture(image, None, None, iW, iH)
        # cast to int to make sure we don't get a float
        x = int(SCREEN_WIDTH / 2 - iW.contents.value / 2)
        y = int(SCREEN_HEIGHT / 2 - iH.contents.value / 2)

        # renderTexture(image, ren, x, y)
        # print(useClip['x'], useClip['y'])
        renderTexture(image, ren, x, y, useClip, USE_CLIP=True)

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
