from flask import Flask, request, render_template, send_file
import os
import ciphers.vigenere_standard as vigenere_standard
import ciphers.extended_vigenere as extended_vigenere
import ciphers.autokey_vigenere as autokey_vigenere
import ciphers.playfair as playfair
import ciphers.affine as affine
import ciphers.hill_cipher as hill_cipher
from werkzeug.utils import secure_filename

def clean_text(text):
    return ''.join(filter(str.isalpha, text.upper()))

def group_five(text):
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    grouped_result = None
    if request.method == 'POST':
        cipher = request.form['cipher']
        mode = request.form['mode']
        key = request.form.get('key')
        a = request.form.get('a')
        b = request.form.get('b')

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            text = request.form['text']

        if cipher == 'vigenere':
            result = vigenere_standard.encrypt(text, key) if mode == 'e' else vigenere_standard.decrypt(text, key)
        elif cipher == 'extended_vigenere':
            result = extended_vigenere.encrypt_file(text, key) if mode == 'e' else extended_vigenere.decrypt_file(text, key)
        elif cipher == 'autokey':
            result = autokey_vigenere.encrypt(text, key) if mode == 'e' else autokey_vigenere.decrypt(text, key)
        elif cipher == 'playfair':
            result = playfair.encrypt(text, key) if mode == 'e' else playfair.decrypt(text, key)
        elif cipher == 'hill':
            result = hill_cipher.encrypt(text, key) if mode == 'e' else hill_cipher.decrypt(text, key)
        elif cipher == 'affine':
            result = affine.encrypt(text, key) if mode == 'e' else affine.decrypt(text, key)

        if result:
            grouped_result = group_five(result)
            output_path = os.path.join(OUTPUT_FOLDER, 'output.txt')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)

    return render_template('index.html', result=result, grouped=grouped_result)

@app.route('/download')
def download():
    return send_file('outputs/output.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
