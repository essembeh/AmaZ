"""
some utilities
"""
import ast
import itertools

try:
    from ast import unparse
except:
    from astunparse import unparse

from .ast_utils import AsTra


def iter_functions(src_text: str):
    """
    iter over all function names found in given ast
    """
    for f in filter(lambda x: isinstance(x, ast.FunctionDef), ast.parse(src_text).body):
        yield f.name


def tweak_ast(source_code: str):
    """
    alter a given code by altering the AST
    """
    tree = ast.parse(source_code)
    AsTra().visit(tree)
    return unparse(tree)


def xor(data: bytes, key: str):
    """
    simple xor on given byte array using a key
    """
    return bytes(a ^ b for a, b in zip(data, itertools.cycle(key.encode())))


def encode_exec(code: str, encode_fnc: callable, decode_fnc: callable):
    """
    encode python code and returns the exec command to load it
    """
    return f"exec(base64.{decode_fnc.__name__}({encode_fnc(code.encode())}))"
