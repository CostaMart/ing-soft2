import os
import subprocess


class LocalDAO:

    def findJavaClass(self, directory):
        """Metodo che trova tutte le classi di un progetto java"""
        """ Questo metodo cerca tutti i file java in una cartella e ne restituisce una lista di nomi di file """
        risultati = []
        cartella = os.path.abspath(directory)

        for root, dirs, files in os.walk(cartella):
            for file in files:
                if file.endswith(".java") or file.endswith(".py"):
                    risultati.append(file)

        return risultati

    def getRepoInfoFromGit(self):
        """Ottieni le informazioni del repository dal sistema Git."""
        current_directory = os.getcwd()

        os.chdir("repository")
        repoDir =os.listdir()[0]
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


        