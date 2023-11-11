
from typing import List
from model.LocalRepoModel import LocalRepoModel
from model import Domain
import model.repo_utils
from icecream import ic

class ProjectMetricsController:
    
    def __init__(self):
       self.localModel = LocalRepoModel()
    
    
    def getLocalRepoData(self) -> Domain.Repository:
        return self.localModel.getRepoData()
    
    def getClassesList(self, commitHash) -> List[str]: 
        files = self.localModel.getClassListFromGivenCommit(commitHash)
        allFileList= ic([file.split("/")[-1] for file in files])
        classList = [file for file in allFileList if ".java" in file]
        return classList
        
    def getCommitWithClassList(self, className):
        return self.localModel.getCommitWithClassList(className= className)

    def getRepoYearList(self):
        return self.localModel.getYearList()
    
    def getCommitsByYear(self, year):
        return self.localModel.getCommiListByYear(year)