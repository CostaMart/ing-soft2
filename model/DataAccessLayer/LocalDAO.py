import os
import subprocess


class LocalDAO:

    def trova_classi_java(self, directory):
        """Metodo che trova tutte le classi di un progetto java"""
        lista_classi = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".java"):
                    lista_classi.append(os.path.join(root, file))
        return lista_classi

    def getRepoInfoFromGit(self):
        """Ottieni le informazioni del repository dal sistema Git."""
        current_directory = os.getcwd()

        os.chdir("repository")
        repoDir = subprocess.check_output(["dir"]).decode("utf-8")
        repoDir = os.path.join(current_directory, "repository", repoDir).replace("\n", "")
        checkDir = os.path.join(current_directory, "repository")

        if os.getcwd() == checkDir:
            os.chdir(repoDir)
            result = subprocess.check_output(["git", "remote", "show", "origin"]).decode("utf-8")
            os.chdir(current_directory)
            print(os.getcwd())

            firstLine = result.split("\n")[1]
            name = firstLine.split("/")[-2]
            repoName = firstLine.split("/")[-1]
            return name, repoName

        os.chdir(current_directory)
        return None, None

    def cloneRepository(self, url):
        """Clona il repository usando il comando 'git clone'."""
        try:
            subprocess.call(['git', 'clone', url])
            # Esegui eventuali operazioni aggiuntive dopo il clone, se necessario
        except Exception as e:
            # Gestisci eccezioni in caso di fallimento del clone
            print(f"Errore durante il clone del repository: {e}")