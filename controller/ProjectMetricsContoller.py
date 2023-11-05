
from typing import List
from model.LocalRepoModel import LocalRepoModel
from model import Domain

class ProjectMetricsController:
    
    def __init__(self):
       self.localModel = LocalRepoModel()
    
    
    def getLocalRepoData(self) -> Domain.Repository:
        return self.localModel.getRepoData()
    
    def getClassesList(self) -> List[str]:
        return self.localModel.getAllJavaClassProject("repository")