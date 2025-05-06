from flask import Flask, render_template, request
from extended_vigenere import encrypt_text, decrypt_text

app = Flask(__name__)

@app.route('/extended_vigenere', methods=['GET', 'POST'])
def extended_vigenere():
    result = ''
    mode = ''
    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        mode = request.form['mode']

        if mode == 'encrypt':
            result = encrypt_text(text, key)
        elif mode == 'decrypt':
            result = decrypt_text(text, key)

    return render_template('extended_vigenere.html', result=result, mode=mode)
