from cryptography.fernet import Fernet
import json
import os
import random
import string

# Generate and save encryption key
def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

# Load encryption key
def load_key():
    return open('secret.key', 'rb').read()

# Initialize the key and cipher
if not os.path.exists('secret.key'):
    generate_key()
key = load_key()
cipher = Fernet(key)

# Load passwords from a file
def load_passwords():
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as file:
            return json.load(file)
    return {}

# Save passwords to a file
def save_passwords(passwords):
    with open('passwords.json', 'w') as file:
        json.dump(passwords, file)

# Generate a strong password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Add a password
def add_password(category, service, username, password):
    encrypted_password = cipher.encrypt(password.encode()).decode()
    passwords[category][service] = {'username': username, 'password': encrypted_password}
    save_passwords(passwords)

# Retrieve a password
def retrieve_password(category, service):
    encrypted_password = passwords[category][service]['password']
    decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
    return decrypted_password

# Main menu
def main():
    global passwords
    passwords = load_passwords()

    while True:
        print("\nPassword Manager")
        print("1. Generate Strong Password")
        print("2. Add Password")
        print("3. Retrieve Password")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            length = int(input("Enter the desired length of the password: "))
            print(f"Generated password: {generate_password(length)}")
        elif choice == '2':
            category = input("Enter category: ")
            service = input("Enter service: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            if category not in passwords:
                passwords[category] = {}
            add_password(category, service, username, password)
            print("Password added successfully!")
        elif choice == '3':
            category = input("Enter category: ")
            service = input("Enter service: ")
            if category in passwords and service in passwords[category]:
                print(f"Password: {retrieve_password(category, service)}")
            else:
                print("Password not found!")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
