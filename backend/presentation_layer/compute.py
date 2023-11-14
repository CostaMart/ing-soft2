from multiprocessing.connection import Pipe
from model.spMetrics import generate_process_metrics
""" tutte le funzioni devono accettare il dictionary come parametro (usando **args) così i 
parametri possono essere passati come coppie chiave valore """

"""In questo modulo python vengono inserite le funzioni da essere eseguite e in particolare
le funzioni per il calcolo delle metriche"""

def ping(**kwargs):
    
    if "num1" not in kwargs or "num2" not in kwargs:
        print("necessari parametri num1 e num2")
        return
    a = kwargs["num1"]
    b = kwargs["num2"]
    return a + b

def generate_metrics(**kwargs):
    """esegue il calcolo delle metriche usando le metriche di processo di spMetrics.py"""
    """genera le metriche di processo"""
    """ritorna un dizionario con le metriche"""
    
    #controllo se i parametri non sono presenti
    if "nome_classe" not in kwargs or "commits_dict" not in kwargs:
        print("necessari parametri nome_classe e commits_dict")
        return

    nome_classe = kwargs["nome_classe"]
    commits_dict = kwargs["commits_dict"]
    # a questo punto ritorna le metriche generate alla view che le stampa
    # sull'interfaccia grafica.
    return generate_process_metrics(nome_classe=nome_classe, commits_dict=commits_dict)
