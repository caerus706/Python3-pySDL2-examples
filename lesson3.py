from ctypes import c_long, pointer
import ctypes
from sdl2 import *
from sdl2.sdlimage import *

# screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
# tile size for scaling
TILE_SIZE = 40


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
def renderTexture(tex, ren, x, y, USE_TILE=False):
    # create destination rectangle to be at position we want
    dst = SDL_Rect(x, y)

    w = pointer(c_long(0))
    h = pointer(c_long(0))

    # Query texture to get its width and height to use
    if not USE_TILE:
        SDL_QueryTexture(tex, None, None, w, h)
        dst.w = w.contents.value
        dst.h = h.contents.value
    else:
        dst.w = TILE_SIZE
        dst.h = TILE_SIZE
    SDL_RenderCopy(ren, tex, None, dst)


# This is an attempt to follow C++ Syntax on my conversion
def main():
    SDL_Init(SDL_INIT_VIDEO)

    # there's no error checking at the moment
    # the interpreter will throw an error if there is a problem
    # no cleanup function built yet, will change if made

    win = SDL_CreateWindow(
        b"Lesson 3",
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
    resPath = "res/lesson3/"
    background = loadTexture(resPath + 'background.png', ren)
    image = loadTexture(resPath + 'image.png', ren)

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

        # Determine tiles needed to fill screen
        # make sure they're integers with int()
        xTiles = int(SCREEN_WIDTH / TILE_SIZE)
        yTiles = int(SCREEN_HEIGHT / TILE_SIZE)

        # Loop through the tiles
        # nested for loop was easier to code
        for horz in range(xTiles):
            for vert in range(yTiles):
                renderTexture(background,
                              ren,
                              horz * TILE_SIZE,
                              vert * TILE_SIZE,
                              True)

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
        SDL_Delay(1000)

    SDL_DestroyTexture(background)
    SDL_DestroyTexture(image)
    SDL_DestroyRenderer(ren)
    SDL_DestroyWindow(win)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    main()
