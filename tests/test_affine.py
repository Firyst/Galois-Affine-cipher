import pytest

import affine
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


def test_bin_blocks_1():
    message = "hello"
    for i in range(2, 20):
        coded = affine.string_to_binary_blocks(message, i)
        # print(coded)
        assert affine.binary_blocks_to_integers(coded, i).replace(" ", "") == message


def test_bin_blocks_2():
    message = "привет!"
    for i in range(2, 20):
        coded = affine.string_to_binary_blocks(message, i)
        # print(coded)
        assert affine.binary_blocks_to_integers(coded, i).replace(" ", "") == message


def test_b_1():
    field = GaloisField(2, 5)
    field.set_irreducible([1, 0, 1, 1, 1, 1])

    a = field.elements[2]
    b = field.elements[4]

    text = "ababefagabdh"

    encrypted = encryptB(field, text, a, b)
    assert text == decryptB(field, encrypted, a, b).replace(" ", '')
