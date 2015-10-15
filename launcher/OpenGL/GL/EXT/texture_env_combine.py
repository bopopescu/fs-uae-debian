'''OpenGL extension EXT.texture_env_combine

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.texture_env_combine to provide a more 
Python-friendly API

Overview (from the spec)
	
	New texture environment function COMBINE_EXT allows programmable
	texture combiner operations, including:
	
	    REPLACE                 Arg0
	    MODULATE                Arg0 * Arg1
	    ADD                     Arg0 + Arg1
	    ADD_SIGNED_EXT          Arg0 + Arg1 - 0.5
	    INTERPOLATE_EXT         Arg0 * (Arg2) + Arg1 * (1-Arg2)
	
	where Arg0, Arg1 and Arg2 are derived from
	
	    PRIMARY_COLOR_EXT       primary color of incoming fragment
	    TEXTURE                 texture color of corresponding texture unit
	    CONSTANT_EXT            texture environment constant color
	    PREVIOUS_EXT            result of previous texture environment; on
	                            texture unit 0, this maps to PRIMARY_COLOR_EXT
	
	and Arg2 is restricted to the alpha component of the corresponding source.
	
	In addition, the result may be scaled by 1.0, 2.0 or 4.0.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/texture_env_combine.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.EXT.texture_env_combine import *
from OpenGL.raw.GL.EXT.texture_env_combine import _EXTENSION_NAME

def glInitTextureEnvCombineEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION