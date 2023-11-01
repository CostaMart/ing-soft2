from model.Domain import Repository
from model import FilterProject
import os
from model.LocalRepoModel import LocalRepoModel
from model.RepoModel import RepoModel
import psutil


class mainPageController:
    def __init__(self):
        super().__init__()
        self.process = None
        self.globalModel = LocalRepoModel()
        self.repoModel = RepoModel()
      
      
    def requestRepoUpdate(self):
        self.globalModel.RepoDataUpdate()  
        
    def getRepoData(self):     
        return self.globalModel.getRepoData()
    
    def request_for_repos(self, query):
        """ funzione necessaria a concludere la risoluzione della query con @get_repo_list """
        
        return self.repoModel.getRepoListByName(query)
        
    def get_selected_repo(self, url):
        self.globalModel.createLocalRepo(url)
        return True
           
    def checkRepo():
            percorso_git = os.path.join("repository", ".git")
            if os.path.exists(percorso_git) and os.path.isdir(percorso_git):
                return True
            else:
                return False