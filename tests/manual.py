from affine import *

def f():
    field = GaloisField(2, 3)
    field.set_irreducible([1, 0, 1, 1])

    a = field.elements[1]
    b = field.elements[0]

    abc = "abcdefgh"
    encrypted = encryptA(field, abc, abc, a, b)
    print(encrypted)

f()