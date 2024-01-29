from galois import GaloisField, GaloisFieldElement


def string_to_binary_blocks(input_string, block_size):
    # Преобразование строки в двоичный формат с использованием кодировки UTF-8
    binary_string = ''.join(format(ord(char), '016b') for char in input_string)

    # Добавление пробелов в конец строки, если необходимо
    while len(binary_string) % block_size != 0:
        # Добавление пробела в конец строки и его преобразование в двоичный формат
        binary_string += format(ord(' '), '016b')

    # Разбиение двоичной последовательности на блоки
    blocks = [binary_string[i:i + block_size] for i in range(0, len(binary_string), block_size)]

    # Преобразование каждого блока в целое число
    blocks_as_integers = [int(block, 2) for block in blocks]

    return blocks_as_integers


def binary_blocks_to_integers(blocks, block_size):
    # Преобразование списка целых чисел в двоичную строку с заданной длиной блока
    binary_string = ''.join(format(block, '0' + str(block_size) + 'b') for block in blocks)

    # Разбиение двоичной строки на блоки по 8 бит
    byte_blocks = [binary_string[i:i + 16] for i in range(0, len(binary_string), 16)]

    # Преобразование двоичных блоков в байты и декодирование их в строку UTF-8
    try:
        string = ''.join(chr(int(byte_block, 2)) for byte_block in byte_blocks if len(byte_block) == 16)
        return string
    except ValueError:
        # В случае ошибки декодирования, возвращаем пустую строку или сообщение об ошибке
        return "Ошибка декодирования. Проверьте входные данные."


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


def encryptB(field: GaloisField, input_text: str, alpha: GaloisFieldElement, beta: GaloisFieldElement):
    encoded = string_to_binary_blocks(input_text, field.n)

    ciphertext = ""

    # assert reflect_back(field.elements[reflect(alphabet[3])]) == alphabet[4]

    for s in encoded:
        # print(f"E index of {s}: {reflect(s)}")
        encrypted = field.get_mult(s - 1, alpha) + beta
        print(f"E encrypted {s}", encrypted)
        ciphertext += (bin(field.get_element(encrypted) + 1)[2:]).rjust(field.n, '0')
        # print(f"E back {s} : {reflect_back(encrypted)}")

    return ciphertext


def decryptB(field: GaloisField, ciphertext: str, alpha: GaloisFieldElement, beta: GaloisFieldElement):
    text = []
    for i in range(0, len(ciphertext), field.n):
        block = ciphertext[i:i+field.n]

        decrypted = field.get_mult(field.get_inv(alpha), (field.get(int(block, 2) - 1) - beta))
        # print("dec", field.get_inv(alpha), decrypted, field.elements[reflect(s)])
        # print(f"D back {s} : {reflect_back(decrypted)}")
        text.append(1 + field.get_element(decrypted))

    return binary_blocks_to_integers(text, field.n)
