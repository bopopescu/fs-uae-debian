'''OpenGL extension OES.point_size_array

This module customises the behaviour of the 
OpenGL.raw.GLES1.OES.point_size_array to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/point_size_array.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.OES.point_size_array import *
from OpenGL.raw.GLES1.OES.point_size_array import _EXTENSION_NAME

def glInitPointSizeArrayOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glPointSizePointerOES.pointer size not checked against 'type,stride'
glPointSizePointerOES=wrapper.wrapper(glPointSizePointerOES).setInputArraySize(
    'pointer', None
)
### END AUTOGENERATED SECTION