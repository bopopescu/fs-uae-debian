'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_internalformat_query'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_internalformat_query',error_checker=_errors._error_checker)
GL_NUM_SAMPLE_COUNTS=_C('GL_NUM_SAMPLE_COUNTS',0x9380)
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLenum,_cs.GLsizei,arrays.GLintArray)
def glGetInternalformativ(target,internalformat,pname,bufSize,params):pass