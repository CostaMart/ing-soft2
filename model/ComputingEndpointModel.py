
import requests
import multiprocessing
from icecream import ic
import backend.start_endpoint
from backend.start_endpoint import computationEndpoint

class ComputingEndpointModel:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ComputingEndpointModel, cls).__new__(cls) 
        return cls._instance   
    
    def activateLocal(self):
    
        """ richiede attivazione del servizio locale """
        try:
           self.parent_conn, child_conn = multiprocessing.Pipe()
           p = multiprocessing.Process(target= backend.start_endpoint.startEndpoint, args = [child_conn])
           p.start()
           print(p.pid)
        except  multiprocessing.ProcessError as e:
            print(f"error while activating process: {e.with_traceback()}")
            raise
    
    def isActiveLocal(self):
           
            self.parent_conn.send('ping --- {"num1": 5, "num2": 10}')
            
            result = self.parent_conn.recv()
            ic(f"la risposta ottenuta è: {result}")
       
    
   
    
    