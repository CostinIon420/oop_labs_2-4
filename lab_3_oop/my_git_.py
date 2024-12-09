import os
import time
import threading
from datetime import datetime

# Clasa de bază pentru fișiere
class DocumentFile:
    def __init__(self, filename):
        self.filename = filename
        self.extension = os.path.splitext(filename)[1]
        self.created_date = datetime.fromtimestamp(os.path.getctime(filename))
        self.last_modified_date = datetime.fromtimestamp(os.path.getmtime(filename))

    def display_info(self):
        print(f"Filename: {self.filename}")
        print(f"Extension: {self.extension}")
        print(f"Created Date: {self.created_date}")
        print(f"Last Modified Date: {self.last_modified_date}")

# Clasa pentru fișiere imagine
class ImageFile(DocumentFile):
    def __init__(self, filename):
        super().__init__(filename)
        self.width, self.height = self.get_image_dimensions()

    def get_image_dimensions(self):
        # Înlocuiește cu cod pentru a obține dimensiunile reale ale imaginii, dacă e posibil
        return (800, 600)  # Dimensiuni simulate

    def display_info(self):
        super().display_info()
        print(f"Dimensions: {self.width}x{self.height}")

# Clasa pentru fișiere text
class TextFile(DocumentFile):
    def __init__(self, filename):
        super().__init__(filename)

    def display_info(self):
        super().display_info()
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            print(f"Line Count: {len(lines)}")
            print(f"Word Count: {sum(len(line.split()) for line in lines)}")
            print(f"Character Count: {sum(len(line) for line in lines)}")

# Clasa principală pentru monitorizarea documentelor
class DocumentMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.snapshot = {}  # Dictionar care reține ultimul timp de modificare pentru fiecare fișier
        self.load_files()

    def load_files(self):
        self.files = {}
        for filename in os.listdir(self.folder_path):
            filepath = os.path.join(self.folder_path, filename)
            if filename.endswith(('.png', '.jpg')):
                self.files[filename] = ImageFile(filepath)
            elif filename.endswith('.txt'):
                self.files[filename] = TextFile(filepath)
            # Adaugă alte tipuri de fișiere aici, după necesitate

    def commit(self):
        # Actualizează snapshot-ul pentru toate fișierele monitorizate
        self.snapshot = {filename: os.path.getmtime(os.path.join(self.folder_path, filename))
                         for filename in self.files}
        print("Snapshot updated.")

    def info(self, filename):
        if filename in self.files:
            self.files[filename].display_info()
        else:
            print(f"File '{filename}' not found.")

    def status(self):
        for filename, file_obj in self.files.items():
            filepath = os.path.join(self.folder_path, filename)
            last_modified = os.path.getmtime(filepath)
            status = "changed" if last_modified != self.snapshot.get(filename) else "unchanged"
            print(f"{filename}: {status}")

    def real_time_status(self):
        while True:
            time.sleep(5)
            print("\n--- Real-Time Update ---")
            self.status()
            print("------------------------")

# Funcția principală de interacțiune cu utilizatorul
def main():
    folder_path = "/calea/spre/folder"  # Setează calea corectă a folderului
    monitor = DocumentMonitor(folder_path)

    while True:
        command = input("Enter command (commit, info <filename>, status): ").strip().split()
        if not command:
            continue

        action = command[0]
        if action == "commit":
            monitor.commit()
        elif action == "info" and len(command) > 1:
            monitor.info(command[1])
        elif action == "status":
            monitor.status()
        else:
            print("Invalid command.")

# Pornirea monitorizării în timp real într-un thread separat
if __name__ == "__main__":
    print("hiiiiiiiiiii")
    folder_path = "C:\Users\Asus\Desktop\oop\lab_3_oop\yest_my_git"

   
  # Setează calea corectă a folderului
    monitor = DocumentMonitor(folder_path)
    
    # Pornim monitorizarea în timp real într-un thread separat
    threading.Thread(target=monitor.real_time_status, daemon=True).start()

    # Funcția principală pentru interacțiunea cu utilizatorul
    main()