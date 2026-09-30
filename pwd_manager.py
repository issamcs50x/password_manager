from os import path, urandom
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import json

def main():

    # 1- get master password
    master_password = input("Master password: ").strip().encode()

    # 2- generate a random salt and store it localy
    # the salt.txt existance indicates that the user previously created a password
    if not path.exists("salt.enc"):
        salt = urandom(16)
        with open("salt.enc", "wb") as f:
            f.write(salt)
    else:
        with open("salt.enc", "rb") as f:
            salt = f.read()

    # 4- deriving a key from the master password
    key = deriving_key(master_password, salt)

    #
    cipher = Fernet(key)

    # 5- create json file if not exist
    if not path.exists("log.json"):
        with open("log.json", "w") as f:
            json.dump({}, f)

    # 6- store the encrypted VALIDWORD
    VALIDWORD = "VALID_KEY"
    if not path.exists("valid_key.enc"):
        with open("valid_key.enc", "wb") as f:
            f.write(cipher.encrypt(VALIDWORD.encode()))
    # check if the user entred the correct password
    else:
        with open("valid_key.enc", "rb") as f:
            try:
                cipher.decrypt(f.read()).decode()
            except:
                print("Invalid password!")
                return 0                    

    while True:
        # 7- display options
        options = ["register", "view", "quit"]
        for index, option in enumerate(options, start=1):
            print(f"{index}- {option.capitalize()}")

        # 8- get user choice
        choice = input("choose a number:").strip()

        if choice == "1":
            register(cipher)
        elif choice == "2":
            view(cipher)
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

# - deriving a key from the master password
def deriving_key(password, _salt):
    # Key mixer
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,          
    salt=_salt,
    iterations=600000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def register(cipher):
    # 1- get infos
    account = input("Account: ").strip()
    password = input("password: ").strip()
    # 2- encrypte infos:
    cipher_account = cipher.encrypt(account.encode()).decode()
    cipher_password = cipher.encrypt(password.encode()).decode()
    encrypted_data = {
        cipher_account: cipher_password 
        }
    # 3- load stored data
    with open("log.json", "r") as f:
        data = json.load(f)
    # 4- store encrypted data to a json file
    data.update(encrypted_data)
    with open("log.json", "w") as f:
        json.dump(data, f)
    print("data registred successfuly.")

def view(cipher):
    # 1- load data from the json file:
    with open("log.json", "r") as f:
        data = json.load(f)
    # 2- decrypte data and display it
    print("-" * 10)
    for cipher_account, cipher_password in data.items():
        print(cipher.decrypt(cipher_account.encode()).decode(),
              "|",
              cipher.decrypt(cipher_password.encode()).decode())
    print("-" * 10)
main()

