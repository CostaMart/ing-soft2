

import subprocess


def isGitInstalled():
    """ return false if git is not installed or not executable from console, returns true and version if everything is ok """    
    result = subprocess.run("git --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if("git version" in result.stdout):
            return True, result.stdout
    else: 
        return False
    
