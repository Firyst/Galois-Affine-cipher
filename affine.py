from galois import GaloisField, GaloisFieldElement


def encryptA(field: GaloisField, alphabet: str, input_text: str, alpha: GaloisFieldElement, beta: GaloisFieldElement):
    if (len(field.elements) + 1) != len(alphabet):
        raise ArithmeticError("Неверная длина алфавита")

    def reflect(symbol: str) -> int:
        return alphabet.index(symbol) - 1

    def reflect_back(symbol: GaloisFieldElement) -> str:
        return alphabet[1 + field.get_element(symbol)]

    ciphertext = ""

    # assert reflect_back(field.elements[reflect(alphabet[3])]) == alphabet[4]

    for s in input_text:
        print(f"E index of {s}: {reflect(s)}")
        encrypted = field.get_mult(reflect(s), alpha) + beta
        print(f"E encrypted {s}", encrypted)
        ciphertext += reflect_back(encrypted)
        print(f"E back {s} : {reflect_back(encrypted)}")

    return ciphertext


def decryptA(field: GaloisField, alphabet: str, ciphertext: str, alpha: GaloisFieldElement, beta: GaloisFieldElement):
    if (len(field.elements) + 1) != len(alphabet):
        raise ArithmeticError("Неверная длина алфавита")

    def reflect(symbol: str) -> int:
        return alphabet.index(symbol) - 1

    def reflect_back(symbol: GaloisFieldElement) -> str:
        return alphabet[1 + field.get_element(symbol)]

    text = ""

    for s in ciphertext:
        print(f"D index of {s}: {reflect(s)}")
        decrypted = field.get_mult(field.get_inv(alpha), (field.get(reflect(s)) - beta))
        print("dec", field.get_inv(alpha), decrypted, field.elements[reflect(s)])
        print(f"D back {s} : {reflect_back(decrypted)}")
        text += reflect_back(decrypted)

    return text
