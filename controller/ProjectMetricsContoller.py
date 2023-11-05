
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
        dirs = os.listdir("repository")
        path = os.path.join("repository", dirs[0]) 
        return model.repo_utils.checkout_tag(tag, path)
        
    def getClassesListR(self):
        dirs = os.listdir("repository")
        path = os.path.join("repository", dirs[0]) 
        ic(model.repo_utils.cerca_file_java(path)) 
        return model.repo_utils.cerca_file_java(path) 
        