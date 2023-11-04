from typing import Callable, List
from model.Domain import Repository
import os
from model.LocalRepoModel import LocalRepoModel
from model.RepoModel import RepoModel
import threading


class MainPageController:
   
    def __init__(self):
        super().__init__()
        self.process = None
        self.globalModel = LocalRepoModel()
        self.repoModel = RepoModel()
         
    def requestRepoUpdate(self, callbackBefore : Callable[[], None] = None, callbackAfter : Callable[[], None] = None):
        """ avvia una richiesta di update per i dati locali del repository, verrà eseguita su un thread apposito
        è possibile registrare una callback sia prima che dopo l'update,
        verranno eseguite nello stesso thread dell'update"""
        def toRun():
            if callbackBefore != None:
                callbackBefore()
                
            self.globalModel.RepoDataUpdate()  
            
            if callbackAfter != None:
                callbackAfter()
        threading.Thread(target = toRun).start()
            
    def getRepoData(self):     
        return self.globalModel.getRepoData()
    
    def request_for_repos(self, query, callback : Callable[[List[Repository]], any]):
        """ recupera una nuova lista di repository in maniera asincrona"""
        def toRun():
            repoList = self.repoModel.getRepoListByName(query)
            callback(repoList)
        
        threading.Thread(target= toRun).start()
            
    def get_selected_repo(self, url):
        self.globalModel.createLocalRepo(url)
        return True
           
    def checkRepo(self):
            percorso_git = os.path.join("repository", ".git")
            if os.path.exists(percorso_git) and os.path.isdir(percorso_git):
                return True
            else:
                return False