import model.process_metrics as pm
import model.repo_utils as ru
import pandas as pd
import model.git_ck as ck

# def generate_process_metrics(hash_code=None, folder = "repository"):
#     """Genera le metriche di processo, è possibile specificare il commit da analizzare e il folder dove è conservata la repository"""
#     """Questo metodo dovrà essere utilizzato per fare tutte le analisi disponibili con le metriche di processo, a parte i code churn"""
#     if(hash_code is not None):
#         ru.checkout_commit(hash_code)
    
#     if(folder != "repository"):
#         nr = pm.controlla_numero_revisioni_per_repo(folder)
#         lc = pm.calcola_loc_repo(folder)
#         ad = pm.calcola_autori_distinti_per_repo(folder)
#         sf = pm.calcola_settimane_repo(folder)
#     else:
#         nr = pm.controlla_numero_revisioni_per_repo()
#         lc = pm.calcola_loc_repo()
#         ad = pm.calcola_autori_distinti_per_repo()
#         sf = pm.calcola_settimane_repo()
#     result = nr.merge(lc, on='Nome della Classe').merge(ad, on='Nome della Classe').merge(sf, on='Nome della Classe')
#     bf = pm.calcola_numero_bug_fix()
#     resultDF = pd.DataFrame(result)
#     return resultDF, bf



def generate_process_metrics(nome_classe, commits_dict, folder = "repository"):
    """Genera le metriche di processo, è possibile specificare il commit da analizzare e il folder dove è conservata la repository"""
    """Questo metodo dovrà essere utilizzato per fare tutte le analisi disponibili con le metriche di processo, a parte i code churn"""
    # df_filtrato = ru.estrai_parametri(json_list)
    df_filtrato = pd.DataFrame(list(commits_dict.items()), columns=['Commit Hash', 'Data del Commit'])
    hash1 = df_filtrato.loc[0, "Commit Hash"]
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
    return df_finale


# PER ORA DEPRECATO
# def generate_ck_metrics(tag = None, year=0, df = None, folder = "repository",measures = ["cbo", "wmc", "dit", "noc", "rfc", "lcom"]):
#     """Genera le metriche ad oggetti , questo metodo prende la release da cui si vuole partire(opzionale), trova i commit e li inserisce in un dataframe"""
#     """Una volta generato ,se generato(quindi nel caso di avvio dell'analisi da 0) prende 10 commit e li analizza globalmente restituendo un dataframe """
#     """Con il commit_hash, la data e le misurazioni"""
#     """Se inserisci sia tag che anno il metodo non funzionerà, se inserisci l'anno ti riporterà un'analisi per anno, se inserisci il tag, un'analisi per release"""
    
#     if(tag is not None and year != 0):
#         print("Non si può analizzare sia release che anno")
#         return 0

#     if(tag is not None):
#         df = ru.inizia_analisi(tag = tag, folder=folder)
#     else:
#         if(year != 0):
#             df = ru.inizia_analisi(folder=folder, year=year)

#     commit=ck.commit_measure_interval(measures, df, folder)
#     if(commit.empty): 
#         print("Non ci sono commit disponibili")
#         return 0
#     return commit



def generate_metrics_ck(commits_dict, folder = "repository", measures =["cbo", "wmc", "dit", "noc", "rfc", "lcom"]):
    """Genera le metriche ad oggetti , questo metodo prende la release da cui si vuole partire(opzionale), trova i commit e li inserisce in un dataframe"""
    """Poi li filtra dal commit dopo la release precedente, alla release scelta e ritorna il primo dataframe filtrato,"""
    """Una volta richiamato il metodo, se gli si passa il dataframe e i due hash per cui si vuole avere l'intervallo di analisi, filtra di nuovo il df e analizza"""

    df_filtrato = pd.DataFrame(list(commits_dict.items()), columns=['Commit Hash', 'Data del Commit'])
    commit=ck.commit_measure_interval(measures, df_filtrato, folder)
    if(commit.empty): 
        print("Non ci sono commit disponibili")
        return 0
    return commit





