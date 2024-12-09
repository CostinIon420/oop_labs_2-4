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
        self.snapshot = {} 
        print(f"Using folder path: {self.folder_path}") 
        self.load_files()

    def load_files(self):
        self.files = {}
        

        # Citește fișierele deja urmărite din `untracked_files.txt` și le salvează într-un set
        
        with open("untracked_files.txt", "r") as f:
                untracked_files = set(f.read().splitlines())  # Creează un set pentru verificare rapidă
        with open("tracked.txt", "r") as f:
                tracked_files = set(f.read().splitlines())

        
        for filename in os.listdir(self.folder_path):
                filepath = os.path.join(self.folder_path, filename)
                

                # Verifică dacă fișierul este deja urmărit
                if filename not in untracked_files and filename not in tracked_files :
                    with open("untracked_files.txt", "a") as f:
                        f.write(filename + "\n")
                    untracked_files.add(filename)  # Adaugă fișierul în set pentru a evita duplicatele

                # Încarcă fișierul în `self.files` în funcție de extensie
                if filename.endswith(('.png', '.jpg')):
                    self.files[filename] = ImageFile(filepath)
                if filename.endswith('.txt'):
                    self.files[filename] = TextFile(filepath)
                
                   
                
        

                
        


        

    def commit(self):
        # Actualizează snapshot-ul pentru toate fișierele monitorizate
        self.snapshot = {filename: os.path.getmtime(os.path.join(self.folder_path, filename))
                         for filename in self.files}
        
        with open("untracked_files.txt", 'r') as f:
            with open("tracked.txt", 'a') as f2:
                for linie in f:
                    f2.write(linie)
        print("Snapshot updated.")
        with open("untracked_files.txt", 'w') as f:
            pass


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
        if os.path.getsize("untracked_files.txt"):
            print("new untracked file")    
    def real_time_status(self):
        while True:
            time.sleep(5)
            self.load_files()
            
            

            
   

# Funcția principală de interacțiune cu utilizatorul
def main():

    git_init=False

    init_path = "git_init.txt"

    if os.path.exists(init_path):
        print("Fișierul există.")
        git_init=True
    else:
         git_init=False
         if not git_init:
             print("to start work use comand git init")
             user_comand=input()
             if user_comand=="git init":
                    with open("git_init.txt","a") as f:
                        f.write("git initialized with succes")
                    git_init=True
             else:
               print("command not found")
   
  

    
        
    

    if git_init:    

        folder_path = "C:\Users\Asus\Desktop\oop\lab_3_oop\yest_my_git" # Setează calea corectă a folderului
        monitor = DocumentMonitor(folder_path)
    
        
        while True:
            
            if os.path.getsize("untracked_files.txt"):

                print("untracked files: \n")
                with open("untracked_files.txt", "r") as f:
                    content=f.read()
                    print(f"\033[91m{content}\033[0m")

                print("tracked files:")
                with open("tracked.txt", "r") as f:
                    content=f.read()
                    print(f"\033[92m{content}\033[0m")

                
                print("use comand 'git commit' to track files")
                

                  
            else :
                print("nothing to commit\n")   
                print("tracked files:")
                with open("tracked.txt", "r") as f:
                    content=f.read()
                    print(f"\033[92m{content}\033[0m")   

            
                

            
            if os.path.getsize("tracked.txt"):
                command = input("Enter command ( info <filename>, status): ").strip().split()
                

                action = command[0]
                
                if action == "commit":
                     monitor.commit()
                if action == "info" and len(command) > 1:
                    monitor.info(command[1])
                elif action == "status":
                    monitor.status()
                else:
                    print("Invalid command.")
if __name__ == "__main__":

    folder_path="C:\Users\Asus\Desktop\oop\lab_3_oop\yest_my_git"
    monitor = DocumentMonitor(folder_path)
    threading.Thread(target=monitor.real_time_status, daemon=True).start()
  
    main()
