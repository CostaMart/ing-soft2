

import os
import subprocess
from model.RepositoryRepo import RepoRepository

def isGitInstalled():
    """ return false if git is not installed or not executable from console, returns true and version if everything is ok """    
    result = subprocess.run("git --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if("git version" in result.stdout):
            return True, result.stdout
    else: 
        return False
    
def RepoData():
    model = RepoRepository()
    _CheckRepoDir()
  
    result = subprocess.check_output(["git", "remote", "show", "origin"], cwd="repository").decode("utf-8")
   
    firstLine = result.split("\n")[1]
    name = firstLine.split("/")[-2]
    repoName = firstLine.split("/")[-1]
    repodata = model.getRepoByNameeAuthor(name, repoName)
    
    return repodata
   
    
        
def _CheckRepoDir():
    if not os.path.exists("repository"):
        try:
            os.makedirs("repository")
        except OSError as e:
            print(f"Errore durante la creazione della cartella: {e}")
    else:
        return

