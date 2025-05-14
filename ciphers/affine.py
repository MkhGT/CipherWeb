#affine cipher
from math import gcd

def clean_text(text):
    return ''.join(filter(str.isalpha, text.upper()))

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def encrypt(text, key):
    # Parsing key, key berformat 'a,b' misalnya '5,8'
    try:
        a, b = map(int, key.split(','))
    except ValueError:
        raise ValueError("Format kunci harus 'a,b' (misal: 5,8)")

    if gcd(a, 26) != 1:
        raise ValueError("'a' harus coprime dengan 26. Contoh nilai yang valid: 3, 5, 7, 11, 15, 17, 19, 21, 23, 25.")

    plaintext = clean_text(text)
    ciphertext = ''
    for char in plaintext:
        x = ord(char) - 65
        y = (a * x + b) % 26
        ciphertext += chr(y + 65)
    return ciphertext

def decrypt(text, key):
    # Parsing key, key berformat 'a,b' misalnya '5,8'
    try:
        a, b = map(int, key.split(','))
    except ValueError:
        raise ValueError("Format kunci harus 'a,b' (misal: 5,8)")

    if gcd(a, 26) != 1:
        raise ValueError("'a' harus coprime dengan 26. Contoh nilai yang valid: 3, 5, 7, 11, 15, 17, 19, 21, 23, 25.")
    
    a_inv = mod_inverse(a, 26)
    ciphertext = clean_text(text)
    plaintext = ''
    for char in ciphertext:
        y = ord(char) - 65
        x = (a_inv * (y - b)) % 26
        plaintext += chr(x + 65)
    return plaintext
