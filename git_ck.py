import subprocess
import os
from git import Repo 
import repo_utils as ru
import pandas as pd
from multiprocessing import Pool

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
    subprocess.call(['java', '-jar', 'ck.jar', repo_to_analyze, 'true', '0', 'true', f"{output_dir}/{commit_hash}"])
    # ru.delete_garbage("class")
    # Non ritorna nulla ma crea il file csv con metriche per il commit richiesto



def commit_measure(measures, commit_hash):
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



def commit_measure_avg(measure, commit_hash): 
    # Questo metodo estrae la media della metrica desiderata dal commit
    dir = os.path.abspath("output")+"\\"+commit_hash
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
    output_dir = os.path.abspath('output')

    selected_commits = []
    for commit in Repo(repo_to_analyze).iter_commits():
        if commit.committed_datetime.year == year:
            selected_commits.append(commit)

    # Itera sui commit selezionati e calcola le metriche
    for commit in selected_commits:
        commit_hash = commit.hexsha
        file_name = os.path.join(output_dir, f"{year}_{commit_hash}.csv")
        ck_metrics_for_single_commit(commit_hash)
        ru.delete_garbage("class")




def commit_measure_year(year, measure):
    # commit_for_year(year)
    result_data = []
    path = os.path.abspath("output")
    element_names = os.listdir(path)
    for name in element_names:
        result_data.append({"name": name, "avg": commit_measure_avg(measure, name)})
    result_df = pd.DataFrame(result_data)
    return result_df



def process_commit(commit):
    # Metodo che serve solo per dividere i processi
    commit_hash = commit.hexsha
    ck_metrics_for_single_commit(commit_hash)



def commit_for_yearConc(year):
    # Metodo che serve a calcolare le metriche per commit annuali in maiera concorrente su tutti i core
    repo_to_analyze = os.path.abspath('Repository')
    
    selected_commits = []
    for commit in Repo(repo_to_analyze).iter_commits():
        if commit.committed_datetime.year == year:
            selected_commits.append(commit)

    # Create a Pool of worker processes
    with Pool() as pool:
        pool.map(process_commit, selected_commits)
    ru.delete_garbage("class")
