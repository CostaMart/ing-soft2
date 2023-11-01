from model.Domain import Repository
from model import FilterProject
import os
import psutil


class mainPageController:
    def __init__(self):
        super().__init__()
        self.process = None
        
    def request_for_repos(self, query):
        """ funzione necessaria a concludere la risoluzione della query con @get_repo_list """
        repoList = FilterProject.search_repo(query)
        return repoList
        
    def get_selected_repo(self, url):
        FilterProject.clone_repo(url)
        return True
           
            


    def checkRepo(self):
            percorso_git = os.path.join("repository", ".git")
            if os.path.exists(percorso_git) and os.path.isdir(percorso_git):
                return True
            else:
                return False