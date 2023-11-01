from model.DataAccessLayer.RepoDataAccess import CRUDRepo


class RepoModel:
    

    def getRepoListByName(self, name):
        CRUD =  CRUDRepo()
        return CRUD.getRepoList(name)
    