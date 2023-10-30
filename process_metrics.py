import git
import os
import repo_utils as ru
import pygit2
import subprocess
import datetime
import math


def controlla_numero_revisioni_per_classe(classe_filename):
    """Metodo che dato il nome di una classe ne calcola il numero di revisioni"""
    repository_path = os.path.abspath('Repository')
    classe_file_path = ru.trova_file_classe(classe_filename)

    if classe_file_path is None:
        return 0 

    repo = git.Repo(repository_path)
    numero_revisioni = 0

    for commit in repo.iter_commits(paths=classe_file_path):
        numero_revisioni += 1

    return numero_revisioni



def calcola_numero_bug_fix():
    """Metodo che calcola i bug fix di un progetto se documentati """
    repository_path = os.path.abspath('Repository')
    repo = git.Repo(repository_path)
    numero_bug_fix = 0

    for commit in repo.iter_commits():
        if 'fix' in commit.message.lower():
            numero_bug_fix += 1

    return numero_bug_fix



def calcola_code_churn(commit_hash1, commit_hash2):
    """Metodo che calcola i code churn tra 2 commit, praticamente le linee modificate """
    repository_path = os.path.abspath('Repository')
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
    with open(classe_file_path, 'r') as file:
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



def calcola_autori_distinti_per_file(file_name):
    """Questo metodo calcola il numero di autori distinti per file e ne restituisce una lista di nomi"""
    file_path = ru.trova_file_classe(file_name)
    repository_path = os.path.abspath('Repository')
    result = subprocess.check_output(['git', 'log', '--format="%an"', '--follow', file_path], cwd=repository_path, shell=True, text=True)

    autori_distinti = set()
    lines = result.split('\n')

    for line in lines:
        autore = line.strip('"')
        if autore:
            autori_distinti.add(autore)

    return autori_distinti



def calcola_settimane_file(class_name):
    """Questo metodo calcola l'età del file richiesto in settimane"""
    repository_path = os.path.abspath('Repository')
    file_path = ru.trova_file_classe(class_name)
    git_command = f'git log --diff-filter=A --format=%ct -- {file_path}'
    result = subprocess.check_output(git_command, cwd=repository_path, shell=True).decode('utf-8').strip()

    if not result:
        return None 

    file_creation_timestamp = int(result)
    file_creation_date = datetime.datetime.utcfromtimestamp(file_creation_timestamp)

    current_time = datetime.datetime.now()

    time_difference = current_time - file_creation_date

    weeks = time_difference.days / 7
    weeks_true= math.floor(weeks)
    return weeks_true