import os
import shutil
import sys
from .DataAccessLayer.RepoDataAccess import CRUDRepo
import subprocess

class LocalRepoModel:
    """modella le interazioni e il recupero dei dati locali (come il repo locale) necessari all app """
    
    
    _instance = None
    repoData = None
    
    def __new__(cls):
        
        if cls._instance is None:
            cls._instance = super(LocalRepoModel, cls).__new__(cls)
            
        return cls._instance
    
    def getRepoData(self):
        return self.repoData
    
    def RepoDataUpdate(self):
        CRUD = CRUDRepo()
        self._CheckRepoDir()
  
        result = subprocess.check_output(["git", "remote", "show", "origin"], cwd="repository").decode("utf-8")
        
        firstLine = result.split("\n")[1]
        name = firstLine.split("/")[-2]
        repoName = firstLine.split("/")[-1]
        repodata = CRUD.getRepoByNameeAuthor(name, repoName)

        self.repoData = repodata

    def createLocalRepo(self, url):
        current_directory = os.getcwd()
        folder_path = os.path.join(current_directory, "repository")
    
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                    
            except OSError as e:
                print(f"Errore durante la creazione della cartella repository': {e}")
        else:   
            if sys.platform.startswith('win'):
                print("siamo su windowss")
                os.system(f'rmdir /S /Q ')
        
            elif sys.platform.startswith('linux'):
                print("siamo su linux")
                shutil.rmtree("repository")   
       
        return subprocess.call(['git', 'clone', url], cwd= "repository")
    
    def _CheckRepoDir(self):
        if not os.path.exists("repository"):
            try:
                os.makedirs("repository")
            except OSError as e:
                print(f"Errore durante la creazione della cartella: {e}")
        else:
            return

