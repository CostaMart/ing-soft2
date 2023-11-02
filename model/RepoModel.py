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


