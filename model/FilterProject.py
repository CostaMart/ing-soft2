from model.Domain import Repository
import requests



def search_repo(nome_progetto):
    
    # Effettua la ricerca dei repository su GitHub basati sul nome del progetto
    url = f"https://api.github.com/search/repositories?q={nome_progetto}"
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

# Esempio di utilizzo della funzione
# nome_progetto = input("Inserisci il nome del progetto: ")
# repositories = ricerca_e_restituzione_repositories(nome_progetto)
#
# for repository in repositories:
#     print(f"Nome: {repository.name}")
#     print(f"URL: {repository.url}")
#     print(f"Descrizione: {repository.description}")
#     print("-----------------------")


