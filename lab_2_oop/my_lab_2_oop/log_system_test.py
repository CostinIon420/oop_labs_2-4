from abc import ABC, abstractmethod
import os

def check_if_account_was_already_created():
    # Verificăm dacă fișierul există înainte de a citi din el
    if not os.path.exists("log.txt"):
        return False
    with open("log.txt", "r") as f:
        return f.read(1) != ""  # Returnează True dacă fișierul nu e gol (deci contul există)

class OperationLogger(ABC):
    @abstractmethod
    def log(self, message: str):
        pass  # Abstract method to be overridden in subclasses

class FileLogger(OperationLogger):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def log(self, message: str):
        with open(self.file_name, 'a') as file:  # Append mode
            file.write(message + '\n')

class ConsoleLogger(OperationLogger):
    def log(self, message: str):
        print("Console Log:", message)

def create_account(auth_file):
    print("Creating a new account.")
    login = input("Enter a new login: ")
    password = input("Enter a new password: ")

    with open(auth_file, 'w') as file:
        file.write(f"{login}\n{password}\n")
    print("Account created successfully.")

def authenticate(auth_file):
    with open(auth_file, 'r') as file:
        stored_login = file.readline().strip()
        stored_password = file.readline().strip()

    login = input("Enter your login: ")
    password = input("Enter your password: ")

    if login == stored_login and password == stored_password:
        print("Authentication successful.")
        return True
    else:
        print("Authentication failed. Incorrect login or password.")
        return False

def perform_operation(logger: OperationLogger, operation: str):
    logger.log("Operation performed: " + operation)

def main():
    auth_file = "log.txt"
    
    # Check if account exists
    not_already_logged = not check_if_account_was_already_created()  # Verificăm dacă nu există cont

    if not_already_logged:
        create_account(auth_file)  # Aici transmitem auth_file ca argument
    else:
        # Authenticate user if account exists
        if not authenticate(auth_file):
            print("Access denied.")
            return  # Exit if authentication fails
    
    # Initialize loggers
    file_logger = FileLogger("logfile.txt")
    console_logger = ConsoleLogger()

    # Perform logging operations
    perform_operation(file_logger, "File operation: Saving data to file")
    perform_operation(console_logger, "Console operation: Displaying information")

if __name__ == "__main__":
    main()