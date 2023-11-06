from model.Domain import Repository 
import model.FilterProject

class ControllerFalso:
    def getLocalRepoData(self):
        repo = Repository(name = "reopo", html_url= "repoURl", releases=["rel1", "rel2"], description= "ciao")
        repo.git_url = "ciao"
        repo.license = {"name": "brutta"}
        repo.owner = {"login":"ca",
                      "url": "ciao"}
        
        return repo
    
    
    def getClassesListR(self):
        return model.repo_utils.cerca_file_java("repository")