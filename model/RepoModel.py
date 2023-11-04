from model.DataAccessLayer.RepoDataAccess import CRUDRepo


class RepoModel:
    """Classe che recupera i repository utilizzando il layer
    di accesso ai dati"""
    def __init__(self):
        self.CRUD= CRUDRepo()

    def getRepoListByName(self, name):
        return self.CRUD.getRepoList(name)

    def getRepoListByNameInJava(self, name):
        return self.CRUD.getJavaRepoList(name)

    def getRepoListByAuthorAndRepoName(self, author, repo_name):
       return self.CRUD.getJavaRepoListForAuthorAndRepo(author, repo_name)

    def getRepoListByAuthor(self, author):
       return self.CRUD.getRepoListByAuthor(author)

