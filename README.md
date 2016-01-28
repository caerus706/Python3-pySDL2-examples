## pysdl2-text-example

### Python 3.5 examples of pySDL2

pySDL2 favors python 2 at the moment, which makes it much harder to get some things working in Python 3.

Nothing worked until I figured out how it was expecting the calls.

#### Changes to get SDL2_ttf working in Python 3

* The calls to TTF_* expect to be encoded in byte format
* You need to either enclose a string in `b'text to send'` or format it to byte format like this `str.encode(textVariable)`
 

#### Windows Installation

1. Install pySDL2 with `pip install pySDL2`
2. Download SDL2.dll from https://www.libsdl.org/download-2.0.php
3. Download from SDL2_ttf from https://www.libsdl.org/projects/SDL_ttf/
4. Place the dll's either in your project folder or your system folder.
   For example C:\Windows\SysWOW64\
5. setup environment variable PYSDL2_DLL_PATH to whichever folder you set the sdl dll in. (If you don't want to constantly set your environment variable.) This may require a restart to work.
6. lesson3 requires [SDL2_Image] (https://www.libsdl.org/projects/SDL_image/)

#### Testing sdl2 import

you can test your path in ipython or the python shell with:

```python
import os
os.getenviron("SDL2")
```

if correct it will return the folder where it finds the dll.

If you don't want to setup PYSDL2_DLL_PATH before runtime you can also do this
```python
import os
os.environ['PYSDL2_DLL_PATH'] = 'C:\\path\\to\\project\\'

from sdl2 import *
```

##### Note: if you're running 64-bit python and you put the 32-bit sdl2 in system32 it will find it there by default, but the program won't run, (This is only if you don't properly set PYSDL2_DLL_PATH

##### examples
text.py is based on the one at [egDev] (https://egdev.wordpress.com/2014/03/14/python-sdl2-ttf-test/)
SDL 2.0 Lessons based on [Twinklebear] (https://github.com/Twinklebear/TwinklebearDev-Lessons)
