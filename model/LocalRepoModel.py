import os
from .DataAccessLayer.DAORepo import DAORepo
from icecream import ic
from .DataAccessLayer.LocalDAO import LocalDAO


class LocalRepoModel:
    """SINGLETON: modella le interazioni e il recupero dei dati locali (come il repo locale) necessari all app """
    
    
    _instance = None
    repoData = None

    def __new__(cls):
        
        if cls._instance is None:
            cls._instance = super(LocalRepoModel, cls).__new__(cls)
            cls._instance.CRUD = DAORepo()
            cls._instance.LocalDAO = LocalDAO()
        return cls._instance

    def getRepoData(self):
        """ ritorna i metadati del repository installato localente """
        return self.repoData
    
    def RepoDataUpdate(self):
        """Recupera i metadati aggiornati relativi al repository installato localmente."""

        self._CheckRepoDir()

        # Utilizzo del pattern DAO
        name, repoName = self.LocalDAO.getRepoInfoFromGit()

        if name is not None and repoName is not None:
            repodata = self.CRUD.getRepoByNameeAuthor(name, repoName)
            self.repoData = repodata

            if self.repoData is not None:
                self.repoData.releases = self.CRUD.get_all_release_tag_repo(name, repoName)

    def createLocalRepo(self, url):
        """A partire dall'URL fornito, installa localmente in una directory 'repository' il repo cercato."""
        self.LocalDAO.cloneRepository(url)

    def _CheckRepoDir(self):
        "controlla se la directory repository esiste localmente, altrimenti la crea "
        if not os.path.exists("repository"):
            try:
                os.makedirs("repository")
            except OSError as e:
                print(f"Errore durante la creazione della cartella: {e}")
        else:
            return

    def get_status_code(self):
        # Accedi all'attributo last_http_code di CRUDRepo
        status_code = self.CRUD.last_http_response
        return status_code
    
    def getAllJavaClassProject(self, rootDirectory):
        return self.LocalDAO.findJavaClass(rootDirectory)
    
    def getCommitWithClassList(self, className):
        """ dato il nomoe di una classe recupera tutti i commit in cui questa è presente """
        return self.LocalDAO.get_commits_with_class(className, "repository")
    
    def getYearList(self):
        return self.LocalDAO.extract_years_from_commits()
    
    def getClassListFromGivenCommit(self, commit):
        return self.LocalDAO.getClassListFromGivenCommit(commit)
    
    def getCommiListByYear(self, year):
        return self.LocalDAO.dataCommitLinkYear(year)