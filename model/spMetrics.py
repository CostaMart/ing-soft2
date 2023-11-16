import model.process_metrics as pm
import model.repo_utils as ru
import pandas as pd
import model.git_ck as ck
import subprocess
import os


def generate_process_metrics(nome_classe, commits_dict, folder = "repository"):
    """Genera le metriche di processo, è possibile specificare il commit da analizzare e il folder dove è conservata la repository"""
    """Questo metodo dovrà essere utilizzato per fare tutte le analisi disponibili con le metriche di processo, a parte i code churn"""
    latest_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=os.path.abspath(folder), text=True).strip()
    df_filtrato = pd.DataFrame(list(commits_dict.items()), columns=['Commit Hash', 'Data del Commit'])
    df_filtrato['Data del Commit'] = df_filtrato['Data del Commit'].apply(lambda x: x['date'])
    hash1 = df_filtrato["Commit Hash"][0]
    df_finale= pd.DataFrame(columns=['Commit hash', 'Data del Commit', 'Numero di Revisioni', 'Linee di Codice', 'Linee vuote', 'Commenti', 'Autori Distinti', 'Settimane file', 'Bugfix commit', 'Code churn'])
    for index, element in enumerate(df_filtrato["Commit Hash"]):
        ru.checkout_commit(element)
        nr = pm.controlla_numero_revisioni_per_classe(nome_classe, folder)
        rig, rigv, com = pm.calcola_loc(nome_classe, folder)
        ad = pm.calcola_autori_distinti_per_file(nome_classe, folder)
        sf = pm.calcola_settimane_file(nome_classe, folder)
        bf = pm.calcola_numero_bug_fix(folder)
        cc = pm.calcola_code_churn(hash1, element, folder)
               
        temp_df = pd.DataFrame({'Commit hash': element,
                                'Data del Commit': df_filtrato.loc[index, 'Data del Commit'],  
                                'Numero di Revisioni': nr,
                                'Linee di Codice': rig,
                                'Linee vuote': rigv,
                                'Commenti': com,
                                'Autori Distinti': [ad],
                                'Settimane file': sf,
                                'Bugfix commit': bf,
                                'Code churn': cc}, index=[0])
        df_finale = pd.concat([df_finale, temp_df], ignore_index=True)
        # df_finale['Data del Commit'] = pd.to_datetime(df_finale['Data del Commit'])
        # df_finale['Data del Commit'] = df_finale['Data del Commit'].dt.strftime('%Y-%m-%d %H:%M:%S')
    ru.checkout_commit(latest_commit_hash)
    return df_finale





def generate_metrics_ck(commits_dict, folder = "repository", measures =["cbo", "wmc", "dit", "noc", "rfc", "lcom"]):
    """Genera le metriche ad oggetti , questo metodo prende la release da cui si vuole partire(opzionale), trova i commit e li inserisce in un dataframe"""
    """Poi li filtra dal commit dopo la release precedente, alla release scelta e ritorna il primo dataframe filtrato,"""
    """Una volta richiamato il metodo, se gli si passa il dataframe e i due hash per cui si vuole avere l'intervallo di analisi, filtra di nuovo il df e analizza"""
    latest_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=os.path.abspath(folder), text=True).strip()
    df_filtrato = pd.DataFrame(list(commits_dict.items()), columns=['Commit Hash', 'Data del Commit'])
    df_filtrato['Data del Commit'] = df_filtrato['Data del Commit'].apply(lambda x: x['date'])
    commit=ck.commit_measure_interval(measures, df_filtrato, folder)
    if(commit.empty): 
        print("Non ci sono commit disponibili")
        ru.checkout_commit(latest_commit_hash)
        return 0
    ru.checkout_commit(latest_commit_hash)
    return commit





