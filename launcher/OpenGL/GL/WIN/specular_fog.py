'''OpenGL extension WIN.specular_fog

This module customises the behaviour of the 
OpenGL.raw.GL.WIN.specular_fog to provide a more 
Python-friendly API

Overview (from the spec)
	
	Specularly lit textures enhance the realism of a scene greatly.
	Using the current OpenGL lighting model, one cannot obtain specularly lit 
	textures. This is because in the current OpenGL lighting model lighting
	is done ahead of texturing and texture-functions such as modulate are 
	inadequate for such a simulation. What needs to be addressed is that, 
	somehow an additional interpolant (specular color of that material) needs 
	to be propagated till that stage of the pipeline where texture-mapping is
	performed. This interpolant is then added on to the fragment's color
	resulting from the texturing process before proceeding with the rest of 
	the pipeline.
	
	This can be addressed very easily in software, but hardware
	is not so malleable. Currently most hardware does not support such a
	
	lighting model. However, some current hardware does support fogging,
	which takes place in the pipeline after texturing. This hardware 
	assumes that the fog blend factor f is computed per-vertex and
	interpolates the value across the primitive. The WIN_specular_fog
	extension enables the use of such existing fog circuitry to obtain 
	specularly lit textures without much performance degradation. 
	
	To use it the programmer simply enables the extension with a call to
	Enable with the appropriate enumerant and sets the fog color to the 
	desired specular color.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/WIN/specular_fog.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.WIN.specular_fog import *
from OpenGL.raw.GL.WIN.specular_fog import _EXTENSION_NAME

def glInitSpecularFogWIN():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION