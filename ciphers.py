"""Навчальні перетворення для української абетки."""

ALPHABET = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
NAME = "СТАВІСЮК ОЛЕКСАНДРА СЕРГІЇВНА"
KEY = "МОПС"
P, Q, D = 8623, 41947, 319838333
MESSAGE, CIPHER = "2897878135", "20979746"


def substitute(text, shifts, reverse=False):
    result, steps = [], []
    for letter in text.upper():
        if letter.isspace():
            result.append(letter)
            continue
        if letter not in ALPHABET:
            raise ValueError("Введіть українські літери та пробіли.")
        index = ALPHABET.index(letter)
        shift = shifts[len(steps) % len(shifts)] * (-1 if reverse else 1)
        target = (index + shift) % len(ALPHABET)
        result.append(ALPHABET[target])
        steps.append(f"{letter}: ({index} + ({shift})) mod 33 = {target} → {ALPHABET[target]}")
    return "".join(result), steps


def vigenere(text, key=KEY, reverse=False):
    key = key.strip().upper()
    if not key or any(letter not in ALPHABET for letter in key):
        raise ValueError("Ключ має містити українські літери.")
    return substitute(text, [ALPHABET.index(letter) + 2 for letter in key], reverse)


def polybius(text, reverse=False):
    if reverse:
        result, steps = [], []
        for pair in text.split():
            if pair == "/":
                result.append(" ")
                continue
            if len(pair) != 2 or any(digit not in "123456" for digit in pair):
                raise ValueError("Введіть пари цифр 1–6, між словами поставте /.")
            index = (int(pair[0]) - 1) * 6 + int(pair[1]) - 1
            if index >= len(ALPHABET):
                raise ValueError(f"Клітинка {pair} порожня.")
            result.append(ALPHABET[index])
            steps.append(f"{pair} → {ALPHABET[index]}")
        return "".join(result), steps
    result, steps = [], []
    for letter in text.upper():
        if letter.isspace():
            result.append("/")
            continue
        if letter not in ALPHABET:
            raise ValueError("Введіть українські літери та пробіли.")
        row, col = divmod(ALPHABET.index(letter), 6)
        pair = f"{row + 1}{col + 1}"
        result.append(pair)
        steps.append(f"{letter} → рядок {row + 1}, стовпець {col + 1} → {pair}")
    return " ".join(result), steps
