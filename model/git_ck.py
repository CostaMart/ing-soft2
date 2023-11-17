import subprocess
import os
from git import Repo 
import model.repo_utils as ru
import pandas as pd
from multiprocessing import Pool


def ck_metrics_for_single_commit(commit_hash, output = None, folder = "repository"):
    """Questo metodo estrae le metriche del commit scelto
    Utilizzato per fare analisi su commit singoli
    Utilizzato per fare analisi su commit in maniera iterativa per le richieste di metriche per intervallo"""
    partenza = os.getcwd()
    repo_to_analyze = os.path.abspath(folder)
    ck_tool = os.path.abspath('ck.jar')
    if (output is not None):
        output_dir = os.path.abspath("output") +"\\" +output
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.path.abspath("output")
    file_name = commit_hash + "class.csv"
    file_path = os.path.join(output_dir, file_name)
    if not os.path.exists(file_path):
        os.chdir(repo_to_analyze)
        subprocess.call(['git', 'checkout', '-f', commit_hash])
        os.chdir(os.path.dirname(ck_tool))
        subprocess.call(['java', '-jar', 'ck.jar', repo_to_analyze, 'true', '0', 'false', f"{output_dir}/{commit_hash}"])
        if(output is not None):
            ru.delete_garbage("class", output)
            os.chdir(partenza)
    # Non ritorna nulla ma crea il file csv con metriche per il commit richiesto
    


def commit_measure_for_single_commit(measures, commit_hash):
    """Questo metodo estrae dal commit la metrica o le metriche desiderate"""
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
    """Questo metodo estrae la media della metrica desiderata dal commit"""
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



def analyze_commits_for_interval(df, folder = "repository"):
    """Questo metodo estrae i commit corrispondenti all'intervallo scelto e li analizza"""
    commits = df
    if(commits.empty):
        return pd.DataFrame()
    if not commits.empty:  # Controlla se il DataFrame non è vuoto
        commit_messages = commits.iloc[:, 0] 
        for commit_message in commit_messages:

            ck_metrics_for_single_commit(commit_message, folder = folder)
        ru.delete_garbage("class")
        return commits
    else:
        print("Nessun commit disponibile per il tag di rilascio specificato.")



def commit_measure_interval(measures, df, folder = "repository"):
    """ Questo metodo calcola le metriche per l'intervallo e fa la media delle metriche richieste per ogni commit"""
    commit = analyze_commits_for_interval(df, folder)
    if(commit.empty):
        return pd.DataFrame
    commit['Commit Hash'] = commit['Commit Hash'] + 'class.csv'
    result_data = []
    path = os.path.abspath("output")
    element_names = os.listdir(path)
    
    for name in element_names:
        metric_averages = {}
        for measure in measures:
            metric_averages[measure] = commit_measure_avg(measure, name)
        result_data.append({"Commit Hash": name, **metric_averages})
    result_df = pd.DataFrame(result_data)
    result = commit.merge(result_df, on ="Commit Hash")
    return result








