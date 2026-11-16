import unittest

from ciphers import NAME, MESSAGE, CIPHER, substitute, vigenere, polybius
from rsa_lab import N, PHI, E, rsa
from app import calculate


class CiphersTest(unittest.TestCase):
    def test_caesar(self):
        output, _ = substitute(NAME, [5])
        self.assertEqual(output, "ЦЧДЄМЦГП УРІПЦДТИХД ЦІХЖМНЄТД")
        self.assertEqual(substitute(output, [5], True)[0], NAME)

    def test_vigenere(self):
        output, _ = vigenere(NAME)
        self.assertEqual(output, "ЕЗСХЩЖПҐ ГВЧҐЕРДШДР ЗЩДУЯВРҐС")
        self.assertEqual(vigenere(output, reverse=True)[0], NAME)

    def test_polybius(self):
        self.assertEqual(polybius("АЯ")[0], "11 63")
        self.assertEqual(polybius(polybius(NAME)[0], True)[0], NAME)
        with self.assertRaises(ValueError):
            polybius("66", True)

    def test_rsa(self):
        self.assertEqual((N, PHI, E), (361708981, 361658412, 240983813))
        self.assertEqual(rsa(MESSAGE)[0], "187880492 | 79821865")
        self.assertEqual(rsa("187880492 79821865", True)[0], "28978781 | 35")
        self.assertEqual(rsa(CIPHER, True)[0], "295808259")

    def test_invalid_shift(self):
        with self.assertRaises(ValueError):
            calculate(dict(mode="caesar", text="А", key="33", reverse=False))
