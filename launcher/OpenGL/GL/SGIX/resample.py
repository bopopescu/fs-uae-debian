'''OpenGL extension SGIX.resample

This module customises the behaviour of the 
OpenGL.raw.GL.SGIX.resample to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension enhances the unpacking resampling capabilities
	of the SGIX_subsample extension.
	
	When pixel data is received from the client and an unpacking
	upsampling mode other than PIXEL_SUBSAMPLE_RATE_4444_SGIX is
	specified, the upsampling is performed via one of two methods:
	RESAMPLE_REPLICATE_SGIX, RESAMPLE_ZERO_FILL_SGIX.
	Replicate and zero fill are provided to
	give the application greatest performance and control over the
	filtering process.
	
	However, when pixel data is read back to the client and a
	packing downsampling mode other than PIXEL_SUBSAMPLE_RATE_4444_SGIX
	is specified, downsampling is
	performed via simple component decimation (point sampling). That is,
	only the RESAMPLE_DECIMATE_SGIX is valid.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SGIX/resample.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.SGIX.resample import *
from OpenGL.raw.GL.SGIX.resample import _EXTENSION_NAME

def glInitResampleSGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION