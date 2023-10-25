import subprocess
import os
from git import Repo 
import repo_utils as ru



def ck_metrics_for_single_commit(commit_hash):
    # Questo metodo estrae le metriche del commit scelto
    repo_to_analyze = os.path.abspath('Repository')
    ck_tool = os.path.abspath('ck.jar')
    output_dir = os.path.abspath('output') 

    os.chdir(repo_to_analyze)

    # Verifica se il commit esiste nella repository
    try:
        repo = Repo(repo_to_analyze)
        repo.commit(commit_hash)
    except:
        print(f"Il commit con hash: {commit_hash} non è stato trovato nella repository.")
        return
    
    # Effettua il checkout del commit
    subprocess.call(['git', 'checkout', '-f', commit_hash])
    os.chdir(os.path.dirname(ck_tool))
    subprocess.call(['java', '-jar', 'ck.jar', repo_to_analyze, 'false', '0', 'true', f"{output_dir}/{commit_hash}"])
    ru.delete_garbage(keep="class")