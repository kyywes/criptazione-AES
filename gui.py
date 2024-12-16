import os
import sys
print("Interprete Python:", sys.executable)
print("Percorsi cercati:", sys.path)
from tkinter import Tk, filedialog, messagebox
from tkinter.ttk import Button, Label, Entry
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from hashlib import pbkdf2_hmac

def generate_key(password, salt=None):
    if salt is None:
        salt = get_random_bytes(16)
    key = pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)
    return key, salt

def encrypt_file(filepath, password):
    with open(filepath, "rb") as f:
        plaintext = f.read()

    # Genera salt e IV
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)

    # Deriva la chiave
    key, salt = generate_key(password, salt)

    # Cifra i dati
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # Salva salt, IV e dati crittografati
    encrypted_filepath = filepath + ".enc"
    with open(encrypted_filepath, "wb") as f:
        f.write(salt + iv + ciphertext)
    
    messagebox.showinfo("Successo", f"File cifrato salvato come: {encrypted_filepath}")

def decrypt_file(filepath, password):
    with open(filepath, "rb") as f:
        data = f.read()

    # Estrai salt e IV
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]

    # Deriva la chiave
    key, _ = generate_key(password, salt)

    # Decifra i dati
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    except ValueError:
        messagebox.showerror("Errore", "Decifratura fallita: chiave o dati non validi.")
        return

    # Salva il file decifrato
    decrypted_filepath = filepath.replace(".enc", "")
    with open(decrypted_filepath, "wb") as f:
        f.write(plaintext)
    
    messagebox.showinfo("Successo", f"File decifrato salvato come: {decrypted_filepath}")

class EncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryptor App")
        self.password = None

        Label(root, text="Inserisci la password per la crittografia AES:").pack(pady=5)
        self.password_entry = Entry(root, show="*")
        self.password_entry.pack(pady=5)

        Button(root, text="Imposta Password", command=self.set_password).pack(pady=5)
        Button(root, text="Cifra File", command=self.encrypt_file).pack(pady=5)
        Button(root, text="Decifra File", command=self.decrypt_file).pack(pady=5)
        Button(root, text="Esci", command=root.quit).pack(pady=5)

    def set_password(self):
        self.password = self.password_entry.get()
        if self.password:
            messagebox.showinfo("Successo", "Password impostata!")
        else:
            messagebox.showwarning("Errore", "Inserisci una password valida!")

    def encrypt_file(self):
        if not self.password:
            messagebox.showwarning("Errore", "Imposta una password prima di procedere!")
            return

        filepath = filedialog.askopenfilename(title="Seleziona il file da cifrare")
        if filepath:
            encrypt_file(filepath, self.password)

    def decrypt_file(self):
        if not self.password:
            messagebox.showwarning("Errore", "Imposta una password prima di procedere!")
            return

        filepath = filedialog.askopenfilename(title="Seleziona il file da decifrare")
        if filepath:
            decrypt_file(filepath, self.password)

if __name__ == "__main__":
    root = Tk()
    root.geometry("400x300")
    app = EncryptorApp(root)
    root.mainloop()
