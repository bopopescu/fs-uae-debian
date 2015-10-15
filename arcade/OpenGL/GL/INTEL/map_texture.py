'''OpenGL extension INTEL.map_texture

This module customises the behaviour of the 
OpenGL.raw.GL.INTEL.map_texture to provide a more 
Python-friendly API

Overview (from the spec)
	Systems with integrated GPUs can share the same physical memory between CPU
	and GPU. This feature, if exposed by API, can bring significant performance
	benefits for graphics applications by reducing the complexity of
	uploading/accessing texture contents. This extension enables CPU direct
	access to the GPU memory holding textures.
	
	The problem with texture memory directly exposed to clients is that
	textures are often 'tiled'. Texels are kept in specific layout to improve
	locality of reference and thus performance of texturing. This 'tiling'
	is specific to particular hardware and would be thus difficult to use.
	
	This extension allows to create textures with 'linear' layout which allows
	for simplified access on user side (potentially sacrificing some
	performance during texture sampling).

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/INTEL/map_texture.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.INTEL.map_texture import *
from OpenGL.raw.GL.INTEL.map_texture import _EXTENSION_NAME

def glInitMapTextureINTEL():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION