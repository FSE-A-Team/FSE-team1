from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import os
import secrets
import string

# Function to generate a key from a passphrase
def generate_key_from_passphrase(passphrase, salt):
    # Key derivation function setup
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key

# Function to encrypt the data
def encrypt_data(data, key):
    # Initialize the Fernet class with the key
    f = Fernet(key)
    # Encode the data to bytes
    encoded_data = data.encode()
    # Encrypt the data
    encrypted_data = f.encrypt(encoded_data)
    return encrypted_data

# Function to decrypt the data
def decrypt_data(encrypted_data, key):
    # Initialize the Fernet class with the key
    f = Fernet(key)
    # Decrypt the data
    decrypted_data = f.decrypt(encrypted_data)
    # Decode the data from bytes to string
    return decrypted_data.decode()

def generate_salt(length=16):
    # Define the character pool excluding potentially confusing characters
    alphabet = string.ascii_letters + string.digits
    alphabet = alphabet.replace('l', '').replace('I', '').replace('1', '').replace('0', '').replace('O', '')
    
    # Use the secrets.choice() method to select random characters from the alphabet
    salt = ''.join(secrets.choice(alphabet) for i in range(length))
    return salt

# Main flow
if __name__ == "__main__":

    # Get the data, passphrase and salt from the user
    use_method = input("Enter 'e' to encrypt or 'd' to decrypt: ")

    #Encrypt
    if use_method == 'e':
        data = input("Enter data to encrypt: ")
        pass_phrase = input("Enter a passphrase: ")
        salt = input("Enter a salt (leave empty for random salt): ")
        if salt == "":
            salt = generate_salt(16)
            print(f"Salt: {salt}")
        salt = salt.encode()
        key = generate_key_from_passphrase(pass_phrase, salt)
        encrypted_message = encrypt_data(data, key)
        print(f"Encrypted data: {encrypted_message.decode()}")

    #Decrypt
    elif use_method == 'd':
        data = input("Enter data to decrypt: ")
        pass_phrase = input("Enter a passphrase: ")
        salt = input("Enter a salt: ")
        salt = salt.encode()
        key = generate_key_from_passphrase(pass_phrase, salt)
        decrypted_message = decrypt_data(data, key)
        print(f"Decrypted data: {decrypted_message}")
