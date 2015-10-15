'''OpenGL extension KHR.lock_surface2

This module customises the behaviour of the 
OpenGL.raw.EGL.KHR.lock_surface2 to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/KHR/lock_surface2.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.EGL import _types
from OpenGL.raw.EGL.KHR.lock_surface2 import *
from OpenGL.raw.EGL.KHR.lock_surface2 import _EXTENSION_NAME

def glInitLockSurface2KHR():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION