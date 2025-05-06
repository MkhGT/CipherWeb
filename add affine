from flask import Flask, render_template, request
import autokey_vigenere
import playfair
import affine


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    mode = ''
    algo = ''
    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        mode = request.form['mode']
        algo = request.form['algorithm']

        if algo == 'autokey_vigenere':
            result = autokey_vigenere.encrypt(text, key) if mode == 'encrypt' else autokey_vigenere.decrypt(text, key)
        elif algo == 'playfair':
            result = playfair.encrypt(text, key) if mode == 'encrypt' else playfair.decrypt(text, key)

    return render_template('index.html', result=result, mode=mode, algo=algo)

if __name__ == '__main__':
    app.run(debug=True)
