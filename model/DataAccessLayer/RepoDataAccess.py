from ..FilterProject import *
from icecream import ic

class CRUDRepo:
    
    def _set_release_tags(self, owner, repo_name):
           
            """Metodo che setta le versioni delle release nell'oggetto
                che modella i metadati del progetto github"""
            release_tags = get_all_release_tag_repo(owner, repo_name)
            if release_tags:
                self.tag_releases = release_tags
            else:
                print("Impossibile impostare i tag delle release.")
     
    def getRepoByNameeAuthor(self, repoOwner, repoName): 
       
        response = requests.get(f'https://api.github.com/repos/{repoOwner}/{repoName}')
       
        ic(response.json())
        
        if response.status_code == 200:
            repository_data = response.json()
            repository = Domain.MetadataRepository(repository_data)
            relesases = self._set_release_tags(repository.owner, repository.full_name)
            repository.tag_releases = relesases
            
            return repository
        else:
            return None
        
    def getRepoByUrl(self, repoUrl: str):
        splitted = repoUrl.split("/")
        repoName = splitted[-1]
        repoOwner = splitted[-2]
    
        response = requests.get(f'https://api.github.com/repos/{repoOwner}/{repoName}')
        
        if response.status_code == 200:
            repository_data = response.json()
            repository = Domain.MetadataRepository(repository_data)
            relesases = self._set_release_tags(repository.owner, repository.full_name)
            repository.tag_releases = relesases
            ic(repository)
            return repository
        else:
            return None
       
    def getRepoList(self, repoName):
        #Solo i repository java
        url = f"https://api.github.com/search/repositories?q={repoName}+language:java"
        response = requests.get(url)
        risultati = response.json()["items"]

        # Crea una lista di oggetti di tipo Repository
        repositories = []
        for risultato in risultati:
            name = risultato["name"]
            html_url = risultato["html_url"]
            description = risultato["description"]
            repository = Repository(name, html_url, description)
            repositories.append(repository)

        return repositories
            

    def getJavaRepoList(self, repoName):
        url = f"https://api.github.com/search/repositories?q={repoName}+language:java"
        response = requests.get(url)
        risultati = response.json()["items"]

        # Crea una lista di oggetti di tipo Repository
        repositories = []
        for risultato in risultati:
            name = risultato["name"]
            html_url = risultato["html_url"]
            description = risultato["description"]
            repository = Repository(name, html_url, description)
            repositories.append(repository)

        return repositories