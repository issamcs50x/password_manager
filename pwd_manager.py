from os import path

def main():

    # 1- get master password
    master_password = input("Master password: ").strip()

    # 2- generate a random salt and store it localy
    # the salt.txt existance indicates that the user previously created a password
    if not path.exists("salt.txt"):
        salt = generate_salt()
        with open("salt.txt", "w") as f:
            f.write(salt)
    else:
        with open("salt.txt", "r") as f:
            salt = f.read()

    # 3- combine the master password with the salt
    master_password += salt

    # 4- deriving a key from the master password
    key = deriving_key(master_password)

    # 5- create json file if not exist
    if not path.exists("log.json"):
        with open("log.json", "w") as f:
            json.dump({}, f)

    # 6- store the encrypted VALIDWORD
    VALIDWORD = "VALID_KEY"
    if not path.exists("valid_key.txt"):
        with open("valid_key.txt", "w") as f:
            f.write(encryptor(VALIDWORD, key))
    # check if the user entred the correct password
    else:
        with open("valid_key.txt", "r") as f:
            decrypted_word = encryptor(f.read(), key * -1)
        if decrypted_word != VALIDWORD:
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
            register(key)
        elif choice == "2":
            view(key)
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

# - generate a random salt 
from random import choice, shuffle
from string import ascii_uppercase, ascii_lowercase, digits

def generate_salt():
    parts = (ascii_uppercase, ascii_lowercase, digits)
    salt = [choice(parts[i]) for i in range(len(parts))]
    shuffle(salt)
    return "".join(salt)

# - deriving a key from the master password
def deriving_key(password):
    total = 0
    for char in password:
        total += ord(char)
    return total % 26

UPPER_START = ord("A")
LOWER_START = ord("a")
DIGIT_START = ord("0")

def encryptor(text, _key):
    result = ""
    for char in text:
        # - Preserve the letter's case
        if char.isalpha():
            if char.islower():
                shift = (((ord(char) - LOWER_START) + _key) % 26) + LOWER_START
            else:
                shift = (((ord(char) - UPPER_START) + _key) % 26) + UPPER_START
        elif char.isdigit():
            shift = (((ord(char) - DIGIT_START ) + _key) % 10) + DIGIT_START
        # - Preserve any non alphabetic char
        else:
            result += char
            continue   
        result += chr(shift) 
    return result

import json

def register(key):
    # 1- get infos
    account = input("Account: ").strip()
    password = input("password: ").strip()
    # 2- encrypte infos:
    encrypted_data = {
        encryptor(account, key): encryptor(password, key)
        }
    # 3- load stored data
    with open("log.json", "r") as f:
        data = json.load(f)
    # 4- store encrypted data to a json file
    data.update(encrypted_data)
    with open("log.json", "w") as f:
        json.dump(data, f)
    print("data registred successfuly.")

def view(key):
    # 1- load data from the json file:
    with open("log.json", "r") as f:
        data = json.load(f)
    # 2- decrypte data and display it
    print("-" * 10)
    for cipher_account, cipher_password in data.items():
        print(encryptor(cipher_account, key * -1),
              "|",
              encryptor(cipher_password, key * -1))
    print("-" * 10)
main()