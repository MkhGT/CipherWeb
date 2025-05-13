# autokey_vigenere.py
def clean_text(text):
    return ''.join(filter(str.isalpha, text.upper()))

def generate_key_autokey(plaintext, key):
    plaintext = clean_text(plaintext)
    key = clean_text(key)
    key_stream = key + plaintext
    return key_stream[:len(plaintext)]

def encrypt(text, key):
    plaintext = clean_text(text)
    key_stream = generate_key_autokey(plaintext, key)
    ciphertext = ''
    for p, k in zip(plaintext, key_stream):
        c = chr(((ord(p) - 65 + (ord(k) - 65)) % 26) + 65)
        ciphertext += c
    return ciphertext

def decrypt(text, key):
    ciphertext = clean_text(text)
    key = clean_text(key)
    plaintext = ''
    key_stream = key
    for i in range(len(ciphertext)):
        k = key_stream[i]
        c = ciphertext[i]
        p = chr(((ord(c) - 65 - (ord(k) - 65)) % 26) + 65)
        plaintext += p
        key_stream += p
    return plaintext