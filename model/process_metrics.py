import git
import os
import model.repo_utils as ru
import pygit2
import subprocess
import datetime
import math
import pandas as pd
import chardet


def controlla_numero_revisioni_per_classe(classe_filename, folder = "repository"):
    """Metodo che dato il nome di una classe ne calcola il numero di revisioni"""
    repository_path = os.path.abspath(folder)
    classe_file_path = ru.trova_file_classe(classe_filename)
    # print(classe_file_path)
    if classe_file_path is None:
        return 0 

    repo = git.Repo(repository_path)
    numero_revisioni = 0

    for commit in repo.iter_commits(paths=classe_file_path):
        numero_revisioni += 1

    return numero_revisioni



def controlla_numero_revisioni_per_repo(folder = "repository"):
    """Metodo che calcola il numero di revisioni per repository"""
    list = ru.cerca_file_java(folder)
    class_data = []
    for element in list:
        class_data.append({'Nome della Classe': element, 'Numero di Revisioni': controlla_numero_revisioni_per_classe(element)})
    return pd.DataFrame(class_data)



def calcola_numero_bug_fix(folder ="repository"):
    """Metodo che calcola i bug fix di un progetto se documentati """
    repository_path = os.path.abspath(folder)
    repo = git.Repo(repository_path)
    numero_bug_fix = 0

    for commit in repo.iter_commits():
        if 'fix' in commit.message.lower():
            numero_bug_fix += 1

    return numero_bug_fix



def calcola_code_churn(commit_hash1, commit_hash2, folder="repository"):
    """Metodo che calcola i code churn tra 2 commit, praticamente le linee modificate """
    repository_path = os.path.abspath(folder)
    repo = pygit2.Repository(repository_path)
    code_churn = 0

    commit1 = repo.revparse_single(commit_hash1)
    commit2 = repo.revparse_single(commit_hash2)

    for patch in repo.diff(commit1, commit2):
        code_churn += patch.line_stats[1]  # Linee rimosse
        code_churn += patch.line_stats[2]  # Linee aggiunte

    return code_churn



def calcola_loc(classe_filename):
    """Questo metodo calcola le misure LOC di un codice restituendo il 
       numero di linee di codice il numero di linee vuote e il numero di commenti"""
    classe_file_path = ru.trova_file_classe(classe_filename)
    with open(classe_file_path, 'rb') as raw_file:
        raw_data = raw_file.read()
        encoding_info = chardet.detect(raw_data)
        file_encoding = encoding_info['encoding']
    
    # Verifica la codifica rilevata
    if file_encoding is None:
        file_encoding = 'utf-8'  # Imposta una codifica predefinita se non può essere rilevata
    # print(file_encoding)
    with open(classe_file_path, 'r', encoding=file_encoding) as file:
        linee_di_codice = 0
        linee_vuote = 0
        commenti = 0

        for linea in file:
            linea = linea.strip()
            if not linea:
                linee_vuote += 1
            elif linea.startswith('#') or linea.startswith('//') or linea.startswith('*') or linea.startswith('*/') or linea.startswith('/*') or linea.startswith('"""') or linea.endswith('"""'):
                commenti += 1
            else:
                linee_di_codice += 1

        return linee_di_codice, linee_vuote, commenti
    


def calcola_loc_repo(folder="repository"):
    """Calcola il LOC per una lista di classi di un commit e restituisce un DataFrame."""
    risultati = []
    classi = ru.cerca_file_java(folder)
    for classe in classi:
        loc_result = calcola_loc(classe)  # Usa il tuo metodo calcola_loc
        nome_classe = classe.split("/")[-1]  # Estrarre solo il nome della classe
        risultati.append([nome_classe, loc_result[0], loc_result[1], loc_result[2]])

    # Creare un DataFrame con i risultati
    df = pd.DataFrame(risultati, columns=["Nome della Classe", "Linee di Codice", "Linee Vuote", "Commenti"])
    
    return df



def calcola_autori_distinti_per_file(file_name, folder="repository"):
    """Questo metodo calcola il numero di autori distinti per file e ne restituisce una lista di nomi"""
    file_path = ru.trova_file_classe(file_name)
    repository_path = os.path.abspath(folder)

    # Esegui il comando Git per ottenere gli autori
    git_command = ['git', 'log', '--format="%an"', '--follow', file_path]
    output = subprocess.check_output(git_command, cwd=repository_path)

    # Rileva la codifica dell'output
    encoding_info = chardet.detect(output)
    output_encoding = encoding_info['encoding']
    # print(encoding_info)
    # Verifica la codifica rilevata
    if output_encoding is None:
        output_encoding = 'utf-8'  # Imposta una codifica predefinita se non può essere rilevata

    # Decodifica l'output con la codifica corretta
    decoded_output = output.decode(output_encoding)

    autori_distinti = set()
    lines = decoded_output.split('\n')
    for line in lines:
        autore = line.strip('"\n')  # Rimuovi i caratteri di citazione e newline
        autori_distinti.add(autore)

    return autori_distinti



def calcola_autori_distinti_per_repo(folder = "repository"):
    """Metodo che calcola e restituisce gli autori distinti che hanno modificato un file"""
    list = ru.cerca_file_java(folder)
    class_data = []
    for element in list:
        class_data.append({'Nome della Classe': element, 'Autori': calcola_autori_distinti_per_file(element)})
    return pd.DataFrame(class_data)



def calcola_settimane_file(class_name, folder = "repository"):
    """Questo metodo calcola l'età del file richiesto in settimane"""
    repository_path = os.path.abspath(folder)
    file_path = ru.trova_file_classe(class_name)
    git_command = f'git log --diff-filter=A --format=%ct -- "{file_path}"'
    result = subprocess.check_output(git_command, cwd=repository_path, shell=True).decode().strip()

    if not result:
        return None 
    timestamps = result.split('\n')

    # Prendi solo la prima parte del timestamp (ignorando il timestamp doppio se presente)
    first_timestamp = timestamps[0]

    # Converti il timestamp in un intero
    file_creation_timestamp = int(first_timestamp)
    file_creation_date = datetime.datetime.utcfromtimestamp(file_creation_timestamp)

    current_time = datetime.datetime.now()
    time_difference = current_time - file_creation_date

    # Calcola il numero di giorni
    return math.ceil(time_difference.days/7)



def calcola_settimane_repo(folder = "repository"):
    """Questo metodo calcola l'età in settimane di tutti i file in una repository"""
    list = ru.cerca_file_java(folder)
    class_data = []
    for element in list:
        class_data.append({'Nome della Classe': element, 'Settimane file': calcola_settimane_file(element)})
    return pd.DataFrame(class_data)