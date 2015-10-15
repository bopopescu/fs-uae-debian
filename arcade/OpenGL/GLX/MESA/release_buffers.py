'''OpenGL extension MESA.release_buffers

This module customises the behaviour of the 
OpenGL.raw.GLX.MESA.release_buffers to provide a more 
Python-friendly API

Overview (from the spec)
	
	Mesa's implementation of GLX is entirely implemented on the client side.
	Therefore, Mesa cannot immediately detect when an X window or pixmap is
	destroyed in order to free any ancilliary data associated with the window
	or pixmap.
	
	The glxMesaReleaseBuffers() function can be used to explicitly indicate
	when the back color buffer, depth buffer, stencil buffer, and/or accum-
	ulation buffer associated with a drawable can be freed.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/MESA/release_buffers.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.GLX import _types
from OpenGL.raw.GLX.MESA.release_buffers import *
from OpenGL.raw.GLX.MESA.release_buffers import _EXTENSION_NAME

def glInitReleaseBuffersMESA():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION