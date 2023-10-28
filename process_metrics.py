import git
import os
import repo_utils as ru
import pygit2
import re


def controlla_numero_revisioni_per_classe(classe_filename):
    # Metodo che dato il nome di una classe ne calcola il numero di revisioni
    repository_path = os.path.abspath('Repository')
    classe_file_path = ru.trova_file_classe(classe_filename)

    if classe_file_path is None:
        return 0  # Il file della classe non è stato trovato nel repository

    repo = git.Repo(repository_path)
    numero_revisioni = 0

    for commit in repo.iter_commits(paths=classe_file_path):
        numero_revisioni += 1

    return numero_revisioni



def calcola_numero_bug_fix():
    # Metodo che calcola i bug fix di un progetto se documentati 
    repository_path = os.path.abspath('Repository')
    repo = git.Repo(repository_path)
    numero_bug_fix = 0

    for commit in repo.iter_commits():
        if 'fix' in commit.message.lower():
            numero_bug_fix += 1

    return numero_bug_fix



def calcola_code_churn(commit_hash1, commit_hash2):
    # Metodo che calcola i code churn tra 2 commit, praticamente le linee modificate 
    repository_path = os.path.abspath('Repository')
    repo = pygit2.Repository(repository_path)
    code_churn = 0

    commit1 = repo.revparse_single(commit_hash1)
    commit2 = repo.revparse_single(commit_hash2)

    for patch in repo.diff(commit1, commit2):
        code_churn += patch.line_stats[1]  # Linee rimosse
        code_churn += patch.line_stats[2]  # Linee aggiunte

    return code_churn


