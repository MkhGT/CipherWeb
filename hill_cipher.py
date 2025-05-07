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
    """Parse kunci dari string ke matriks 2x2"""
    try:
        key_numbers = list(map(int, key_str.split(',')))
        if len(key_numbers) != 4:
            raise ValueError("Kunci harus 4 angka dipisahkan koma (contoh: 5,8,17,3)")
        key_matrix = np.array(key_numbers).reshape(2, 2)
        
        # Validasi matriks harus invertible
        det = int(round(np.linalg.det(key_matrix)))
        if gcd(det, 26) != 1:
            raise ValueError("Determinan matriks kunci harus coprime dengan 26")
            
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
    """Enkripsi teks dengan Hill Cipher (2x2)"""
    key_matrix = parse_key(key)
    cleaned_text = clean_text(text)
    
    # Padding jika panjang teks ganjil
    if len(cleaned_text) % 2 != 0:
        cleaned_text += 'X'
    
    numbers = text_to_numbers(cleaned_text)
    encrypted_numbers = []
    
    for i in range(0, len(numbers), 2):
        block = np.array(numbers[i:i+2])
        encrypted_block = np.dot(key_matrix, block) % 26
        encrypted_numbers.extend(encrypted_block)
    
    ciphertext = numbers_to_text(encrypted_numbers)
    return ciphertext

def decrypt(text, key):
    """Dekripsi teks dengan Hill Cipher (2x2)"""
    key_matrix = parse_key(key)
    cleaned_text = clean_text(text)
    
    if len(cleaned_text) % 2 != 0:
        raise ValueError("Panjang ciphertext harus genap")
    
    # Hitung matriks invers
    det = int(round(np.linalg.det(key_matrix)))
    det_inv = modinv(det)
    adjugate = np.array([[key_matrix[1,1], -key_matrix[0,1]], 
                         [-key_matrix[1,0], key_matrix[0,0]]])
    inv_matrix = (det_inv * adjugate) % 26
    
    numbers = text_to_numbers(cleaned_text)
    decrypted_numbers = []
    
    for i in range(0, len(numbers), 2):
        block = np.array(numbers[i:i+2])
        decrypted_block = np.dot(inv_matrix, block) % 26
        decrypted_numbers.extend(decrypted_block)
    
    plaintext = numbers_to_text(decrypted_numbers)
    return plaintext

def format_output(text):
    """Format output: tanpa spasi dan kelompok 5 huruf"""
    no_space = text.replace(" ", "")
    grouped = ' '.join([no_space[i:i+5] for i in range(0, len(no_space), 5)])
    return no_space, grouped