from model.Domain import Repository
from model import FilterProject
import threading

        
def request_for_repos(query):
    """ funzione necessaria a concludere la risoluzione della query con @get_repo_list """
    repoList = FilterProject.search_repo(query)
    return repoList
    
def get_selected_repo(url):
    FilterProject.clone_repo(url)
    return