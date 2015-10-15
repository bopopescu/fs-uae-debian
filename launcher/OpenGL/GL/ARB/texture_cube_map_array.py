'''OpenGL extension ARB.texture_cube_map_array

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.texture_cube_map_array to provide a more 
Python-friendly API

Overview (from the spec)
	
	The GL_EXT_texture_array extension, and subsequently OpenGL 3.0 have
	introduced the concept of one- and two-dimensional array textures.
	An array texture is an ordered set of images with the same size and
	format. Each image in an array texture has a unique level. This
	extension expands texture array support to include cube map
	textures.
	
	A cube map array texture is a 2-dimensional array texture that may
	contain many cube map layers. Each cube map layer is a unique cube
	map image set. Images in a cube map array have the same size and
	format limitations as one- and two-dimensional array textures. A
	cube map array texture is specified using TexImage3D in a similar
	manner to two-dimensional arrays. Cube map array textures can be
	bound to a render targets of a frame buffer object as
	two-dimensional arrays are using FramebufferTextureLayer.
	
	When accessed by a programmable shader, a cube map array texture
	acts as a single unit. The "s", "t", "r" texture coordinates are
	treated as a regular cube map texture fetch. The "q" texture is
	treated as an unnormalized floating-point value identifying the
	layer of the cube map array texture. Cube map array texture lookups
	do not filter between layers.
	
	This extension does not provide for the use of cube map array
	textures with fixed-function fragment processing.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/texture_cube_map_array.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.ARB.texture_cube_map_array import *
from OpenGL.raw.GL.ARB.texture_cube_map_array import _EXTENSION_NAME

def glInitTextureCubeMapArrayARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION