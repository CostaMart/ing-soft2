
import requests
import subprocess
from icecream import ic

class ComputingEndpointModel:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ComputingEndpointModel, cls).__new__(cls) 
        return cls._instance   
    
    def activateLocal(self):
        """ richiede attivazione del servizio locale """
        try:
            p = subprocess.Popen(["python", "start_endpoint.py"], cwd= "backend")
            ic(p.pid)
        except  subprocess.SubprocessError as e:
            print(f"error while activating process: {e.with_traceback()}")
            raise
    
    def isActiveLocal(self):
        " controlla se il servizio è attivo localmente "
        return requests.get("http://localhost:8080/ping")