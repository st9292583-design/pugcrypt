from ciphers import substitute, vigenere, polybius
from rsa_lab import rsa

def calculate(data):
    value = data["text"].strip()
    if not 0 < len(value) <= 1000:
        raise ValueError("Довжина повідомлення має бути від 1 до 1000 символів.")
    mode, reverse = data["mode"], data["reverse"]
    if mode == "caesar":
        shift = int(data.get("key", ""))
        if not 0 <= shift <= 32:
            raise ValueError("Зсув має бути від 0 до 32.")
        return substitute(value, [shift], reverse)
    if mode == "vigenere":
        return vigenere(value, data.get("key", ""), reverse)
    if mode == "polybius":
        return polybius(value, reverse)
    if mode == "rsa":
        return rsa(value, reverse)
    raise ValueError("Оберіть алгоритм.")


