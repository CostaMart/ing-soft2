import os
import shutil
import stat
import model.DataAccessLayer.RepoDataAccess
from .DataAccessLayer.RepoDataAccess import CRUDRepo
import subprocess

class LocalRepoModel:
    """SINGLETON: modella le interazioni e il recupero dei dati locali (come il repo locale) necessari all app """
    
    
    _instance = None
    repoData = None

    def __new__(cls):
        
        if cls._instance is None:
            cls._instance = super(LocalRepoModel, cls).__new__(cls)
            cls._instance.CRUD = CRUDRepo()
        return cls._instance

    def get_status_code(self):
        # Accedi all'attributo last_http_code di CRUDRepo
        status_code = self.CRUD.last_http_response
        return status_code

    def getRepoData(self):
        """ ritorna i metadati del repository installato localente """
        return self.repoData
    
    def RepoDataUpdate(self):
        """ recupera i meta dati aggiornati relativi al repo installato localmente """
        CRUD = self.CRUD
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
            repodata = self.CRUD.getRepoByNameeAuthor(name, repoName)
            self.repoData = repodata
            
            if self.repoData != None:
                self.repoData.releases = self.CRUD.get_all_release_tag_repo(name, repoName)

        os.chdir(current_directory)
          
    def createLocalRepo(self, url):
        """a partire dall'URL fornito intsalla localmente in una directory 'repository' il repo cercato"""
       
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
        "controlla se la directory repository esiste localmente, altrimenti la crea "
        if not os.path.exists("repository"):
            try:
                os.makedirs("repository")
            except OSError as e:
                print(f"Errore durante la creazione della cartella: {e}")
        else:
            return