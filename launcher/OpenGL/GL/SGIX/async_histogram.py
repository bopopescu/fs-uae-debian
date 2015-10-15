'''OpenGL extension SGIX.async_histogram

This module customises the behaviour of the 
OpenGL.raw.GL.SGIX.async_histogram to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension introduces a new asynchronous mode for histogram
	and minmax readbacks.  It allows programs to get the contents of a
	histogram or minmax table without blocking and to continue issuing
	graphics commands during the readback.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SGIX/async_histogram.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.SGIX.async_histogram import *
from OpenGL.raw.GL.SGIX.async_histogram import _EXTENSION_NAME

def glInitAsyncHistogramSGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION