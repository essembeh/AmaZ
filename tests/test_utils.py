import codecs

from amaz import utils

KEY = "foobar"
TEXT = "Hello World!"


def test_func():
    data = TEXT.encode()
    assert len(TEXT) == len(data)
    xor_data = utils.xor(data, KEY)
    assert len(data) == len(xor_data)
    data2 = utils.xor(xor_data, KEY)
    assert data2 == data
    text2 = data2.decode()
    assert text2 == TEXT


def test_ast():
    code = """
MY_CONST = 'hello'

def foo():
    mystring = 'foobar'
"""
    code2 = utils.tweak_ast(code)
    code3 = utils.tweak_ast(code2)
    for orig, rot in (
        ("MY_CONST", "ZL_PBAFG"),
        ("hello", "uryyb"),
        ("mystring", "zlfgevat"),
        ("foobar", "sbbone"),
    ):
        assert orig == codecs.decode(rot, "rot13")
        assert orig not in code2
        assert orig in code3
        assert rot in code2
        assert rot not in code3
