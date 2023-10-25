import git_ck
import os

folder = "Repository"

def check_repo():
#   Metodo che controlla se il progetto da analizzare è presente
    if os.path.exists(folder):
        content = os.listdir(folder)
        if content is not None:
            return 0
    else:
        git_ck.clone_repo()


def check_folder():
    # Metodo che controlla se la cartella di output è presente
    if not os.path.exists("output"):
        path = os.path.join("output")
        os.mkdir(path)