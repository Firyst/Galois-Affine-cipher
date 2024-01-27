from galois import *
import pytest

def test_prime_1():
    assert is_prime(2)

def test_prime_2():
    assert is_prime(3)

def test_prime_3():
    assert is_prime(13)

def test_prime_4():
    assert is_prime(43)

def test_prime_5():
    assert not is_prime(36)

def test_fact_1():
    assert factorize(12) == [2, 3, 4, 6]

def test_simple_mult_1():
    empty_poly = GaloisFieldElement([], 999, [])
    assert empty_poly.simple_mult([1, 0], [1], 5) == [1, 0]


def test_simple_mult_2():
    empty_poly = GaloisFieldElement([], 999, [])
    assert empty_poly.simple_mult([1, 1, 1, 1, 1, 1, 0], [1], 5) == [1, 1, 1, 1, 1, 1, 0]


def test_simple_mult_3():
    empty_poly = GaloisFieldElement([], 999, [])
    assert empty_poly.simple_mult([1, 0], [1, 0], 5) == [1, 0, 0]


def test_simple_mult_4():
    empty_poly = GaloisFieldElement([], 999, [])
    assert empty_poly.simple_mult([1, 0], [1, 1], 5) == [1, 1, 0]


#
# p=3, n=2
#

def test_add_1():
    p1 = GaloisFieldElement([1, 0], 3, [2, -2, 1])
    p2 = GaloisFieldElement([1, 0], 3, [2, -2, 1])
    assert (p1 + p2).coefficients == [2, 0]


def test_add_2():
    p1 = GaloisFieldElement([2, 0], 3, [2, -2, 1])
    p2 = GaloisFieldElement([1, 0], 3, [2, -2, 1])
    assert (p1 + p2).coefficients == [0]


def test_mul_1():
    p1 = GaloisFieldElement([2], 3, [2, -2, 1])
    p2 = GaloisFieldElement([1], 3, [2, -2, 1])
    assert (p1 * p2).coefficients == [2]


def test_mul_2():
    p1 = GaloisFieldElement([2], 3, [2, -2, 1])
    p2 = GaloisFieldElement([1, 0], 3, [2, -2, 1])
    assert (p1 * p2).coefficients == [2, 0]


def test_mul_3():
    p1 = GaloisFieldElement([1, 0], 3, [2, -2, 1])
    p2 = GaloisFieldElement([1, 0], 3, [2, -2, 1])
    assert (p1 * p2).coefficients == [1, 1]


def test_mul_4():
    p1 = GaloisFieldElement([1, 1], 3, [2, -2, 1])
    p2 = GaloisFieldElement([1, 1], 3, [2, -2, 1])
    assert (p1 * p2).coefficients == [2]


def test_mul_5():
    p1 = GaloisFieldElement([2, 0], 3, [2, -2, 1])
    p2 = GaloisFieldElement([2, 0], 3, [2, -2, 1])
    assert (p1 * p2).coefficients == [1, 1]


def test_mul_6():
    p1 = GaloisFieldElement([2, 2], 3, [2, -2, 1])
    p2 = GaloisFieldElement([2, 2], 3, [2, -2, 1])
    assert (p1 * p2).coefficients == [2]


def test_mul_7():
    p1 = GaloisFieldElement([2, 2], 3, [2, -2, 1])
    p2 = GaloisFieldElement([1], 3, [2, -2, 1])
    assert (p1 * p2).coefficients == [2, 2]


def test_mul_8():
    p1 = GaloisFieldElement([1, 1], 3, [2, -2, 1])
    p2 = GaloisFieldElement([2, 2], 3, [2, -2, 1])
    assert (p1 * p2).coefficients == [1]

#
# p = 2, n = 3
#


def test_mul_9():
    p1 = GaloisFieldElement([1], 2, [1, 0, 1, 1])
    p2 = GaloisFieldElement([1], 2, [1, 0, 1, 1])
    assert (p1 * p2).coefficients == [1]


def test_mul_10():
    p1 = GaloisFieldElement([1, 0], 2, [1, 0, 1, 1])
    p2 = GaloisFieldElement([1, 0], 2, [1, 0, 1, 1])
    assert (p1 * p2).coefficients == [1, 0, 0]


def test_mul_11():
    p1 = GaloisFieldElement([1, 0, 0], 2, [1, 0, 1, 1])
    p2 = GaloisFieldElement([1, 0, 0], 2, [1, 0, 1, 1])
    assert (p1 * p2).coefficients == [1, 1, 0]


def test_mul_12():
    p1 = GaloisFieldElement([1, 1, 1], 2, [1, 0, 1, 1])
    p2 = GaloisFieldElement([1, 1, 1], 2, [1, 0, 1, 1])
    assert (p1 * p2).coefficients == [1, 1]

#
# тест поля
#


def test_irreducible_1():
    field = GaloisField(3, 2)
    field.set_irreducible([2, -2, 1])

    assert field.ready


def test_irreducible_2():
    field = GaloisField(3, 2)
    with pytest.raises(ArithmeticError):
        field.set_irreducible([2, -2, 0])


def test_irreducible_3():
    field = GaloisField(2, 4)
    with pytest.raises(ArithmeticError):
        field.set_irreducible([1, 0, 1, 0, 1])


def test_mul_table_1():
    field = GaloisField(2, 3)
    field.set_irreducible([1, 0, 1, 1])

    assert len(field.cached_mul) == 28


def test_powers_0():
    field = GaloisField(2, 4)
    field.set_irreducible([1, 0, 0, 1, 1])
    assert field.get_power([1]) == 1

def test_powers_1():
    field = GaloisField(2, 4)
    field.set_irreducible([1, 0, 0, 1, 1])
    assert field.get_power([1, 0]) == 15
    assert field.get_power([1, 1, 1]) == 3
    assert field.get_power([1, 1, 1, 1]) == 5