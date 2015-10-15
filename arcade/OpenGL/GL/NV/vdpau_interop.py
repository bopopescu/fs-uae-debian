'''OpenGL extension NV.vdpau_interop

This module customises the behaviour of the 
OpenGL.raw.GL.NV.vdpau_interop to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows VDPAU video and output surfaces to be used
	for texturing and rendering.
	
	This allows the GL to process and display the content of video
	streams decoded using VDPAU.
	
	Alternatively, the GL may modify VDPAU surfaces in-place, and VDPAU
	may then process and/or display those surfaces itself.
	
	This allows the GL to be used to combine application user-interface
	elements with decoded video, implement custom video-processing
	algorithms, etc.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/vdpau_interop.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.NV.vdpau_interop import *
from OpenGL.raw.GL.NV.vdpau_interop import _EXTENSION_NAME

def glInitVdpauInteropNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION