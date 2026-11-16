"""Блокові операції RSA для фіксованого варіанта 28."""
from ciphers import P, Q, D

N = P * Q
PHI = (P - 1) * (Q - 1)
E = pow(D, -1, PHI)
WIDTH = len(str(N)) - 1


def power_trace(base, exponent):
    current, result = base, 1
    trace = []
    while exponent:
        bit = exponent % 2
        if bit:
            result = result * current % N
        trace.append(f"Біт {bit} · основа {current} · накопичено {result}")
        current = current * current % N
        exponent //= 2
    return result, trace


def rsa(text, reverse=False):
    parts = text.split()
    if not parts or any(not part.isascii() or not part.isdecimal() for part in parts):
        raise ValueError("Введіть десяткове число або блоки через пробіл.")
    if not reverse and len(parts) != 1:
        raise ValueError("Для шифрування введіть одне число.")
    if not reverse:
        message = parts[0]
        parts = [message[i:i + WIDTH] for i in range(0, len(message), WIDTH)]
    if any(len(part) > len(str(N)) or int(part) >= N for part in parts):
        raise ValueError(f"Кожний блок має бути меншим за {N}.")
    outputs, steps = [], [f"N = {N} · φ(N) = {PHI} · e = {E} · d = {D}"]
    for part in parts:
        result, trace = power_trace(int(part), D if reverse else E)
        outputs.append(str(result))
        steps.extend([f"Блок {part} → {result}", *trace])
    return " | ".join(outputs), steps
