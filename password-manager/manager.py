import hashlib
import getpass

# Dictionary to store usernames and their corresponding hashed passwords
password_manager = {}

# Function to create a new account by taking a username and password from the user,
# hashing the password, and storing it in the password manager dictionary
def create_account():
    username = input("Enter your desired username: ")
    password = getpass.getpass("Enter your desired password: ")
    # Hash the password using SHA-256 and store it in the dictionary
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    password_manager[username] = hashed_password
    print("Account created successfully!")

# Function to allow a user to log in by verifying their username and password
# against the stored data in the password manager dictionary
def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    # Hash the entered password to compare with the stored hash
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Check if the username exists and the password matches the stored hash
    if username in password_manager.keys() and password_manager[username] == hashed_password:
        print("Login successful!")
    else:
        print("Invalid username or password.")

# Main function to provide a simple user interface for creating accounts, logging in,
# or exiting the program
def main():
    while True:
        # Prompt the user to choose an action: create an account, log in, or exit
        choice = input("Enter 1 to create an account, 2 to login, or 0 to exit: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

# Entry point of the program
if __name__ == "__main__":
    main()
