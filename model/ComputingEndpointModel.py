import multiprocessing
from icecream import ic
from backend.start_endpoint import startEndpoint  # Importa il target del processo


class ComputingEndpointModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ComputingEndpointModel, cls).__new__(cls)
        return cls._instance

    def activateLocal(self):
        """Richiede l'attivazione del servizio locale."""
        try:
            self.parent_conn, child_conn = multiprocessing.Pipe()
            p = multiprocessing.Process(target=startEndpoint, args=(child_conn,))
            p.start()
            print(f"Processo avviato con PID: {p.pid}")
        except Exception as e:
            print(f"Errore durante l'attivazione del processo: {e}")
            raise

    def isActiveLocal(self):
        """Verifica se il processo creato è attivo."""
        try:
            self.parent_conn.send({"fun": "ping", "num1": 1, "num2": 2})
            result = self.parent_conn.recv()
            ic(f"La risposta ottenuta è: {result}")
        except Exception as e:
            print(f"Errore durante il controllo dell'attività del processo locale: {e}")

    def sendMessageToEndpoint(self, message):
        """Invia un messaggio al processo."""
        try:
            self.parent_conn.send(message)
        except Exception as e:
            print(f"Errore durante l'invio del messaggio al processo: {e}")

    def receiveMessageFromEndpoint(self):
        """Ricevi un messaggio dal processo."""
        try:
            message = self.parent_conn.recv()
            return message
        except Exception as e:
            print(f"Errore durante la ricezione del messaggio dal processo: {e}")

    def isEndpointActive(self):
        """Verifica se il processo è attivo."""
        return self.parent_conn.poll()  # True se il processo è attivo, False altrimenti

    def destroy(self) -> None:
        self.parent_conn.send({"fun": "destroy"})
        message = self.parent_conn.recv()
        print(message)