
from model.LocalRepoModel import LocalRepoModel


class MetricsPageContoller:
    
    def __init__(self):
       self.localModel = LocalRepoModel()
    
    
    def getLocalRepoData(self):
        return self.localModel.getRepoData()