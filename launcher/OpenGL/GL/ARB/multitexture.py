'''OpenGL extension ARB.multitexture

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.multitexture to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/multitexture.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.ARB.multitexture import *
from OpenGL.raw.GL.ARB.multitexture import _EXTENSION_NAME

def glInitMultitextureARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION
for typ,arrayType in (
    ('d',arrays.GLdoubleArray),
    ('f',arrays.GLfloatArray),
    ('i',arrays.GLintArray),
    ('s',arrays.GLshortArray),
):
    for size in (1,2,3,4):
        name = 'glMultiTexCoord%(size)s%(typ)svARB'%globals()
        globals()[name] = arrays.setInputArraySizeType(
            globals()[name],
            size,
            arrayType,
            'v',
        )
        try:
            del size,name
        except NameError as err:
            pass
    try:
        del typ,arrayType
    except NameError as err:
        pass
