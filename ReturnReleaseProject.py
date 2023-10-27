import requests


def get_github_releases(repo_url):
    # Estrai il nome del proprietario e del repository dal link
    parts = repo_url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]

    # URL dell'API delle release di GitHub
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    # Esegui la chiamata GET all'API di GitHub
    response = requests.get(api_url)

    # Verifica se la chiamata è stata eseguita con successo (status code 200)
    if response.status_code == 200:
        releases = response.json()
        return releases
    else:
        print("Errore nell'ottenere le release del repository.")
        return None


# Esempio di utilizzo della funzione
# repo_url="https://github.com/obsidianmd/obsidian-releases"
# releases = get_github_releases(repo_url)
#
# if releases:
#     print("Release disponibili nel repository:")
#     for release in releases:
#         print(f"- Nome: {release['name']}, Tag: {release['tag_name']}")
# else:
#     print("Impossibile ottenere le release del repository.")
#
# import requests
#
# import requests


def get_github_release_commits(repo_url, release_tag):
    # Estrai il nome del proprietario e del repository dal link
    parts = repo_url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]

    # URL dell'API per ottenere i dettagli dei commit della release
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    # Parametri per filtrare i commit per il tag della release
    params = {
        "sha": release_tag
    }

    # Esegui la chiamata GET all'API di GitHub per ottenere i commit della release
    response = requests.get(api_url, params=params)

    # Verifica se la chiamata è stata eseguita con successo (status code 200)
    if response.status_code == 200:
        commits = response.json()
        return commits
    else:
        print(f"Errore nell'ottenere i commit della release {release_tag}. Codice di stato: {response.status_code}")
        return None


# Esempio di utilizzo della funzione per tutte le release fornite
repo_url = "https://github.com/owner/repository"

# Lista delle release fornite
release_tags = ["v1.4.16", "v1.4.14", "v1.4.13", "v1.4.12", "v1.4.11", "v1.4.10", "v1.4.5", "v1.3.7", "v1.3.5",
                "v1.3.4", "v1.3.3", "v1.2.8", "v1.2.7", "v1.1.16", "v1.1.15", "v1.1.9", "v1.1.8-E21",
                "v1.1.8", "v1.0.3", "v1.0.0", "v0.15.9", "v0.15.8", "v0.15.6", "v0.14.15", "v0.14.6",
                "v0.14.5", "v0.14.2", "v0.13.33", "v0.13.31", "v0.13.30"]

for release_tag in release_tags:
    commits = get_github_release_commits(repo_url, release_tag)

    if commits:
        print(f"Commits per la release {release_tag}:")
        for commit in commits:
            print(f"- SHA: {commit['sha']}, Messaggio: {commit['commit']['message']}")
    else:
        print(f"Nessun commit trovato per la release {release_tag}")
    print("----")

