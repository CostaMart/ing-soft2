from model.Domain import Repository
import requests
import subprocess
import os
import sys
import shutil

folder = "repository"

def search_repo(nome_progetto):
    
    # Effettua la ricerca dei repository su GitHub basati sul nome del progetto
    url = f"https://api.github.com/search/repositories?q={nome_progetto}"
    response = requests.get(url)
    risultati = response.json()["items"]

    # Crea una lista di oggetti di tipo Repository
    repositories = []
    for risultato in risultati:
        name = risultato["name"]
        html_url = risultato["html_url"]
        description = risultato["description"]
        repository = Repository(name, html_url, description)
        repositories.append(repository)

    return repositories


def clone_repo(url):
   
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder)
    
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
                    
        except OSError as e:
            print(f"Errore durante la creazione della cartella '{folder}': {e}")
    else:   
        if sys.platform.startswith('win'):
            print("siamo su windowss")
            os.system(f'rmdir /S /Q "{folder}"')
        
        elif sys.platform.startswith('linux'):
            print("siamo su linux")
            shutil.rmtree(folder)   
       
        

    
    subprocess.call(['git', 'clone', url, folder])
    
    


