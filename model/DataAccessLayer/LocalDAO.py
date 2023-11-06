import os
import subprocess
from icecream import ic
import shutil
import stat

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
        
        os.chdir("repository")
        result = subprocess.check_output(["git", "remote", "show", "origin"]).decode("utf-8")
        firstLine = result.split("\n")[1]
        name = firstLine.split("/")[-2]
        repoName = firstLine.split("/")[-1]
        os.chdir("..")
        return name, repoName
           
        

    def cloneRepository(self, url):
        """Clona il repository usando il comando 'git clone'."""
        
        def on_rm_error( func, path, exc_info):
            os.chmod(path, stat.S_IWRITE)
            os.unlink( path )
        
        
        shutil.rmtree( "repository", onerror = on_rm_error )
            
        try:
            subprocess.call(['git', 'clone', url, "repository"])
            
        except Exception as e:
            # Gestisci eccezioni in caso di fallimento del clone
            print(f"Errore durante il clone del repository: {e}")
        
      

        


        