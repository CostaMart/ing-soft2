from model.DataAccessLayer.RepoDataAccess import CRUDRepo


class RepoModel:
    """Classe che recupera i repository utilizzando il layer
    di accesso ai dati"""

    @staticmethod
    def getRepoListByName(name):
        CRUD = CRUDRepo()
        return CRUD.getRepoList(name)

    @staticmethod
    def getRepoListByNameInJava(name):
        CRUD = CRUDRepo()
        return CRUD.getJavaRepoList(name)

# Esempio di utilizzo:
repo_name = "esempio"  # Sostituisci con il nome del repository che stai cercando
repositories = RepoModel.getRepoListByNameInJava(repo_name)

for repo in repositories:
    print(f"Nome: {repo.name}")
    print(f"URL: {repo.url}")
    print(f"Descrizione: {repo.description}")
    print("---")
