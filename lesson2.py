from ctypes import c_long, pointer
import ctypes
from sdl2 import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


# there are better ways to load textures
# I'm just trying to mirror the tutorial lesson as closely as possible
def loadTexture(filePath, renderer):
    # loads bmp image
    # str.encode() converts string to byte type
    loadedImage = SDL_LoadBMP(str.encode(filePath))

    if loadedImage:
        # creates texture from loadedImage
        texture = SDL_CreateTextureFromSurface(renderer, loadedImage)
        # free the loadedImage
        SDL_FreeSurface(loadedImage)

        if not texture:
            # error check to make sure texture loaded
            print("SDL_CreateTextureFromSurface")
    else:
        print("SDL_LoadBMP failed")
    return texture


def renderTexture(tex, ren, x, y):
    # create destination rectangle to be at position we want
    dst = SDL_Rect(x, y)

    w = pointer(c_long(0))
    h = pointer(c_long(0))

    # Query texture to get its width and height to use
    SDL_QueryTexture(tex, None, None, w, h)
    dst.w = w.contents.value
    dst.h = h.contents.value
    SDL_RenderCopy(ren, tex, None, dst)


# This is an attempt to follow C++ Syntax on my conversion
def main():
    SDL_Init(SDL_INIT_VIDEO)

    # there's no error checking at the moment
    # the interpreter will throw an error if there is a problem

    win = SDL_CreateWindow(
        b"Hello World",
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
    resPath = "res/lesson2/"
    background = loadTexture(resPath + 'background.bmp', ren)
    image = loadTexture(resPath + 'image.bmp', ren)

    # check if images loaded, destroy if not
    if not background or not image:
        if background:
            SDL_DestroyTexture(background)
        if image:
            SDL_DestroyTexture(image)
        SDL_DestroyRenderer(ren)
        SDL_DestroyWindow(win)
        SDL_Quit()

    event = SDL_Event()

    running = True
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break

        SDL_RenderClear(ren)

        # uses pointers to get width and height from the texture
        # so we know how much to move x, y to tile correctly
        bW = pointer(c_long(0))
        bH = pointer(c_long(0))
        SDL_QueryTexture(background, None, None, bW, bH)

        # pointers don't work the same here, had to add contents.value
        # we want to tile the background 4 times
        renderTexture(background, ren, 0, 0)
        renderTexture(background, ren, bW.contents.value, 0)
        renderTexture(background, ren, 0, bH.contents.value)
        renderTexture(background, ren, bW.contents.value, bH.contents.value)

        # we want to draw image in center of window
        iW = pointer(c_long(0))
        iH = pointer(c_long(0))
        SDL_QueryTexture(image, None, None, iW, iH)
        # cast to int to make sure we don't get a float
        x = int(SCREEN_WIDTH / 2 - iW.contents.value / 2)
        y = int(SCREEN_HEIGHT / 2 - iH.contents.value / 2)
        renderTexture(image, ren, x, y)

        # Update the screen
        SDL_RenderPresent(ren)
        # take short break
        SDL_Delay(100)

    SDL_DestroyTexture(background)
    SDL_DestroyTexture(image)
    SDL_DestroyRenderer(ren)
    SDL_DestroyWindow(win)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    main()
