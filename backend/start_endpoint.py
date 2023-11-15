import time
from icecream import ic
from .functionFactory import FunctionFactory


# Descrizione della classe:

""" Classe che permette di inviare un messaggio tramite la pipe bidirezionale a un processo 
    che esegue il calcolo delle metriche"""


class ComputationEndpoint:

    def __init__(self, connection):
        self.working = True
        self.funFactory = FunctionFactory()
        self.pipe = connection
        self.worker()

    def worker(self):
        try:
            while self.working:
                message = self.pipe.recv()

                if "fun" not in message:
                    self.pipe.send(
                        "Errore: il messaggio deve essere un dizionario che contiene il parametro 'fun' per specificare la funzione.")
                    continue
                
                if message["fun"] == "destroy":
                    self.pipe.send("destroy request ok")
                    self.destroy()
                    continue    

                fun_name = message.pop("fun")
                fun = self.funFactory.getFunct(fun_name)

                if fun is not None:
                    print(f"Esecuzione della funzione: {fun_name}")
                    result = fun(**message)
                    self.pipe.send(result)
                else:
                    error_message = f"Nessuna corrispondenza con una funzione disponibile: messaggio {message}, metodo chiamato {fun_name}"
                    self.pipe.send(error_message)

        except Exception as e:
            print(f"Errore durante l'esecuzione del worker: {e}")

        finally:
            self.pipe.close()
    
    def destroy(self):
        self.working = False



# Funzione per avviare l'endpoint
def startEndpoint(connection):
    try:
        ComputationEndpoint(connection)
    except Exception as e:
        print(f"Errore durante l'avvio dell'endpoint: {e}")



    
            

            

