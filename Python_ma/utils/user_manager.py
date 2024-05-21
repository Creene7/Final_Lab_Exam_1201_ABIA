import os
from utils.user import User

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('data/users.txt'):
            open('data/users.txt', 'w').close()
        else:
            with open('data/users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = User(username, password)

    def save_users(self):
        with open('data/users.txt', 'w') as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password}\n")

    def validate_username(self, username):
        return len(username) >= 4 and username not in self.users

    def validate_password(self, password):
        return len(password) >= 8

    def register(self):
        while True:
            username = input("Enter username: ").strip()
            if not username:
                return
            if not self.validate_username(username):
                print("Invalid username or username already exists. Please try again.")
                continue

            password = input("Enter password: ").strip()
            if not password:
                return
            if not self.validate_password(password):
                print("Password must be at least 8 characters. Please try again.")
                continue

            self.users[username] = User(username, password)
            self.save_users()
            print("Registration successful!")
            return

    def login(self):
        while True:
            username = input("Enter username: ").strip()
            if not username:
                return None

            password = input("Enter password: ").strip()
            if not password:
                return None

            if username in self.users and self.users[username].password == password:
                print("Login successful!")
                return self.users[username]
            else:
                print("Invalid username or password. Please try again.")