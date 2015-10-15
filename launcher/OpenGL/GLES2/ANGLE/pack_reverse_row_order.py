'''OpenGL extension ANGLE.pack_reverse_row_order

This module customises the behaviour of the 
OpenGL.raw.GLES2.ANGLE.pack_reverse_row_order to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ANGLE/pack_reverse_row_order.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.GLES2 import _types
from OpenGL.raw.GLES2.ANGLE.pack_reverse_row_order import *
from OpenGL.raw.GLES2.ANGLE.pack_reverse_row_order import _EXTENSION_NAME

def glInitPackReverseRowOrderANGLE():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION