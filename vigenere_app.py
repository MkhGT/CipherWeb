from flask import Flask, render_template, request
from vigenere_standard import encrypt, decrypt
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('vigenere.html')

@app.route('/vigenere', methods=['POST'])
def process():
    text = request.form['text']
    key = request.form['key']
    action = request.form['action']
    format_type = request.form.get('format', 'no_space')

    if action == 'encrypt':
        result = encrypt(text, key, format_type)
    else:
        result = decrypt(text, key)

    return render_template('vigenere.html', result=result, text=text, key=key)

if __name__ == '__main__':
    app.run(debug=True)
