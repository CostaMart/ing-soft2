import requests
from icecream import ic
from model.Domain import HttpResponse, Repository, MetadataRepository 
import os
from ..FilterProject import  get_all_release_tag_repo


class DAORepo:
    def __init__(self):
        self.last_http_response = None



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

        self.last_http_response = HttpResponse(response.status_code, response.json())

        if response.status_code == 200:
            repository_data = response.json()
            repository = MetadataRepository(repository_data)
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
        self.last_http_response = HttpResponse(response.status_code, response.json())
        if response.status_code == 200:
            repository_data = response.json()
            repository = MetadataRepository(repository_data)
            relesases = self._set_release_tags(repository.owner, repository.full_name)
            repository.tag_releases = relesases

            return repository
        else:
            return None



    def getRepoList(self, repoName):
        # Solo i repository java
        url = f"https://api.github.com/search/repositories?q={repoName}+language:java"
        response = requests.get(url)
        self.last_http_response = HttpResponse(response.status_code, response.json())
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
        self.last_http_response = HttpResponse(response.status_code, response.json())
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



    def get_all_release_tag_repo(self, owner, repo_name):
        """Metodo che ritorna tutte le  releases di uno specifico progetto"""
        url = f"https://api.github.com/repos/{owner}/{repo_name}/releases"
        response = requests.get(url)

        if response.status_code == 200:
            releases = response.json()
            # Estrai solo i tag delle release dalla lista di release
            
            release_tags = [release['tag_name'] for release in releases]
            return release_tags
        else:
            print(f"Errore {response.status_code}: Impossibile ottenere le release del progetto.")
            return None



    def getJavaRepoListForAuthorAndRepo(self, author, repo_name):
        # Se l'autore è specificato, cerca per il nome del repository all'interno dell'account dell'autore
        url = f"https://api.github.com/search/repositories?q=user:{author}+repo:{repo_name}+language:java"
        response = requests.get(url)
        self.last_http_response = HttpResponse(response.status_code, response.json())
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



    def getRepoListByAuthor(self, author):
        url = f"https://api.github.com/search/repositories?q=user:{author}+language:java"
        response = requests.get(url)
        self.last_http_response = HttpResponse(response.status_code, response.json())
        repositories = []
        if response.status_code == 200:
            risultati = response.json()['items']  # Accedi alla lista dei repository dentro la chiave "items"
            for risultato in risultati:
                name = risultato['name']
                html_url = risultato['html_url']
                description = risultato['description']
                repository = Repository(name, html_url, description)
                repositories.append(repository)

        return repositories

