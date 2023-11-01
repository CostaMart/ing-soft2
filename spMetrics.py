import process_metrics as pm
import repo_utils as ru
import pandas as pd

def generate(hash_code, folder = "repository"):
    """Dato l'hash di un commit, il metodo punta al commit richiesto e ne calcola le metriche di processo"""
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


def generate_master(folder = "repository"):
    """Calcola le metriche di processo dell'elemento puntato dalla repository"""
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




