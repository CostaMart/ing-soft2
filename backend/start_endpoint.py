import time
from multiprocessing import Process, Pipe

# Descrizione della classe:

""" Classe che permette di inviare un messaggio tramite la pipe bidirezionale a un processo 
    che esegue il calcolo delle metriche"""

class MyClass:
    def __init__(self):
        # In questo modo si crea un canale bidirezionale ovvero la pipe
        # che è un oggetto che permette di comunicare tra processi
        self.parent_conn, self.child_conn = Pipe()

    def execute_some_task(self, request):
        """ Metodo che rappresenta il lavoro da eseguire"""
        # TODO: Implementare il lavoro da eseguire con il calcolo delle metriche
        time.sleep(5)
        return f"Task eseguito con successo: {request}"

    def worker(self):
        """Metodo che controlla se è arrivato un messaggio sulla pipe"""
        while True:
            # Attende un messaggio dalla pipe
            message = self.child_conn.recv()
            # Chiamata del metodo che esegue il lavoro
            result = self.execute_some_task(request=message)

            # Invia la risposta attraverso la pipe
            self.child_conn.send(result)

    def start_worker(self):
        """Metodo che avvia il processo di lavoro"""
        worker_process = Process(target=self.worker)
        worker_process.start()

    def make_request(self, request):
        """Metodo utilizzato dai chiamanti per inviare un messaggio sulla pipe"""
        self.parent_conn.send(request)

        # in questo modo il processo di lavoro può ricevere il messaggio
        response = self.parent_conn.recv()

        # ritorna il risultato
        return response

