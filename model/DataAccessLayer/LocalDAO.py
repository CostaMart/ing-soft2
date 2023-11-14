from datetime import datetime
import os
import subprocess
from icecream import ic
import shutil
import stat
import git
import pandas as pd
from pydriller import Repository, Commit
from model.repo_utils import get_commits, repo_to_use


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

        def on_rm_error(func, path, exc_info):
            os.chmod(path, stat.S_IWRITE)
            os.unlink(path)

        shutil.rmtree("repository", onerror=on_rm_error)

        try:
            subprocess.call(['git', 'clone', url, "repository"])

        except Exception as e:
            # Gestisci eccezioni in caso di fallimento del clone
            print(f"Errore durante il clone del repository: {e}")

    def _class_exists_in_commit(self, commit, class_name):
        try:
            tree = commit.tree
            file_blob = tree[class_name]
            return True
        except KeyError:
            return False

    def get_commits_with_class(self, class_name, repo_path):
        """ recupera nel repo specificato una lista dei commit in cui era presente la calsse dal nome passato come parametro """

        repo = git.Repo(repo_path)
        commit_list = []

        for commit in repo.iter_commits():

            if self._class_exists_in_commit(commit, class_name):
                commit_list.append(commit)

        return commit_list

    def extract_years_from_commits(self, folder="repository"):
        """ ritorna una lista di tutti gli anni in cui è stato effettuato almeno un commit """
        repo = repo_to_use(folder)

        years = set()

        for commit in get_commits(repo):
            commit_date = commit.committer_date
            year = commit_date.year
            years.add(year)
            # Converti il set in una lista e restituiscila
        ordered_list = list(years)
        ordered_list.sort()
        return ordered_list

    def getClassListFromGivenCommit(self, commit_hash, repo_path="repository"):
        repo = git.Repo(repo_path)
        commit = repo.commit(commit_hash)
        dict_file = set()
        albero_commit = commit.tree
        for blob in albero_commit.traverse():
            if isinstance(blob, git.Blob) and ".java" in blob.path:
                dict_file.add(blob.path.split("/")[-1])

        return dict_file

    def dataCommitLinkYear(self, year, rep="repository"):
        """Metodo che prende tutti i commit con relativa data in base all'anno e li inserisce in un dataframe che ritorna"""
        year = int(year)
        return list(Repository(rep, since=datetime(year, 1, 1), to=datetime(year, 12, 31)).traverse_commits())

    def getCommit(self, hash: str, rep: str = "repository") -> Commit:
        return next(Repository(rep, single=hash).traverse_commits())

    def getCommitsFromDate(self, date: datetime, yearToArrive, repo):
        return list(Repository(repo, since=date, to=datetime(int(yearToArrive), 12, 31)).traverse_commits())

    def getCommitInInterval(self, start_commit, end_commit, repo_path="repository"):
        # oggetto Repository
        repo = Repository(repo_path)

        # Dizionario per salvare i commit nell'intervallo
        commits_in_range = {}

        # Itera attraverso tutti i commit nel repository nell'intervallo specificato
        for commit in repo.traverse_commits():
            if start_commit and commit.hash == start_commit:

                start_commit = None

            if not start_commit:

                commits_in_range[commit.hash] = {
                    "hash": commit.hash,
                    "date": commit.committer_date
                }

            if end_commit and commit.hash == end_commit:
                break

        return commits_in_range
