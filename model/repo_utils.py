import os
import pandas as pd
import json
from pydriller import Repository
import subprocess
import urllib.parse
from icecream import ic

setting = open("settings.json")
settings = json.load(setting)
remote_repo = settings['repo']



def check_repo(folder = "repository"):
    """Metodo che controlla se il progetto da analizzare è presente"""
    if os.path.exists(folder):
        content = os.listdir(folder)
        if content is not None:
            return 0
    else:
        clone_repo()



def check_folder(folder = "output"):
    """Metodo che controlla se la cartella di output è presente"""
    if not os.path.exists(folder):
        path = os.path.join(folder)
        os.mkdir(path)



def clone_repo(folder = "repository"):
    """Metodo che effettua il clone di un repository target"""
    subprocess.call(['git', 'clone', remote_repo, folder])
    


def clone_git_repository_with_tag(tag):
    """Questo metodo clona una repository con il tag specificato"""
    try:
        subprocess.run(['git', 'clone', '-b', tag, remote_repo], check=True)
        print(f"Repository clonata con successo utilizzando il tag {tag}.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il clone: {e.stderr}")



def get_commit_hash_for_tag(tag, folder = "repository"):
    try:
        repository_path=os.path.abspath(folder)
        # Esegui il comando 'git rev-list' per ottenere l'hash del commit associato al tag
        result = subprocess.run(['git', 'rev-list', '-n', '1', tag], cwd=repository_path, capture_output=True, text=True, check=True)
        commit_hash = result.stdout.strip()
        return commit_hash
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'ottenere l'hash del commit per il tag {tag}: {e.stderr}")
        return None
    


def print_current_branch(repository):
    """Metodo che mostra il nome del branch attivo"""
    print(repository.active_branch)



def repo_to_use(folder = "repository"):
    """Metodo che restituisce un oggetto Repository"""
    return Repository(folder) 



def get_commits(repository):
    """Metodo che restituisce tutti i commit di una Repository"""
    return repository.traverse_commits()



def dataCommit():
    """Metodo che prende tutti i commit con relativa data e li inserisce in un dataframe che ritorna"""
    commit_data=[]
    for commit in get_commits(repo_to_use()):
        commit_hash = commit.hash
        commit_date = commit.committer_date
        commit_data.append({'Titolo del Commit': commit_hash, 'Data del Commit': commit_date})
    return pd.DataFrame(commit_data)



def dataCommitLink(rep):
    """Metodo che prende tutti i commit con relativa data e li inserisce in un dataframe che ritorna"""
    commit_data=[]
    for commit in get_commits(rep):
        commit_hash = commit.hash
        commit_date = commit.committer_date
        commit_data.append({'Commit Hash': commit_hash, 'Data del Commit': commit_date})
    return pd.DataFrame(commit_data)



def delete_garbage(keep, output=None, folder = "output"):
    """Elimina i file non utilizzabili creati con le metriche della classe"""
    if(output is None):
        output_dir = os.path.abspath(folder)
    else:
        output_dir = os.path.abspath("output")+"\\"+str(output)
    for filename in os.listdir(output_dir):
        if not keep in filename:
            os.remove(output_dir+"\\"+filename)



def trova_file_classe(classe_filename, folder = "repository"):
    """ Questo metodo trova una classe in una repository e ne ritorna il path assoluto """
    repository_path = os.path.abspath(folder)
    for root, dirs, files in os.walk(repository_path):
        if classe_filename in files:
            return os.path.join(root, classe_filename)
    return None



def cerca_file_java(cartella_name):
    """ Questo metodo cerca tutti i file java in una cartella e ne restituisce una lista di nomi di file """
    risultati = []
    cartella = os.path.abspath(cartella_name)
    
    for root, dirs, files in os.walk(cartella):
        for file in files:
            if file.endswith(".java"):
                risultati.append(file)

    return risultati



def get_git_tags(folder = None):
    """Questo metodo restituisce i tag di una repository"""
    if folder != None:
        repo_path = os.path.abspath(folder)+"\\.git"
    
  
     
    try:
        result = subprocess.run(['git', '--git-dir', repo_path, 'tag'], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Il comando eseguito
            output = result.stdout
            tags = output.split('\n')
            return [tag for tag in tags if tag]  # Rimuovi eventuali tag vuoti
        else:
            print("Errore nell'esecuzione del comando 'git tag':", result.stderr)
            return []
    except subprocess.CalledProcessError as e:
        print("Errore nell'esecuzione del comando 'git tag':", e.stderr)
        return []
    


def get_commit_date(commit_hash, folder = "repository"):
    """Questo metodo restituisce la data del commit richiesto"""
    try:
        result = subprocess.run(['git', 'show', '--format=%aI', '-s', commit_hash], cwd=os.path.abspath(folder), capture_output=True, text=True, check=True)
        commit_date = result.stdout.strip()
        return commit_date
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'ottenere la data del commit {commit_hash}: {e.stderr}")
        return None



def get_git_tags_commit(folder = "repository"):
    """Questo metodo ottiene la lista dei tag e li inserisce in un dataframe con il commit specifico che ha creato il tag e la data del commit"""
    tags = get_git_tags(folder)
    
    data = []
    
    for tag in tags:
        commit_hash = get_commit_hash_for_tag(tag, folder)
        
        if commit_hash:
            commit_date = get_commit_date(commit_hash, folder)
            data.append({'Tag': tag, 'Commit Hash': commit_hash, 'Commit Date': commit_date})
    
    df = pd.DataFrame(data)
    
    return df



def checkout_tag(tag=None, folder = "repository"):
    """Questo metodo prende il tag come parametro e fa il checkout"""
    if(tag != None):
        if(folder == "repository"):
            checkout_commit(get_commit_hash_for_tag(tag))
        else:
            checkout_commit(get_commit_hash_for_tag(tag, folder), folder)
    




def checkout_commit(commit_hash, folder = "repository"):
    """Questo metodo effettua il checkout a un commit specifico"""
    try:
        subprocess.run(['git', 'checkout', commit_hash], cwd=os.path.abspath(folder), check=True)
        print(f"Checkout effettuato con successo al commit {commit_hash}.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il checkout al commit {commit_hash}: {e.stderr}")



def inizia_analisi(tag = None, folder = "repository"):
    """Questo metodo prepara il processo alle operazioni da effettuare"""
    if(tag is not None):
        checkout_tag(tag, folder)
    repo = repo_to_use(folder)
    return dataCommitLink(repo)



def sfoglia_commit(df, index = 0):
    """Questo metodo richiede il dataframe ritornato dall'inizializzazione e sfoglia i commit 10 alla volta sulla base dell'indice passato"""
    if index >= df.shape[0]:
        return pd.DataFrame()
    check_folder()
    start_index = index
    end_index = min(index + 10, df.shape[0])
    subset_df = df.iloc[start_index:end_index]
    return subset_df
        

    

