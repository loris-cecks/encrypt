import subprocess
import os
import keyring

def create_encrypted_archive(subfolder, password, split, delete_source):
    archive_name = f"{os.path.basename(subfolder)}.7z"
    command = [
        "C:\\Program Files\\7-Zip\\7z.exe", "a",
        "-p" + password,
        "-mhe=on",
        "-mx0"
    ]
    
    if split:
        command.append("-v1900m")
    
    if delete_source:
        command.append("-sdel")
    
    command.extend([archive_name, subfolder])
    
    subprocess.run(command, check=True)

def main():
    password = input('Inserisci la password: ')
    keyring.set_password('7z_archives', 'user', password)
    
    split_choice = input('Vuoi suddividere gli archivi in parti da massimo 1900 megabyte? (s/N): ')
    split = split_choice.strip().lower() == 's'
    
    delete_source_choice = input('Vuoi eliminare i file sorgente dopo l\'archiviazione? (s/N): ')
    delete_source = delete_source_choice.strip().lower() == 's'
    
    current_folder = os.getcwd()
    for item in os.listdir(current_folder):
        item_path = os.path.join(current_folder, item)
        if os.path.isdir(item_path):
            create_encrypted_archive(item_path, password, split, delete_source)
    
    # Elimina la password dal keyring al termine
    keyring.delete_password('7z_archives', 'user')

if __name__ == "__main__":
    main()
