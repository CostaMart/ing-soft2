import os
import shutil
import stat
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
        
        current_directory = os.getcwd()
        
        os.chdir("repository")
        repoDir = subprocess.check_output(["dir"]).decode("utf-8")
        
        repoDir = os.path.join(current_directory,"repository",repoDir)
        repoDir = repoDir.replace("\n", "")
        
        checkDir = os.path.join(current_directory,"repository")

        if os.getcwd() == checkDir:
            os.chdir(repoDir)
            
            result = subprocess.check_output(["git", "remote", "show", "origin"]).decode("utf-8")
    
            os.chdir(current_directory)
            print(os.getcwd())
            
            firstLine = result.split("\n")[1]
            name = firstLine.split("/")[-2]
            repoName = firstLine.split("/")[-1]
            repodata = CRUD.getRepoByNameeAuthor(name, repoName)
            self.repoData = repodata

        os.chdir(current_directory)
        
        
    def createLocalRepo(self, url):
        current_directory = os.getcwd()
        folder_path = os.path.join(current_directory, "repository")
        os.chdir(folder_path)

        contenuto_directory = os.listdir()

        def on_rm_error( func, path, exc_info):

            os.chmod( path, stat.S_IWRITE )
            os.unlink( path )
        
        for dir in contenuto_directory:
            if dir != "repository":
                shutil.rmtree( dir, onerror = on_rm_error )
               
        
            
        subprocess.call(['git', 'clone', url])
        os.chdir(current_directory)
        
    def _CheckRepoDir(self):
        if not os.path.exists("repository"):
            try:
                os.makedirs("repository")
            except OSError as e:
                print(f"Errore durante la creazione della cartella: {e}")
        else:
            return