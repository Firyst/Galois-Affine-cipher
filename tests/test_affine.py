import pytest
from affine import *


def test_a_0():
    field = GaloisField(2, 3)
    field.set_irreducible([1, 0, 1, 1])

    a = field.elements[1]
    b = field.elements[0]

    abc = "abcdefgh"
    for text in abc:
        encrypted = encryptA(field, abc, text, a, b)
        print(f"enc for {text}:", encrypted)
        assert text == decryptA(field, abc, encrypted, a, b)


def test_a_1():
    field = GaloisField(2, 3)
    field.set_irreducible([1, 0, 1, 1])

    a = field.elements[2]
    b = field.elements[4]

    abc = "abcdefgh"
    text = "ababefagabdh"

    encrypted = encryptA(field, abc, text, a, b)
    assert text == decryptA(field, abc, encrypted, a, b)
