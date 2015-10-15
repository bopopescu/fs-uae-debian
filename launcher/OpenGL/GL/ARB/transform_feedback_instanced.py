'''OpenGL extension ARB.transform_feedback_instanced

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.transform_feedback_instanced to provide a more 
Python-friendly API

Overview (from the spec)
	
	Multiple instances of geometry may be specified to the GL by calling
	functions such as DrawArraysInstanced and DrawElementsInstanced. Further,
	the results of a transform feedback operation may be returned to the GL
	by calling DrawTransformFeedback, or DrawTransformFeedbackStream. However,
	it is not presently possible to draw multiple instances of data
	transform feedback without using a query and the resulting round trip from
	server to client.
	
	This extension adds functionality to draw multiple instances of the result
	of a transform feedback operation.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/transform_feedback_instanced.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.ARB.transform_feedback_instanced import *
from OpenGL.raw.GL.ARB.transform_feedback_instanced import _EXTENSION_NAME

def glInitTransformFeedbackInstancedARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION