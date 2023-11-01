from model import Domain
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
       
        

    
    return subprocess.call(['git', 'clone', url, folder])
    

def get_all_release_tag_repo(owner, repo_name):
    """Metodo che ritorna tutte le  releases di uno specifico progetto"""
    url = f"https://api.github.com/repos/{owner}/{repo_name}/releases"
    response = requests.get(url)

    if response.status_code == 200:
        releases = response.json()
        # Estrai solo i tag delle release dalla lista di release
        release_tags = [release['tag_name'] for release in releases]
        return release_tags
    else:
        print(f"Errore {response.status_code}: Impossibile ottenere le release del progetto.")
        return None


def get_repository_metadata(owner, repo_name):
    """metodo che ritorna tutti i metadati di un progetto github"""
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = requests.get(api_url)

    if response.status_code == 200:
        repository_data = response.json()
        repository = Domain.MetadataRepository(repository_data)
        return repository
    else:
        print(f"Errore: Impossibile ottenere i dati del repository. Codice di stato: {response.status_code}")
        return None

