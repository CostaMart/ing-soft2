import model.process_metrics as pm
import model.repo_utils as ru
import pandas as pd
import model.git_ck as ck
from icecream import ic



def generate_process_metrics(hash_code=None, folder = "repository"):
    """Genera le metriche di processo, è possibile specificare il commit da analizzare e il folder dove è conservata la repository"""
    """Questo metodo dovrà essere utilizzato per fare tutte le analisi disponibili con le metriche di processo, a parte i code churn"""
    if(hash_code is not None):
        ru.checkout_commit(hash_code)
    if(folder != "repository"):
        nr = pm.controlla_numero_revisioni_per_repo(folder)
        lc = pm.calcola_loc_repo(folder)
        ad = pm.calcola_autori_distinti_per_repo(folder)
        sf = pm.calcola_settimane_repo(folder)
    else:
        nr = pm.controlla_numero_revisioni_per_repo()
        lc = pm.calcola_loc_repo()
        ad = pm.calcola_autori_distinti_per_repo()
        sf = pm.calcola_settimane_repo()
    result = nr.merge(lc, on='Nome della Classe').merge(ad, on='Nome della Classe').merge(sf, on='Nome della Classe')
    bf = pm.calcola_numero_bug_fix()
    resultDF = pd.DataFrame(result)
    return resultDF, bf



def generate_ck_metrics(tag = None, year=0, df = None, index= 0, folder = "repository",measures = ["cbo", "wmc", "dit", "noc"]):
    """Genera le metriche ad oggetti , questo metodo prende la release da cui si vuole partire(opzionale), trova i commit e li inserisce in un dataframe"""
    """Una volta generato ,se generato(quindi nel caso di avvio dell'analisi da 0) prende 10 commit e li analizza globalmente restituendo un dataframe """
    """Con il commit_hash, la data e le misurazioni"""
    """Se inserisci sia tag che anno il metodo non funzionerà, se inserisci l'anno ti riporterà un'analisi per anno, se inserisci il tag, un'analisi per release"""
    
    if(tag is not None and year != 0):
        print("Non si può analizzare sia release che anno")
        return 0,0,0

    if(index == 0 and tag is not None):
        df = ru.inizia_analisi(tag = tag, folder=folder)
    else:
        if(index == 0 and year != 0):
            df = ru.inizia_analisi(folder=folder, year=year)

    commit=ck.commit_measure_interval(measures, df, index, folder)
    if(commit.empty): 
        print("Non ci sono commit disponibili")
        return 0,0,0
    return commit, index+10, df





