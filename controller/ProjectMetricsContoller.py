
from typing import List
from model.LocalRepoModel import LocalRepoModel
from model import Domain
import model.repo_utils
import os
from icecream import ic

class ProjectMetricsController:
    
    def __init__(self):
       self.localModel = LocalRepoModel()
    
    
    def getLocalRepoData(self) -> Domain.Repository:
        return self.localModel.getRepoData()
    
    def getClassesList(self, tag) -> List[str]: 
        return model.repo_utils.checkout_tag(tag, "repository")
        
    def getClassesListR(self):
        return model.repo_utils.cerca_file_java("repository") 
        
    def getCommitWithClassList(self, className):
        return ic(self.localModel.getCommitWithClassList(className= className))
