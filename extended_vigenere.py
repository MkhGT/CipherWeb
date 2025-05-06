def encrypt_bytes(data: bytes, key: str) -> bytes:
    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)
    return bytes([(b + key_bytes[i % key_len]) % 256 for i, b in enumerate(data)])

def decrypt_bytes(data: bytes, key: str) -> bytes:
    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)
    return bytes([(b - key_bytes[i % key_len]) % 256 for i, b in enumerate(data)])

def encrypt_text(text: str, key: str) -> str:
    encrypted = encrypt_bytes(text.encode('utf-8'), key)
    return encrypted.hex()

def decrypt_text(cipher_hex: str, key: str) -> str:
    cipher_bytes = bytes.fromhex(cipher_hex)
    decrypted = decrypt_bytes(cipher_bytes, key)
    return decrypted.decode('utf-8', errors='ignore')
