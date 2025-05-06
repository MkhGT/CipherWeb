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
        if algo == 'affine':
            try:
                if ',' not in key:
                    raise ValueError("Format kunci untuk Affine harus 'a,b' (misalnya: '5,8')")
                a, b = key.split(',')
                key = f"{int(a)},{int(b)}" 
                
            result = affine.encrypt(text, key) if mode == 'encrypt' else affine.decrypt(text, key)
            except ValueError as e:
                error_message = str(e) 
                result = ''

    return render_template('index.html', result=result, mode=mode, algo=algo)

if __name__ == '__main__':
    app.run(debug=True)
