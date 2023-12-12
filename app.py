import streamlit as st
from cryptography.fernet import Fernet, InvalidToken
import os

def generate_key():
    key = Fernet.generate_key()
    with open("Secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("Secret.key", "rb").read()

def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
        try:
            decrypted_data = f.decrypt(encrypted_data)
        except InvalidToken:
            print("Invalid key")
            return
    with open(filename, "wb") as file:
        file.write(decrypted_data)

# create the Streamlit UI using appropriate controls and widgets.
def main():
    # Set page title and description
    st.title("File Encryption/Decryption")
    st.write("Encrypt or decrypt files using Fernet encryption.")

    # Get user's choice (encrypt or decrypt)
    choice = st.radio("Choose an operation:", ('Encrypt', 'Decrypt'))

    if choice == 'Encrypt':
        # Input file name to encrypt
        filename = st.text_input("Enter the file name to encrypt (including file extension):")

        # Check if the file exists
        if os.path.exists(filename):
            st.info(f"Encrypting file: {filename}")
            generate_key()
            key = load_key()
            encrypt(filename, key)
            st.success("File encrypted successfully!")
        else:
            st.error(f"File '{filename}' not found. Please check the file name and try again.")

    elif choice == 'Decrypt':
        # Input file name to decrypt
        filename = st.text_input("Enter the file name to decrypt (including file extension):")

        # Check if the file exists
        if os.path.exists(filename):
            st.info(f"Decrypting file: {filename}")
            key = load_key()
            decrypt(filename, key)
            st.success("File decrypted successfully!")
        else:
            st.error(f"File '{filename}' not found. Please check the file name and try again.")

    else:
        st.error("Invalid choice. Please select either 'Encrypt' or 'Decrypt'.")

if __name__ == "__main__":
    main()