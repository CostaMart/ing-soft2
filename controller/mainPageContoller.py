from model.Domain import Repository
from model import FilterProject
import os

        
def request_for_repos(query):
    """ funzione necessaria a concludere la risoluzione della query con @get_repo_list """
    repoList = FilterProject.search_repo(query)
    return repoList
    
def get_selected_repo(url):
    FilterProject.clone_repo(url)
    return


def checkRepo():
        percorso_git = os.path.join("repository", ".git")
        if os.path.exists(percorso_git) and os.path.isdir(percorso_git):
            return True
        else:
            return False