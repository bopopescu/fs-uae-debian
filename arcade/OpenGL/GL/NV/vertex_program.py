'''OpenGL extension NV.vertex_program

This module customises the behaviour of the 
OpenGL.raw.GL.NV.vertex_program to provide a more 
Python-friendly API

Overview (from the spec)
	
	Unextended OpenGL mandates a certain set of configurable per-vertex
	computations defining vertex transformation, texture coordinate
	generation and transformation, and lighting.  Several extensions
	have added further per-vertex computations to OpenGL.  For example,
	extensions have defined new texture coordinate generation modes
	(ARB_texture_cube_map, NV_texgen_reflection, NV_texgen_emboss), new
	vertex transformation modes (EXT_vertex_weighting), new lighting modes
	(OpenGL 1.2's separate specular and rescale normal functionality),
	several modes for fog distance generation (NV_fog_distance), and
	eye-distance point size attenuation (EXT_point_parameters).
	
	Each such extension adds a small set of relatively inflexible
	per-vertex computations.
	
	This inflexibility is in contrast to the typical flexibility provided
	by the underlying programmable floating point engines (whether
	micro-coded vertex engines, DSPs, or CPUs) that are traditionally used
	to implement OpenGL's per-vertex computations.  The purpose of this
	extension is to expose to the OpenGL application writer a significant
	degree of per-vertex programmability for computing vertex parameters.
	
	For the purposes of discussing this extension, a vertex program is
	a sequence of floating-point 4-component vector operations that
	determines how a set of program parameters (defined outside of
	OpenGL's begin/end pair) and an input set of per-vertex parameters
	are transformed to a set of per-vertex output parameters.
	
	The per-vertex computations for standard OpenGL given a particular
	set of lighting and texture coordinate generation modes (along with
	any state for extensions defining per-vertex computations) is, in
	essence, a vertex program.  However, the sequence of operations is
	defined implicitly by the current OpenGL state settings rather than
	defined explicitly as a sequence of instructions.
	
	This extension provides an explicit mechanism for defining vertex
	program instruction sequences for application-defined vertex programs.
	In order to define such vertex programs, this extension defines
	a vertex programming model including a floating-point 4-component
	vector instruction set and a relatively large set of floating-point
	4-component registers.
	
	The extension's vertex programming model is designed for efficient
	hardware implementation and to support a wide variety of vertex
	programs.  By design, the entire set of existing vertex programs
	defined by existing OpenGL per-vertex computation extensions can be
	implemented using the extension's vertex programming model.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/vertex_program.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.NV.vertex_program import *
from OpenGL.raw.GL.NV.vertex_program import _EXTENSION_NAME

def glInitVertexProgramNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION