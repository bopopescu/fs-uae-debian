'''OpenGL extension SGIX.list_priority

This module customises the behaviour of the 
OpenGL.raw.GL.SGIX.list_priority to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides a mechanism for specifying the relative
	importance of display lists.  This information can be used by
	an OpenGL implementation to guide the placement of display
	list data in a storage hierarchy.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SGIX/list_priority.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.SGIX.list_priority import *
from OpenGL.raw.GL.SGIX.list_priority import _EXTENSION_NAME

def glInitListPrioritySGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION