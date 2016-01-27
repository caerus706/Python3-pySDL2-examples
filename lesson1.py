import ctypes
from sdl2 import *


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
        SDL_RENDERER_ACCELERATED
        )

    # straight import path instead of dynamic loading for now
    bmp = SDL_LoadBMP(b"res/lesson1/hello.bmp")

    tex = SDL_CreateTextureFromSurface(ren, bmp)

    SDL_FreeSurface(bmp)

    event = SDL_Event()

    running = True
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break

        SDL_RenderClear(ren)
        SDL_RenderCopy(ren, tex, None, None)
        SDL_RenderPresent(ren)
        SDL_Delay(100)

    SDL_DestroyTexture(tex)
    SDL_DestroyRenderer(ren)
    SDL_DestroyWindow(win)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    main()
