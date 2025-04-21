import numpy as np
import string

ALPHABET = string.ascii_uppercase
MODULO = 26

### PLAYFAIR CIPHER ###
def generate_playfair_matrix(key):
    key = clean_text(key).replace("J", "I")
    matrix = []
    for c in key + ALPHABET:
        if c not in matrix and c != 'J':
            matrix.append(c)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, letter):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == letter:
                return i, j

def process_playfair(text):
    text = clean_text(text).replace("J", "I")
    i = 0
    pairs = []
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'
        if a == b:
            b = 'X'
            i += 1
        else:
            i += 2
        pairs.append((a, b))
    return pairs
    
def clean_playfair_output(text):
    cleaned = ''
    i = 0
    while i < len(text):
        cleaned += text[i]
        if i+2 < len(text) and text[i] == text[i+2] and text[i+1] == 'X':
            i += 2  # skip X
        else:
            i += 1
    return cleaned


def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    pairs = process_playfair(text)
    ciphertext = ''
    for a, b in pairs:
        ax, ay = find_position(matrix, a)
        bx, by = find_position(matrix, b)
        if ax == bx:
            ciphertext += matrix[ax][(ay+1)%5] + matrix[bx][(by+1)%5]
        elif ay == by:
            ciphertext += matrix[(ax+1)%5][ay] + matrix[(bx+1)%5][by]
        else:
            ciphertext += matrix[ax][by] + matrix[bx][ay]
    return ciphertext

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    pairs = process_playfair(text)
    plaintext = ''
    for a, b in pairs:
        ax, ay = find_position(matrix, a)
        bx, by = find_position(matrix, b)
        if ax == bx:
            plaintext += matrix[ax][(ay-1)%5] + matrix[bx][(by-1)%5]
        elif ay == by:
            plaintext += matrix[(ax-1)%5][ay] + matrix[(bx-1)%5][by]
        else:
            plaintext += matrix[ax][by] + matrix[bx][ay]
    return clean_playfair_output(plaintext)

