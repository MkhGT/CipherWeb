# cipher_app.py
import streamlit as st
import playfair
import autokey_vigenere
import extended_vigenere
import vigenere_standard
import affine

def format_output(text):
    no_space = text.replace(" ", "")
    grouped = " ".join([no_space[i:i+5] for i in range(0, len(no_space), 5)])
    return no_space, grouped

def main():
    st.title("🔐 Web-Based Classical Cipher App")

    cipher_type = st.selectbox("Pilih Cipher:", [
        "Vigenere Cipher",
        "Auto-key Vigenere Cipher",
        "Extended Vigenere Cipher",
        "Affine Cipher",
        "Playfair Cipher",
        "Hill Cipher"
    ])

    mode = st.radio("Mode:", ["Enkripsi", "Dekripsi"])

    input_method = st.radio("Metode Input:", ["Teks Langsung", "Upload File"])
    key = st.text_input("Masukkan Kunci:", max_chars=100)

    input_text = ""
    file_data = None

    if input_method == "Teks Langsung":
        input_text = st.text_area("Masukkan Pesan:")
    else:
        uploaded_file = st.file_uploader("Upload File", type=None)
        if uploaded_file:
            file_data = uploaded_file.read()

    if st.button("Proses"):
        if not key:
            st.warning("Kunci tidak boleh kosong!")
            return

        result = ""

        try:
            if cipher_type == "Vigenere Cipher":
                result = vigenere_standard.encrypt(input_text, key) if mode == "Enkripsi" else vigenere_standard.decrypt(input_text, key)

            elif cipher_type == "Auto-key Vigenere Cipher":
                result = autokey_vigenere.encrypt(input_text, key) if mode == "Enkripsi" else autokey_vigenere.decrypt(input_text, key)

            elif cipher_type == "Extended Vigenere Cipher":
                if file_data:
                    result = extended_vigenere.encrypt_bytes(file_data, key) if mode == "Enkripsi" else extended_vigenere.decrypt_bytes(file_data, key)
                    st.download_button("Download Hasil", result, file_name="result.enc" if mode == "Enkripsi" else "result.dec")
                    return
                else:
                    result_bytes = extended_vigenere.encrypt_bytes(input_text.encode(), key) if mode == "Enkripsi" else extended_vigenere.decrypt_bytes(input_text.encode(), key)
                    result = result_bytes.decode(errors='ignore')

            elif cipher_type == "Affine Cipher":
                result = affine.encrypt(input_text, key) if mode == "Enkripsi" else affine.decrypt(input_text, key)

            elif cipher_type == "Playfair Cipher":
                result = playfair.encrypt(input_text, key) if mode == "Enkripsi" else playfair.decrypt(input_text, key)

            elif cipher_type == "Hill Cipher":
                result = hill_encrypt(input_text, key) if mode == "Enkripsi" else hill_decrypt(input_text, key)

            no_space, grouped = format_output(result)
            st.subheader("Hasil:")
            st.write("Tanpa Spasi:")
            st.code(no_space)
            st.write("Kelompok 5-Huruf:")
            st.code(grouped)

            st.download_button("Download Ciphertext", result.encode(), file_name="ciphertext.txt")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()