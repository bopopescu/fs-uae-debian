'''OpenGL extension EXT.copy_texture

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.copy_texture to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension defines methods to load texture images directly from the
	framebuffer.  Methods are defined for both complete and partial
	replacement of a texture image.  Because it is not possible to define
	an entire 3D texture using a 2D framebuffer image, 3D textures are
	supported only for partial replacement.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/copy_texture.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.EXT.copy_texture import *
from OpenGL.raw.GL.EXT.copy_texture import _EXTENSION_NAME

def glInitCopyTextureEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION