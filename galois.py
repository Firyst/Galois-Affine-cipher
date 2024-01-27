from itertools import product


def is_prime(n):
    """
    Простая проверка на простоту
    :param n: число
    :return: True/False
    """
    if n < 4:
        return True
    for i in range(2, int(n ** 0.5) + 1):
        if i ** 2 == n:
            return False
    return True

def factorize(n):
    """
    Наивная полная факторизация.
    :param n: число
    :return: list, без 1 и n
    """

    result = []
    for p in range(2, n):
        if n % p == 0:
            result.append(p)
    return result

class GaloisFieldElement:
    def __init__(self, coefficients, p, irreducible):
        """
        Инициализация элемента поля Галуа.
        coefficients: коэффициенты многочлена, представляющего элемент поля.
        p: простое число, характеристика поля Галуа.
        irreducible: неприводимый многочлен, по модулю которого производятся операции.
        """
        self.coefficients = [c % p for c in coefficients]  # Приведение коэффициентов по модулю p
        self.p = p
        self.irreducible = irreducible

    def __eq__(self, other):
        return self.p == other.p and self.coefficients == other.coefficients
    def __add__(self, other):
        """
        Сложение многочленов в поле Галуа
        :param other: второй многочлен
        :return: многочлен после сложения
        """
        max_len = max(len(self.coefficients), len(other.coefficients))
        sum_coeffs = [0] * max_len
        for i in range(max_len):
            a = self.coefficients[i] if i < len(self.coefficients) else 0
            b = other.coefficients[i] if i < len(other.coefficients) else 0
            sum_coeffs[i] = (a + b) % self.p

        while len(sum_coeffs) > 1 and sum_coeffs[0] == 0:
            sum_coeffs = sum_coeffs[1:]
        return GaloisFieldElement(sum_coeffs, self.p, self.irreducible)

    @staticmethod
    def simple_mult(coefs1, coefs2, p):
        """
        Простое умножение коэффициентов
        :param coefs1: коэффициенты первого многочлена
        :param coefs2: коэффициенты второго многочлена
        :param p: модуль, по которому брать коэффициенты
        :return: коэффициенты многочлена, полученного в результате умножения
        """
        prod_coeffs = [0] * (len(coefs1) + len(coefs2) - 1)
        for i in range(len(coefs1)):
            for j in range(len(coefs2)):
                prod_coeffs[i + j] += coefs1[i] * coefs2[j]
                prod_coeffs[i + j] %= p

        # убрать страшие нулевые коэффициенты (понизить степень)
        while prod_coeffs[0] == 0:
            prod_coeffs = prod_coeffs[1:]

        return prod_coeffs

    def __mul__(self, other):
        """
        Умножение многочленов в поле Галуа
        :param other: второй многочлен
        :return: резульат умножения
        """
        def reduce_pow(poly):
            """
            Наивное понижение старшей степени многочлена (как минимум на 1)
            :param poly: многочлен GaloisFieldElement
            :return: многочлен, с пониженной степенью
            """
            start_pow = len(poly.coefficients)  # начальная степень МЧ
            irr_pow = len(poly.irreducible)  # степень неприводимого МЧ

            # ищем старшую степень частного, чтобы найти остаток
            irr_mul = self.simple_mult(poly.irreducible, ([1] + [0] * (start_pow - irr_pow - 1)), self.p)

            irr = GaloisFieldElement(irr_mul, self.p, None)

            new_poly = poly + irr

            # прибавляем до тех пор, пока не уйдет старшая степень
            while len(new_poly.coefficients) >= start_pow:
                new_poly = new_poly + irr

            return new_poly

        # выполняем простое умнножение
        prod_coeffs = self.simple_mult(self.coefficients, other.coefficients, self.p)
        # print(prod_coeffs)
        m_poly = GaloisFieldElement(prod_coeffs, self.p, self.irreducible)

        # понижаем все старшие степени, до тех пор, пока степень многочлена не понизится до n-1
        while len(m_poly.coefficients) >= len(self.irreducible):
            m_poly = reduce_pow(m_poly)

        return m_poly

    def inverse_mod(self, a, mod):
        # Расширенный алгоритм Евклида для нахождения обратного элемента
        if a == 0:
            raise ValueError("Обратный элемент не существует")

        lm, hm = 1, 0
        low, high = a % mod, mod
        while low > 1:
            ratio = high // low
            nm, new = hm - lm * ratio, high - low * ratio
            hm, lm = lm, nm
            high, low = low, new

        return lm % mod

    def __str__(self):
        return ' + '.join(f'{coeff}x^{i}' if i > 0 else str(coeff)
                          for i, coeff in enumerate(reversed(self.coefficients)) if coeff)

    def fancy(self):
        """
        Функция для красивого вывода многочлена с использованием символов степени из UTF-8.
        """

        def superscript(num):
            # Преобразование числа в строку со степенями в UTF-8
            superscript_map = {
                "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
                "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"
            }
            return ''.join(superscript_map.get(digit, '') for digit in str(num))

        terms = []
        for i, coeff in enumerate(reversed(self.coefficients)):
            if coeff != 0:
                if i == 0:
                    term = str(coeff)
                elif i == 1:
                    term = f"{coeff}x" if coeff != 1 else "x"
                else:
                    term = f"{coeff}x{superscript(i)}" if coeff != 1 else f"x{superscript(i)}"
                terms.append(term)
        return ' + '.join(reversed(terms)) if terms else '0'

    def _mod_inverse(self, a):
        # Нахождение обратного элемента к a в поле Галуа
        for i in range(self.p):
            if (a * i) % self.p == 1:
                return i
        return 1  # Если обратного не существует, возвращаем 1 (не должно случиться в правильно настроенном поле Галуа)

    def __repr__(self):
        return f"elem(p={self.p}, n={len(self.irreducible) - 1}): {self.fancy()}"


class GaloisField:
    def __init__(self, p, n, irreducible=None):
        self.p = p
        self.n = n
        self.ready = False

        # элементы поля
        self.elements = []
        self.indexed = {}  # словарь кожффициенты:индекс

        # таблицы сложения и умножения
        self.cached_add = {}
        self.cached_mul = {}

        # задать и проверить неприводимый
        if irreducible is None:
            self.irreducible = list()
        else:
            self.set_irreducible(irreducible)

    def set_irreducible(self, coefficients):
        """
        Задать неприводимый многочлен
        :param coefficients: коэффициенты неприводимого многочлена
        :return: None
        """
        if len(coefficients) != (self.n + 1):
            raise ArithmeticError("Неверная степень неприводимого многочлена (!=n)")

        for possible_x in range(self.p):
            value = 0
            for pow, mul in enumerate(reversed(coefficients)):
                value += (possible_x ** pow) * mul
            if value % self.p == 0:
                raise ArithmeticError("Многочлен не является неприводимым! (имеет корни)")

        self.irreducible = coefficients

        # построить поле
        self.generate_all_elements()

        # убедиться, что заданный МЧ нельзя получить произведением
        self.build_mul_table()

        self.ready = True

    def check_ready(self):
        """
        Проверить, определен ли класс
        """
        if not self.ready:
            raise AssertionError("Не задан неприводимый многочлен!")

    def generate_all_elements(self):
        """
        Найти все элементы поля Галуа, кешировать их индексы
        """
        for power in range(self.n):
            for coefficients in product(range(self.p), repeat=(power + 1)):
                if coefficients[0] != 0:
                    self.elements.append(GaloisFieldElement(list(coefficients), self.p, self.irreducible))

        for i, element in enumerate(self.elements):
            self.indexed[tuple(element.coefficients)] = i

    def build_add_table(self):
        pass

    def build_mul_table(self):
        """
        Строит внутреннюю мультипликативную таблицу (cached_mul)
        :return: None
        """
        for num_a in range(0, len(self.elements)):
            for num_b in  range(0, num_a + 1):
                elem_a = self.elements[num_a]
                elem_b = self.elements[num_b]

                irr_test = GaloisFieldElement.simple_mult(elem_a.coefficients, elem_b.coefficients, self.p)
                if irr_test == self.irreducible:
                    raise ArithmeticError("Многочлен не является неприводимым! (является произведениием элементов поля)")

                self.cached_mul[(num_a, num_b)] = elem_a * elem_b

    def get_element(self, data):
        """
        Проверяет, дан ли индекс элемента, или коэффициенты
        :param data: ввод: число/кортеж/список
        :return: индекс элемента
        """
        if type(data) == int:
            if 0 <= data < len(self.elements):
                return data
            else:
                raise IndexError("Неверный индекс элемента поле Галуа.")

        if type(data) == list:
            data = tuple(data)

        if type(data) == tuple:
            if data in self.indexed:
                return self.indexed[data]
            else:
                raise KeyError("Неверный элемент поле Галуа")

        return None

    def get_power(self, member):
        """
        Найти порядок элемента в заданном поле Галуа
        :param elem: индекс/коэффициенты элемента
        :return: int - порядок
        """
        self.check_ready()
        elem = self.elements[self.get_element(member)]

        # проверка на 1
        if elem.coefficients == [1]:
            return 1

        # начинаем перебор с квадрата
        power = 2
        new_elem = elem * elem
        while new_elem.coefficients != [1]:
            # умножаем, пока не получим 1
            new_elem = new_elem * elem
            power += 1
        return power

    def find_groups(self):
        """
        Найти все циклические подгруппы.
        :return: dict{порядок_элементов:[элементы]}
        """
        powers = {}

        # найти все порядки
        for i in range(len(self.elements)):
            power = self.get_power(i)
            powers[i] = power

        groups = {}
        # построить все группы
        for power in sorted(list(powers.values())):

            if power in groups or power == 1:
                continue
            sub_powers = factorize(power)
            # инициализируем новую группу
            groups[power] = LoopGroup(power)
            # сразу добавляем 1
            groups[power].add_element(self.elements[0])

            # ищем образующие и элементы группы
            for kvp in powers.items():
                if kvp[1] == power:  # образующий
                    groups[power].add_root(self.elements[kvp[0]])
                elif kvp[1] in sub_powers:  # просто элемент
                    groups[power].add_element(self.elements[kvp[0]])
        return groups


class LoopGroup:
    def __init__(self, power):
        self.power = power
        self.elements = []  # все элементы
        self.roots = []  # образующие

    def add_root(self, element: GaloisFieldElement):
        if element not in self.roots:
            self.roots.append(element)
            self.add_element(element)

    def add_element(self, element: GaloisFieldElement):
        if element not in self.elements:
            self.elements.append(element)

    def __repr__(self):
        forming = []
        for a in self.roots:
            forming.append(f"<{a.fancy()}>")
        return f"H{self.power} = {' = '.join(forming)}"

    def __eq__(self, other):
        return self.power == other.power


def generate_unreducible(p, n):
    test_field = GaloisField(p, n)
    for coefficients in product(range(p), repeat=(n)):

        for i0 in range(1, p):
            try:
                test_field.set_irreducible([i0] + list(coefficients))
                print([i0] + list(coefficients))
            except ArithmeticError:
                continue



if __name__ == "__main__":
    p1 = GaloisFieldElement([1, 0, 1], 3, [2, -2, 1])
    p2 = GaloisFieldElement([1, 0], 3, [2, -2, 1])

    # print(p1.fancy(), p2.fancy())

    # print((p1 + p2).fancy())

    # print((p1 * p2).fancy())

    generate_unreducible(3, 2)

    f33 = GaloisField(3, 3)
    f33.set_irreducible([2, -2, 1, 1])

    # f33.generate_all_elements()

    for elem in f33.elements:
        print(elem.fancy())

    # f33.build_mul_table()
    print(f33.cached_mul)

    print(len(f33.cached_mul))
    # print(f33.get_power(f33.get_element_id([1, 0])))
    # print(f33.get_power(f33.get_element_id([1, 1, 1])))
    # print(f33.get_power(f33.get_element_id([1, 1, 1, 1])))
    print(f33.find_groups())
    print(len(f33.elements))