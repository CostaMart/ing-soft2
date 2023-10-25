from pydriller import Repository
import subprocess
import json
import os
import pandas as pd
from git import Repo 


setting = open("settings.json")
settings = json.load(setting)
remote_repo = settings['repo']

local_repo_path = "Repository"

def clone_repo():
    # Metodo che effettua il clone di un repository target.
    subprocess.call(['git', 'clone', remote_repo, local_repo_path])

def print_current_branch(repository):
    # Metodo che mostra il nome del branch attivo
    print(repository.active_branch)

def repo_to_use():
    # Metodo che restituisce un oggetto Repository
    return Repository(local_repo_path) 

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



def delete_garbage(keep):
    # Elimina i file non utilizzabili creati con le metriche della classe
    for filename in os.listdir("output"):
        if not keep in filename:
            os.remove("output/"+filename)
    
    for filename in os.listdir("output"):
        df = pd.read_csv("output/"+filename, sep=",")
        if df.empty:
            os.remove("output/"+filename)



def ck_metrics_for_single_commit(commit_hash):
    # Questo metodo estrae le metriche del commit scelto
    repo_to_analyze = os.path.abspath('Repository')
    ck_tool = os.path.abspath('ck.jar')
    output_dir = os.path.abspath('output') 

    os.chdir(repo_to_analyze)

    # Verifica se il commit esiste nella repository
    try:
        repo = Repo(repo_to_analyze)
        repo.commit(commit_hash)
    except:
        print(f"Il commit con hash: {commit_hash} non è stato trovato nella repository.")
        return
    
    # Effettua il checkout del commit
    subprocess.call(['git', 'checkout', '-f', commit_hash])
    os.chdir(os.path.dirname(ck_tool))
    subprocess.call(['java', '-jar', 'ck.jar', repo_to_analyze, 'false', '0', 'true', f"{output_dir}/{commit_hash}"])
    delete_garbage(keep="class")
