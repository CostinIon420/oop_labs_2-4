import os
from abc import ABC, abstractmethod

def check_if_account_was_already_created():
    return os.path.exists("log.txt") and not check_if_file_is_empty("log.txt")

def check_if_file_is_empty(file_path):
    with open(file_path, "r") as f:
        return f.read(1) == ""


class OperationLogger(ABC):
    @abstractmethod
   
    def log(self, message: str):
        pass

class FileLogger(OperationLogger):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def log(self, message: str):
        with open(self.file_name, 'a') as file: 
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

class Student:
    def __init__(self, id, name, surname, group, faculty, status):
        self.id = id
        self.name = name
        self.surname = surname
        self.group = group
        self.faculty = faculty
        self.status = status

    def __str__(self):
        return f"{self.id}, {self.name}, {self.surname}, {self.group}, {self.faculty}, {self.status}"

class Catalog:
    def __init__(self):
        self.catalog = []
        self.graduated_students = []

    def check_if_faculty_exists(self, faculty):
        if faculty not in faculties:
            faculty = input("This faculty doesn't exist, please choose another: ")
        return faculty

    def enroll(self):
        id = input("Student ID: ")
        if any(student.id == id for student in self.catalog):
            print("A student with this ID already exists. Try a different ID.")
            return

        name = input("Student name: ")
        surname = input("Student surname: ")
        group = input("Student group: ")
        faculty = input("Faculty: ")
        faculty = self.check_if_faculty_exists(faculty)
        status = "not graduated"

        new_student = Student(id, name, surname, group, faculty, status)
        self.catalog.append(new_student)
        SaveManage().save_new_student(new_student)
        print(f"Student {name} {surname} enrolled successfully.")

    def display_data(self):
        """Displays all non-graduated students."""
        if not self.catalog:
            print("There are no non-graduated students.")
        else:
            print("Non-graduated Students:")
            for student in self.catalog:
                print(student)

    def graduate_student(self):
        id = input("Enter student ID: ")
        for student in self.catalog:
            if id == student.id:
                student.status = "graduated"
                self.graduated_students.append(student)
                self.catalog.remove(student)
                SaveManage().save_graduate_student(student)
                SaveManage().update_catalog_file(self.catalog)
                print(f"Student {student.name} {student.surname} has graduated.")
                return
        print(f"Cannot graduate student with ID {id}: student not found.")

    def display_graduated_students(self):
        """Displays all graduated students."""
        if not self.graduated_students:
            print("There are no graduated students.")
        else:
            print("Graduated Students:")
            for student in self.graduated_students:
                print(student)

    def batch_enroll(self, file_path):
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    id, name, surname, group, faculty = line.strip().split(", ")
                    if any(student.id == id for student in self.catalog):
                        print(f"Skipping student with ID {id}: already exists.")
                        continue
                    faculty = self.check_if_faculty_exists(faculty)
                    new_student = Student(id, name, surname, group, faculty, "not graduated")
                    self.catalog.append(new_student)
                    SaveManage().save_new_student(new_student)
                    print(f"Student {name} {surname} enrolled from file.")
                except ValueError:
                    print(f"Error: Invalid data format for line '{line.strip()}'. Skipping.")

   
    def batch_graduate(self, file_path):
      
        
      
        with open(file_path, 'r') as f:
            for line in f:
               
                data = line.strip().split(',')
                
            
                
               
                id = str(data[0].strip())
                print(id,"\n")
                
                student_found = False
                for student in self.catalog:
                    print("student id",student.id)
                    if str(student.id) == str(id):
                        student.status = "graduated" 
                        self.graduated_students.append(student) 
                        self.catalog.remove(student) 
                        student_found = True
                        print(f"Student {student.name} {student.surname} graduated from file.")
                        break  
                
             
                if not student_found:
                    print(f"Cannot graduate student with ID {id}: student not found.")
        

        SaveManage().update_graduated_file(self.graduated_students)
        SaveManage().update_catalog_file(self.catalog)


class SaveManage:
    def load_students(self):
        if not check_if_file_is_empty("catalog.txt"):
            with open("catalog.txt", "r") as f:
                for line in f:
                    data = line.strip().split(", ")
                    if len(data) == 6:
                        student = Student(data[0], data[1], data[2], data[3], data[4], data[5])
                        catalog.catalog.append(student)

    def load_graduated_students(self):
        if not check_if_file_is_empty("graduated.txt"):
            with open("graduated.txt", "r") as f:
                for line in f:
                    data = line.strip().split(", ")
                    if len(data) == 6:
                        student = Student(data[0], data[1], data[2], data[3], data[4], data[5])
                        catalog.graduated_students.append(student)

    def save_new_student(self, new_student):
        with open("catalog.txt", "a") as f:
            f.write(str(new_student) + "\n")

    def save_graduate_student(self, student):
        with open("graduated.txt", "a") as f:
            f.write(str(student) + "\n")

    def update_catalog_file(self, catalog_data):
        with open("catalog.txt", "w") as f:
            for student in catalog_data:
                f.write(str(student) + "\n")

    def update_graduated_file(self, graduated_data):
        with open("graduated.txt", "w") as f:
            for student in graduated_data:
                f.write(str(student) + "\n")


def see_faculties():
    if not faculties:
        print("There are no faculties.")
    else:
        print("Available faculties:")
        for faculty in faculties:
            print(faculty)

def add_new_faculty():
    new_faculty = input("Name the new faculty: ")
    faculties.append(new_faculty)
    with open('faculties.txt', 'a') as f:
        f.write(new_faculty + '\n')
    print(f"The faculty '{new_faculty}' has been added.")

def remove_faculty():
    faculty_to_remove = input("Enter the name of the faculty to remove: ")
    if faculty_to_remove in faculties:
        faculties.remove(faculty_to_remove)
        with open('faculties.txt', 'w') as f:
            for faculty in faculties:
                f.write(faculty + '\n')
        print(f"The faculty '{faculty_to_remove}' has been removed.")
    else:
        print(f"The faculty '{faculty_to_remove}' does not exist.")


is_log = False
auth_file = "log.txt"

while not is_log:
    if not check_if_account_was_already_created():
        create_account(auth_file)
    else:
        if authenticate(auth_file):
            is_log = True
        else:
            print("Access denied.")

if is_log:
    with open('faculties.txt', 'r') as f:
        faculties = [line.strip() for line in f]

    file_logger = FileLogger("logfile.txt")
    console_logger = ConsoleLogger()
    perform_operation(file_logger, "File operation: Saving data to file")
    perform_operation(console_logger, "Console operation: Displaying information")
    catalog = Catalog()
    SaveManage().load_students()
    SaveManage().load_graduated_students()

    while True:
        print("\nMenu Options:")
        print("1) Enroll a new student")
        print("2) View non-graduated students")
        print("3) Graduate a student")
        print("4) Display graduated students")
        print("5) Check student in faculty")
        print("6) See faculties")
        print("7) Add a new faculty")
        print("8) Remove a faculty")
        print("9) Batch enroll students from file")
        print("10) Batch graduate students from file")
        print("0) Exit")

        option = input("Choose an option: ")
        if option == "1":
            catalog.enroll()
        elif option == "2":
            catalog.display_data()
        elif option == "3":
            catalog.graduate_student()
        elif option == "4":
            catalog.display_graduated_students()
        elif option == "5":
            id = input("Enter the student ID to check: ")
            print(catalog.check_student_in_faculty(id))
        elif option == "6":
            see_faculties()
        elif option == "7":
            add_new_faculty()
        elif option == "8":
            remove_faculty()
        elif option == "9":
            file_path = "batch_enroll.txt"
            catalog.batch_enroll(file_path)
        elif option == "10":
            file_path = "batch_graduate.txt"
            catalog.batch_graduate(file_path)
        elif option == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")
