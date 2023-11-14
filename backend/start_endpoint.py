import time
from multiprocessing import Process, Pipe
from multiprocessing.connection import PipeConnection
from icecream import ic
from .functionFactory import FunctionFactory


# Descrizione della classe:

""" Classe che permette di inviare un messaggio tramite la pipe bidirezionale a un processo 
    che esegue il calcolo delle metriche"""

class computationEndpoint:
    
    """ inizializza l'endpoint """
    def __init__(self, connection : PipeConnection):

        # In questo modo si crea un canale bidirezionale ovvero la pipe
        # che è un oggetto che permette di comunicare tra processi
       
        self.funFactory = FunctionFactory()
        self.pipe = connection
        self.worker()
        
    def worker(self):
    
        while True:
            # Attende un messaggio dalla pipe
            message = self.pipe.recv()
            
            if "fun" not in message:
                print("""errore, il messaggio deve essere un dictionary che contiene il parametro 'fun' per 
                      specificare la funzione, seguito da una coppia chiave valore per ognuno dei parametri.""")
                return
                
            # rimuovo il nome del metodo, nella lista rimarranno solo i parametri
            fun = self.funFactory.getFunct(message.pop("fun"))
            
            if fun is not None:
                print(f"{fun}")
                ans = fun(**message)
                self.pipe.send(ans)
                
                
            else:
                self.pipe.send(f"nessuna corrispondenza con una funzione disponibile: messaggio {message}, metodo chiamato ")
                return
            
        
            
def startEndpoint(connection : PipeConnection ):
    """ questo metodo viene invocato dall'altro processo per avviare questo endpoint. Funziona sostanzialmente da main """
    computationEndpoint(connection)
    
   
                
            

            

