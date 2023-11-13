
from typing import List
from model.LocalRepoModel import LocalRepoModel
from model import Domain
from icecream import ic
from pydriller import Commit
from threading import Thread, Lock

class ProjectMetricsController:
    
    my_lock = Lock()
    
    
    def __init__(self):
       self.localModel = LocalRepoModel()
    
    def getLocalRepoData(self) -> Domain.Repository:
        """ ritorna dati basilari sul repository locale installato """
        return self.localModel.getRepoData()
    
    def getClassesList(self, commitHash) -> set[str]: 
        """ ritorna un set contenente il nome delle classi presenti in un commit """
        files = self.localModel.getClassListFromGivenCommit(commitHash)
       
        return files
        
    def getCommitWithClassList(self, className):
        return self.localModel.getCommitWithClassList(className= className)

    def updateRepoYearList(self, callback):
        """ esegue la callback in un thread """
        Thread(target = callback).start()
               
    def updateCommitsListByYear(self, year, callback):
        """ recupera una lista di tutti i commit avvenuti in un dato anno e la passa
        come parametro a callback """
        myYear = year
        def target():
            commitList = self.localModel.getCommiListByYear(myYear)
            callback(commitList)
        Thread(target = target).start()    
        
    def getYearList(self):
        """ ritorna la lista completa di tutti gli anni in cui è stato effettuato almeno un commit
        per il repostiory installato """
        return self.localModel.getYearList()
    
    def getCommitByhash(self, hash) -> Commit:
        """ recupera il commit specificato con l'hash passato comme parametro """
        return self.localModel.getCommitByHash(hash)
    
    def getCommiListFromDate(self, date, yearToArrive, callback):
        """ recupera la lista dei commit a partire da date fino ad arrivare all'ultimo
        giorno di yearToArrive. La lista recuperata viene passata alla callback """
        def target():
            commitList = self.localModel.getCommiListFromDate(date, yearToArrive)
            callback(commitList)
            
        Thread(target = target).start()
            
        
        
        
        
        
            
            

        
            
            
    
        