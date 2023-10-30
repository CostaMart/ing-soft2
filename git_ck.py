import subprocess
import os
from git import Repo 
import repo_utils as ru
import pandas as pd
from multiprocessing import Pool


def ck_metrics_for_single_commit(commit_hash, output = None):
    # Questo metodo estrae le metriche del commit scelto
    repo_to_analyze = os.path.abspath('Repository')
    ck_tool = os.path.abspath('ck.jar')
    if (output is not None):
        output_dir = os.path.abspath("output") +"\\" +output
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.path.abspath("output")
    os.chdir(repo_to_analyze)
    subprocess.call(['git', 'checkout', '-f', commit_hash])
    os.chdir(os.path.dirname(ck_tool))
    subprocess.call(['java', '-jar', 'ck.jar', repo_to_analyze, 'true', '0', 'false', f"{output_dir}/{commit_hash}"])
    # ru.delete_garbage("class")
    # Non ritorna nulla ma crea il file csv con metriche per il commit richiesto
    


def commit_measure_for_single_commit(measures, commit_hash):
    # Questo metodo estrae dal commit la metrica o le metriche desiderate
    dir = os.path.abspath("output")+"\\"+commit_hash+"class.csv"
    df = pd.read_csv(dir)
    for measure in measures:
        if measure not in df.columns:
            print(f"Metrica '{measure}' non trovata nel file CSV.")
            return None

    # Seleziona solo le colonne "class" e le metrica specificate
    selected_columns = df[["class"] + measures]

    return selected_columns



def commit_measure_avg(measure, commit_hash, output =None): 
    # Questo metodo estrae la media della metrica desiderata dal commit
    if(output is None):
        dir = os.path.abspath("output")+"\\"+commit_hash
    else:
        dir = os.path.abspath("output")+"\\"+output+"\\"+commit_hash
    df = pd.read_csv(dir)
    if measure not in df.columns:
        print(f"Metrica '{measure}' non trovata nel file CSV.")
        return None

    # Calcola la media della metrica specificata
    mean_value = df[measure].mean()

    return mean_value



######   DEPRECATO  ######


# def commit_measure_avg_year(year, measure, commit_hash): 
#     # Questo metodo estrae la media della metrica desiderata dal commit
#     dir = os.path.abspath("output")+"\\"+str(year)+"\\"+commit_hash
#     df = pd.read_csv(dir)
#     if measure not in df.columns:
#         print(f"Metrica '{measure}' non trovata nel file CSV.")
#         return None

#     # Calcola la media della metrica specificata
#     mean_value = df[measure].mean()

#     return mean_value



def commit_for_year(year):
    # Questo metodo estrae le metriche dei commit per l'anno inserito
    repo_to_analyze = os.path.abspath('Repository')
    selected_commits = []
    
    for commit in Repo(repo_to_analyze).iter_commits():
        if commit.committed_datetime.year == year:
            selected_commits.append(commit)

    # Itera sui commit selezionati e calcola le metriche
    for commit in selected_commits:
        commit_hash = commit.hexsha
        ck_metrics_for_single_commit(commit_hash, str(year))
    ru.delete_garbage("class", str(year))




def commit_measure_year(year, measure):
    commit_for_year(year)
    result_data = []
    path = os.path.abspath("output")+"\\"+str(year)
    element_names = os.listdir(path)
    for name in element_names:
        result_data.append({"name": name, "avg": commit_measure_avg(measure, name, str(year))})
    result_df = pd.DataFrame(result_data)
    return result_df



def commit_for_IntYear(start_year, end_year):
    repo_to_analyze = os.path.abspath('Repository')
    repo = Repo(repo_to_analyze)
    
    selected_commits = []
    for commit in repo.iter_commits():
        commit_date = commit.committed_datetime
        if start_year <= commit_date.year <= end_year :
            selected_commits.append(commit)

    for commit in selected_commits:
            commit_hash = commit.hexsha
            ck_metrics_for_single_commit(commit_hash)
            ru.delete_garbage("class")


def analyze_commits_for_release(repo_owner, repo_name, release_tag):
    """Metodo per analizzare le metriche dei commit per release ipotizziamo che il repository
    è già scaricato"""
    commits = ReturnReleaseProject.get_commits_for_release(repo_owner, repo_name, release_tag)

    if commits:
        for commit in commits:
            commit_hash = commit.sha
            ck_metrics_for_single_commit(commit_hash)
    else:
        print("Nessun commit disponibile per il tag di rilascio specificato.")
