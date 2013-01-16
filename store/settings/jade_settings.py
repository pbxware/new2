# coding=utf-8

# bad patching
from pyjade.compiler import Compiler
Compiler.filters["text"] = lambda x,y: x
