def clean_text(text):
    return ''.join(filter(str.isalpha, text)).upper()

def format_output(text, format_type):
    if format_type == 'no_space':
        return text
    elif format_type == 'group_5':
        return ' '.join(text[i:i+5] for i in range(0, len(text), 5))
    return text

def encrypt(plaintext, key, format_type='no_space'):
    plaintext = clean_text(plaintext)
    key = clean_text(key)
    ciphertext = ''
    for i, char in enumerate(plaintext):
        shift = ord(key[i % len(key)]) - ord('A')
        encrypted = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        ciphertext += encrypted
    return format_output(ciphertext, format_type)

def decrypt(ciphertext, key):
    ciphertext = clean_text(ciphertext)
    key = clean_text(key)
    plaintext = ''
    for i, char in enumerate(ciphertext):
        shift = ord(key[i % len(key)]) - ord('A')
        decrypted = chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))
        plaintext += decrypted
    return plaintext
