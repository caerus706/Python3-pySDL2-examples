import os
from sys import exit
from ctypes import c_long, pointer

# set your path here if you need to
# sdlpath = os.path.join(os.getcwd(), 'dll')
# os.environ['PYSDL2_DLL_PATH'] = sdlpath

from sdl2 import *
from sdl2.sdlttf import *


def renderTexture(tex, ren, x, y):
    """
    :type ren: SDL_Renderer
    :type tex: SDL_Texture
    """

    # Setup the destination rectangle to be at the position we want
    # x and y passed through as long pointer
    dst = SDL_Rect(int(x), int(y))
    w = pointer(c_long(0))
    h = pointer(c_long(0))
    # Query the texture to get its width and height to use
    SDL_QueryTexture(tex, None, None, w, h)
    dst.w = w.contents.value
    dst.h = h.contents.value
    SDL_RenderCopy(ren, tex, None, dst)


def renderText(message, fontFile, color, fontSize, renderer):
    """

    :rtype : SDL_Texture
    """
    # Open the font
    SDL_ClearError()
    try:
        # assume python 3 and encode as byte
        font = TTF_OpenFont(str.encode(fontFile), fontSize)
    except:
        p3 = SDL_GetError()
        try:
            # python 2 import
            font = TTF_OpenFont(fontFile, fontSize)
        except:
            p2 = SDL_GetError()
        if font is None or not p2 == '' or not p3 == '':
            print("TTF_OpenFont error: ", p2, p3)
            return None

    # We need to first render to a surface as that's what TTF_RenderText
    # returns, then load that surface into a texture
    try:
        # message also expected as byte format
        surf = TTF_RenderText_Blended(font, str.encode(message), color)
    except:
        try:
            surf = TTF_RenderText_Blended(font, message, color)
        except:
            pass

    if surf is None:
        TTF_CloseFont(font)
        print("TTF_RenderText")
        return None

    texture = SDL_CreateTextureFromSurface(renderer, surf)
    if texture is None:
        print("CreateTexture")

    # Clean up the surface and font
    SDL_FreeSurface(surf)
    TTF_CloseFont(font)
    return texture

SDL_Init(SDL_INIT_VIDEO)
# Create an application window with the following settings:
try:
    window = SDL_CreateWindow(
        b"SDL2 TTF test",  # window title
        SDL_WINDOWPOS_CENTERED,  # initial x position
        SDL_WINDOWPOS_CENTERED,  # initial y position
        640,  # width, in pixels
        480,  # height, in pixels
        SDL_WINDOW_RESIZABLE  # flags
    )
except:
    # used from another file because first didn't work
    window = SDL_CreateWindow(
        b'SDL2 TTF test 2',
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        640,
        480,
        SDL_WINDOW_SHOWN)

renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

tfi = TTF_Init()
if tfi != 0:
    print("TTF_Init")
    exit(1)

# We'll render the string "TTF fonts are cool!" in white
# Color is in RGB format
color = SDL_Color(255, 255, 255)

font = "Arial"
fontpath = os.path.join(os.environ["windir"], "Fonts", font + ".ttf")

# custom font used in original example
# fontpath = os.path.join(os.path.dirname(__file__), 'font', 'Glametrix.otf')
image = renderText("TTF fonts are cool!", fontpath,
                   color, 64, renderer)

if image is None:
    exit(1)

# Getting the window size.
SCREEN_WIDTH = pointer(c_long(0))
SCREEN_HEIGHT = pointer(c_long(0))
SDL_GetWindowSize(window, SCREEN_WIDTH, SCREEN_HEIGHT)

# Get the texture w/h so we can center it in the screen
iW = pointer(c_long(0))
iH = pointer(c_long(0))
SDL_QueryTexture(image, None, None, iW, iH)
x = SCREEN_WIDTH.contents.value / 2 - iW.contents.value / 2
y = SCREEN_HEIGHT.contents.value / 2 - iH.contents.value / 2

r = 1
event = SDL_Event()
while r:
    if SDL_PollEvent(event):
        if event.type == SDL_QUIT:
            r = 0
        elif event.type == SDL_WINDOWEVENT:
            if event.window.event == SDL_WINDOWEVENT_RESIZED:
                SDL_GetWindowSize(window, SCREEN_WIDTH, SCREEN_HEIGHT)
                x = SCREEN_WIDTH.contents.value / 2 - iW.contents.value / 2
                y = SCREEN_HEIGHT.contents.value / 2 - iH.contents.value / 2
        if r:
            SDL_RenderClear(renderer)
            # We can draw our message as we do any other texture, since it's been
            # rendered to a texture
            renderTexture(image, renderer, x, y)
            SDL_RenderPresent(renderer)

SDL_DestroyTexture(image)
SDL_DestroyRenderer(renderer)
SDL_DestroyWindow(window)
SDL_Quit()
