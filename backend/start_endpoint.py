import time
from multiprocessing import Process, Pipe
from multiprocessing.connection import PipeConnection
from icecream import ic
import inspect
from .presentation_layer import compute

# Descrizione della classe:

""" Classe che permette di inviare un messaggio tramite la pipe bidirezionale a un processo 
    che esegue il calcolo delle metriche"""

class computationEndpoint:
    
    """ inizializza l'endpoint """
    def __init__(self, connection : PipeConnection):

        # In questo modo si crea un canale bidirezionale ovvero la pipe
        # che è un oggetto che permette di comunicare tra processi
        self.functList = dict(inspect.getmembers(compute, predicate= inspect.isfunction))
      
        self.pipe = connection
        self.worker()
        
    def worker(self):
        """ metodo di lavoro: il processo si mette in attesa di ricevere un messaggio da quello principale
        recupera una lista di metodi e invoca il metodo con il nome corrispondente al contenuto del messaggio
        se si vuole inviare dei dati con il messaggio è necessario formattarli come json, inserendoli dopo il nome della funzione da invocare 
        separati da '---' ESEMPIO:
        (le singole funzioni dovranno occuparsi della deserializzazione del json)
        sum --- {
                 num1: 1,
                 num2: 2 
                 }"""
        
        while True:
            # Attende un messaggio dalla pipe
            
            
            message = self.pipe.recv()
            message = message.split("---")
            name = message[0]
            json = message [1]
            name = name.strip()
            json = json.strip()
            
            if name in self.functList.keys():
                print(f"{name}")
                
                funct = self.functList[name]
                funct(self.pipe, json)
            
            else:
                self.pipe.send(f"nessuna corrispondenza con una funzione disponibile: messaggio {message}, metodo chiamato ")

def startEndpoint(connection : PipeConnection ):
    """ questo metodo viene invocato dall'altro processo per avviare questo endpoint. Funziona sostanzialmente da main """
    computationEndpoint(connection)
    
   
