
from typing import List
from model.LocalRepoModel import LocalRepoModel
from model import Domain
import model.repo_utils
from icecream import ic
from pydriller import Commit
from threading import Thread, Lock

class ProjectMetricsController:
    
    my_lock = Lock()
    
    
    def __init__(self):
       self.localModel = LocalRepoModel()
    
    
    def getLocalRepoData(self) -> Domain.Repository:
        return self.localModel.getRepoData()
    
    def getClassesList(self, commitHash) -> List[str]: 
        files = self.localModel.getClassListFromGivenCommit(commitHash)
        allFileList= [file.split("/")[-1] for file in files]
        classList = [file for file in allFileList if ".java" in file]
        return classList
        
    def getCommitWithClassList(self, className):
        return self.localModel.getCommitWithClassList(className= className)

    def updateRepoYearList(self, year, callback):
        
        def target():
            self.my_lock.acquire()
            yearList = self.localModel.getYearList()
            callback(yearList)
            self.my_lock.release()
            
        Thread(target = target).start()
    
    def updateCommitsListByYear(self, year, callback):
        myYear = year
        
        def target():
            self.my_lock.acquire()
            commitList = self.localModel.getCommiListByYear(myYear)
            callback(commitList)
            self.my_lock.release()
            
        Thread(target = target).start()    

    def updateArriveCommitList(self, year, callback):
        
        def target():
            self.my_lock.acquire()
            commitList = self.localModel.getCommiListByYear(year)
            callback(commitList)
            self.my_lock.release()
            
        Thread(target = target).start()    
    
    def getCommitByhash(self, hash) -> Commit:
        return self.localModel.getCommitByHash(hash)