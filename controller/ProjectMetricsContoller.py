
from model.LocalRepoModel import LocalRepoModel
from model import Domain

class MetricsPageContoller:
    
    def __init__(self):
       self.localModel = LocalRepoModel()
    
    
    def getLocalRepoData(self) -> Domain.Repository:
        return self.localModel.getRepoData()