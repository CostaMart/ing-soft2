import os
import pandas as pd
import json
from pydriller import Repository
import subprocess
import shutil


setting = open("settings.json")
settings = json.load(setting)
remote_repo = settings['repo']
folder = "Repository"



def check_repo():
#   Metodo che controlla se il progetto da analizzare è presente
    if os.path.exists(folder):
        content = os.listdir(folder)
        if content is not None:
            return 0
    else:
        clone_repo()



def check_folder():
    # Metodo che controlla se la cartella di output è presente
    if not os.path.exists("output"):
        path = os.path.join("output")
        os.mkdir(path)



def clone_repo():
    # Metodo che effettua il clone di un repository target.
    subprocess.call(['git', 'clone', remote_repo, folder])



def print_current_branch(repository):
    # Metodo che mostra il nome del branch attivo
    print(repository.active_branch)



def repo_to_use():
    # Metodo che restituisce un oggetto Repository
    return Repository(folder) 



def get_commits(repository):
    # Metodo che restituisce tutti i commit di una Repository
    return repository.traverse_commits()



def dataCommit():
    # Metodo che prende tutti i commit con relativa data e li inserisce in un dataframe che ritorna
    commit_data=[]
    for commit in get_commits(repo_to_use()):
        commit_hash = commit.hash
        commit_date = commit.committer_date
        commit_data.append({'Titolo del Commit': commit_hash, 'Data del Commit': commit_date})
    return pd.DataFrame(commit_data)



def dataCommitLink(rep):
    # Metodo che prende tutti i commit con relativa data e li inserisce in un dataframe che ritorna
    commit_data=[]
    for commit in get_commits(rep):
        commit_hash = commit.hash
        commit_date = commit.committer_date
        commit_data.append({'Titolo del Commit': commit_hash, 'Data del Commit': commit_date})
    return pd.DataFrame(commit_data)



def delete_garbage(keep, output=None):

    # Elimina i file non utilizzabili creati con le metriche della classe
    if(output is None):
        output_dir = os.path.abspath("output")
    else:
        output_dir = os.path.abspath("output")+"\\"+str(output)
    for filename in os.listdir(output_dir):
        if not keep in filename:
            os.remove(output_dir+"\\"+filename)
    
    # for filename in os.listdir(output):
    #     df = pd.read_csv(filename, sep=",")
    #     if df.empty:
    #         os.remove(filename)



def refresh():
    directory = os.path.abspath("output")
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)



def trova_file_classe(classe_filename):
    repository_path = os.path.abspath("Repository")
    for root, dirs, files in os.walk(repository_path):
        if classe_filename in files:
            return os.path.join(root, classe_filename)
    return None

