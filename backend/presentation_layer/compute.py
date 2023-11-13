from multiprocessing.connection import PipeConnection
import json

def ping(pipe : PipeConnection, jsonFile : str ):
    """ le funzioni devono prendere il parametro pipe e jsonFile per poter prendere i parametri e rispondere
    questo è un esempio di come si può creare una funzione """
    
    result = json.loads(jsonFile)
    a = result["num1"]
    b = result["num2"]
    c = a + b
    pipe.send(f"mi piace perchè sta funzionando, sappi che ho calcolato la somma ed è: {c}")