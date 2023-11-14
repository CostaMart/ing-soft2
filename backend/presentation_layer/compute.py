from multiprocessing.connection import PipeConnection
""" tutte le funzioni devono accettare il dictionary come parametro (usando **args) così i 
parametri possono essere passati come coppie chiave valore """

def ping(**kwargs):
    
    if "num1" not in kwargs or "num2" not in kwargs:
        print("necessari parametri num1 e num2")
        return
    a = kwargs["num1"]
    b = kwargs["num2"]
    return a + b
    