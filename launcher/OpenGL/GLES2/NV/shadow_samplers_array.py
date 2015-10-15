'''OpenGL extension NV.shadow_samplers_array

This module customises the behaviour of the 
OpenGL.raw.GLES2.NV.shadow_samplers_array to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/shadow_samplers_array.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.GLES2 import _types
from OpenGL.raw.GLES2.NV.shadow_samplers_array import *
from OpenGL.raw.GLES2.NV.shadow_samplers_array import _EXTENSION_NAME

def glInitShadowSamplersArrayNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION