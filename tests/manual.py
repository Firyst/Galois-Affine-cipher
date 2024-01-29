from affine import *

def f():
    field = GaloisField(2, 5)
    field.set_irreducible([1, 0, 1, 1, 1, 1])

    a = field.elements[2]
    b = field.elements[4]

    text = "ababefagabdh"

    encrypted = encryptB(field, text, a, b)
    print(encrypted)
    print(decryptB(field, encrypted, a, b))
    assert text == decryptB(field, encrypted, a, b).replace(" ", "")

f()