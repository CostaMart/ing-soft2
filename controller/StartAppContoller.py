from model.ComputingEndpointModel import ComputingEndpointModel
import subprocess
from model.DataAccessLayer.DAORepo import DAORepo
from model.LocalRepoModel import LocalRepoModel


class StartAppController:

    def __init__(self):
        self.localModel = LocalRepoModel()
        self.ComputeEnd = ComputingEndpointModel()
        
        
    def isGitInstalled(self):
        """ return false if git is not installed or not executable from console, returns true and version if everything is ok """    
        result = subprocess.run("git --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if("git version" in result.stdout):
                return True, result.stdout
        else: 
            return False
        
    def RepoData(self):
        self.localModel.RepoDataUpdate()
    
    def getLocalRepoData(self):
        return  self.localModel.repoData

    def isComputeEndpointActive(self):
        """ controlla se l'endpoint HTTP è attivo localmente """
        return self.ComputeEnd.isActiveLocal()

    def startComputationEndpoint(self):
        "   attiva l'endpoint locale "
        try: 
            self.ComputeEnd.activateLocal()
            return "local"
        except subprocess.SubprocessError as e:
            return "error"
            