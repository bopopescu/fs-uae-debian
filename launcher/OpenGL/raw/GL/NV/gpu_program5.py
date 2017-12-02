'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_gpu_program5'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NV_gpu_program5',error_checker=_errors._error_checker)
GL_FRAGMENT_PROGRAM_INTERPOLATION_OFFSET_BITS_NV=_C('GL_FRAGMENT_PROGRAM_INTERPOLATION_OFFSET_BITS_NV',0x8E5D)
GL_MAX_FRAGMENT_INTERPOLATION_OFFSET_NV=_C('GL_MAX_FRAGMENT_INTERPOLATION_OFFSET_NV',0x8E5C)
GL_MAX_GEOMETRY_PROGRAM_INVOCATIONS_NV=_C('GL_MAX_GEOMETRY_PROGRAM_INVOCATIONS_NV',0x8E5A)
GL_MAX_PROGRAM_SUBROUTINE_NUM_NV=_C('GL_MAX_PROGRAM_SUBROUTINE_NUM_NV',0x8F45)
GL_MAX_PROGRAM_SUBROUTINE_PARAMETERS_NV=_C('GL_MAX_PROGRAM_SUBROUTINE_PARAMETERS_NV',0x8F44)
GL_MAX_PROGRAM_TEXTURE_GATHER_OFFSET_NV=_C('GL_MAX_PROGRAM_TEXTURE_GATHER_OFFSET_NV',0x8E5F)
GL_MIN_FRAGMENT_INTERPOLATION_OFFSET_NV=_C('GL_MIN_FRAGMENT_INTERPOLATION_OFFSET_NV',0x8E5B)
GL_MIN_PROGRAM_TEXTURE_GATHER_OFFSET_NV=_C('GL_MIN_PROGRAM_TEXTURE_GATHER_OFFSET_NV',0x8E5E)
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLuintArray)
def glGetProgramSubroutineParameteruivNV(target,index,param):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,arrays.GLuintArray)
def glProgramSubroutineParametersuivNV(target,count,params):pass