from model.Domain import Repository
from model import FilterProject
import threading


def get_repo_list(query : str, callback) -> list[Repository]:
    """recupera una lista di repositories con il dato nick, è possibile passare una callback che verrà eseguita quando i repo saranno recuperati. Verrà passasto come parametro della callback
    proprio i repository recuperati""" 
    thread = threading.Thread(target= _request_for_repos, args=(query, callback))
    thread.start()
        
    

def _request_for_repos(query, callback):
    repoList = FilterProject.search_repo(query)
    callback(repoList)
    