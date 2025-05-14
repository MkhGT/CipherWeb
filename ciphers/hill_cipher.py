import numpy as np
import string
from math import gcd

ALPHABET = string.ascii_uppercase

def clean_text(text):
    """Hanya menyimpan karakter alfabet, ubah ke uppercase"""
    return ''.join(filter(str.isalpha, text.upper()))

def text_to_numbers(text):
    """Konversi teks ke angka (A=0, B=1, ..., Z=25)"""
    return [ord(c) - ord('A') for c in text]

def numbers_to_text(numbers):
    """Konversi angka kembali ke teks"""
    return ''.join([chr(n + ord('A')) for n in numbers])

def parse_key(key_str):
    """Parse kunci dari string ke matriks (otomatis deteksi ukuran 2x2 atau 3x3)"""
    try:
        # Coba parsing sebagai angka (format lama)
        if ',' in key_str:
            key_numbers = list(map(int, key_str.split(',')))
            n = int(len(key_numbers) ** 0.5)
            if n * n != len(key_numbers):
                raise ValueError("Format angka: jumlah harus 4, 9, atau 16 angka")
        else:
            # Parsing sebagai huruf (format baru)
            key_str = clean_text(key_str)
            n = int(len(key_str) ** 0.5)
            if n * n != len(key_str):
                raise ValueError("Format huruf: panjang harus 4, 9, atau 16 karakter")
            key_numbers = [ord(c) - ord('A') for c in key_str]

        key_matrix = np.array(key_numbers).reshape(n, n)
        det = int(round(np.linalg.det(key_matrix)))
        
        if det == 0:
            raise ValueError("Matriks kunci tidak bisa diinvers (determinan = 0)")
        if gcd(det % 26, 26) != 1:
            raise ValueError("Determinan matriks harus coprime dengan 26")
            
        return key_matrix
    except ValueError as e:
        raise ValueError(f"Kunci tidak valid: {e}")

def modinv(a, m=26):
    """Modular inverse"""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Tidak ada inverse modular untuk {a} modulo {m}")

def encrypt(text, key):
    """Enkripsi teks dengan Hill Cipher"""
    key_matrix = parse_key(key)
    cleaned_text = clean_text(text)
    n = key_matrix.shape[0]
    
    # Padding jika perlu
    padding_length = n - len(cleaned_text) % n
    if padding_length > 0:
        cleaned_text += 'X' * padding_length
    
    numbers = text_to_numbers(cleaned_text)
    encrypted_numbers = []
    
    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n])
        encrypted_block = np.dot(key_matrix, block) % 26
        encrypted_numbers.extend(encrypted_block)
    
    return numbers_to_text(encrypted_numbers)

def decrypt(text, key):
    """Dekripsi teks dengan Hill Cipher"""
    key_matrix = parse_key(key)
    cleaned_text = clean_text(text)
    n = key_matrix.shape[0]
    
    if len(cleaned_text) % n != 0:
        raise ValueError(f"Panjang ciphertext harus kelipatan {n}")
    
    # Hitung matriks invers
    det = int(round(np.linalg.det(key_matrix)))
    det_inv = modinv(det)
    adjugate = np.round(np.linalg.inv(key_matrix) * det).astype(int)
    inv_matrix = (adjugate * det_inv) % 26
    
    numbers = text_to_numbers(cleaned_text)
    decrypted_numbers = []
    
    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n])
        decrypted_block = np.dot(inv_matrix, block) % 26
        decrypted_numbers.extend(decrypted_block)
    
    # Hapus padding
    decrypted_text = numbers_to_text(decrypted_numbers)
    if decrypted_text.endswith('X'):
        decrypted_text = decrypted_text[:-decrypted_text.count('X')]
    
    return decrypted_text

def format_output(text):
    """Format output untuk kompatibilitas"""
    no_space = text.replace(" ", "")
    grouped = ' '.join([no_space[i:i+5] for i in range(0, len(no_space), 5)])
    return no_space, grouped
