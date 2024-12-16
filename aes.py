import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from hashlib import pbkdf2_hmac
from getpass import getpass

# Funzione per generare una chiave AES da una password
def generate_key(password, salt=b"static_salt_16b"):
    return pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)

# Funzione per cifrare un file
def encrypt_file(filepath, key):
    with open(filepath, "rb") as f:
        plaintext = f.read()

    # Padding e cifratura
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # Salva il file cifrato
    encrypted_filepath = filepath + ".enc"
    with open(encrypted_filepath, "wb") as f:
        f.write(iv + ciphertext)
    
    print(f"File cifrato salvato come: {encrypted_filepath}")

# Funzione per decifrare un file
def decrypt_file(filepath, key):
    with open(filepath, "rb") as f:
        data = f.read()

    # Estrai IV e dati cifrati
    iv = data[:16]
    ciphertext = data[16:]

    # Decifratura
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Salva il file decifrato
    decrypted_filepath = filepath.replace(".enc", "")
    with open(decrypted_filepath, "wb") as f:
        f.write(plaintext)
    
    print(f"File decifrato salvato come: {decrypted_filepath}")

def main():
    print("AES File Encryptor/Decryptor")
    password = getpass("Inserisci una password per la crittografia: ")
    key = generate_key(password)

    while True:
        print("\nOpzioni:")
        print("1. Cifrare un file")
        print("2. Decifrare un file")
        print("3. Esci")
        choice = input("Scegli un'opzione: ")

        if choice == "1":
            filepath = input("Inserisci il percorso del file da cifrare: ")
            if os.path.exists(filepath):
                encrypt_file(filepath, key)
            else:
                print("File non trovato!")
        elif choice == "2":
            filepath = input("Inserisci il percorso del file da decifrare: ")
            if os.path.exists(filepath):
                decrypt_file(filepath, key)
            else:
                print("File non trovato!")
        elif choice == "3":
            print("Uscita...")
            break
        else:
            print("Scelta non valida, riprova.")

if __name__ == "__main__":
    main()
