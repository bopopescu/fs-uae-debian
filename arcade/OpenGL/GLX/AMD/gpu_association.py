'''OpenGL extension AMD.gpu_association

This module customises the behaviour of the 
OpenGL.raw.GLX.AMD.gpu_association to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/AMD/gpu_association.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.GLX import _types
from OpenGL.raw.GLX.AMD.gpu_association import *
from OpenGL.raw.GLX.AMD.gpu_association import _EXTENSION_NAME

def glInitGpuAssociationAMD():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION