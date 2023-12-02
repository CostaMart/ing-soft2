import os
import random
import string
import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock, patch
import git
from model.DataAccessLayer.DAORepo import DAORepo
from model.DataAccessLayer.LocalDAO import LocalDAO

import os
import shutil
import subprocess
import unittest
from model.DataAccessLayer.LocalDAO import LocalDAO

import os
import shutil
import subprocess
import unittest
from model.DataAccessLayer.LocalDAO import LocalDAO


class FakeCommit:
    def __init__(self):
        self.tree = {}


class TestLocalDAO(unittest.TestCase):
    test_directory = None

    @classmethod
    def setUpClass(cls):
        # Questo metodo verrà eseguito una sola volta prima di tutti i test
        # Configura l'ambiente di test
        cls.test_directory = "repository"
        os.makedirs(cls.test_directory, exist_ok=True)
        # Configura l'ambiente di test, ad esempio, creando una directory di test
        os.makedirs("test_project", exist_ok=True)
        # test di clone del repository
        local_dao = LocalDAO()
        daoRepo = DAORepo()
        url_repo = daoRepo.getRepoList("java")[0].url
        local_dao.cloneRepository(url_repo)
        cloned_files = os.listdir("repository")
        assert cloned_files, "La directory 'repository' non è vuota dopo il clone"

    @classmethod
    def tearDownClass(cls):
        # Esegue il tearDown finale dell'intero ambiente
        shutil.rmtree("test_project", ignore_errors=True)
        # rimozione della directory repository
        shutil.rmtree("repository",ignore_errors = True)

    def test_findJavaClass(self):
        local_dao = LocalDAO()
        # Crea alcuni file nella directory di test
        open(os.path.join("test_project", "file1.java"), "w").close()
        open(os.path.join("test_project", "file2.java"), "w").close()
        result = local_dao.findJavaClass("test_project")
        self.assertTrue(result)
        self.assertIn("file1.java", result)
        self.assertNotIn("file2.py", result)

    def test_getRepoInfoFromGit(self):
        local_dao = LocalDAO()
        # Assicurati che ci sia un repository Git nella directory "repository"
        subprocess.call(['git', 'init', 'repository'], stdout=subprocess.PIPE)
        result = local_dao.getRepoInfoFromGit()
        self.assertTrue(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_class_exists_in_commit(self):
        local_dao = LocalDAO()

        # Simula un oggetto commit e verifica che una classe specifica esista
        class_name = "MyClass.java"
        fake_commit = FakeCommit()
        fake_commit.tree["MyClass.java"] = "dummy content"

        result = local_dao._class_exists_in_commit(fake_commit, class_name)
        self.assertTrue(result, f"La classe {class_name} dovrebbe esistere nel commit.")

    @patch('model.DataAccessLayer.LocalDAO.Repository', autospec=True)
    def test_getCommitsFromDate(self, mock_repository):
        local_dao = LocalDAO()

        # Simula alcuni commit con date specifiche
        commit_2022 = MagicMock()
        commit_2022.committer_date = datetime(2022, 1, 1)
        commit_2023 = MagicMock()
        commit_2023.committer_date = datetime(2023, 1, 1)

        # Configura il mock per restituire i commit simulati
        mock_repository.return_value.traverse_commits.return_value = [commit_2022, commit_2023]

        # Esegui il test
        result = local_dao.getCommitsFromDate(datetime(2022, 1, 1), 2023, 'repository')

        # Stampa i commit per debug
        print("Commits in result:", result)

        self.assertEqual(len(result), 2, "Il numero di commit dovrebbe essere 2.")
        self.assertIn(commit_2022, result, "Il commit per l'anno 2022 dovrebbe essere presente nella lista.")
        self.assertIn(commit_2023, result, "Il commit per l'anno 2023 dovrebbe essere presente nella lista.")

    @patch('model.DataAccessLayer.LocalDAO.Repository', autospec=True)
    def test_dataCommitLinkYear(self, mock_repository):
        local_dao = LocalDAO()

        # Simula alcuni commit con date specifiche
        commit_2022 = MagicMock()
        commit_2022.committer_date = datetime(2022, 1, 1)
        commit_2023 = MagicMock()
        commit_2023.committer_date = datetime(2023, 1, 1)

        # Configura il mock per restituire i commit simulati
        mock_repository.return_value.traverse_commits.return_value = [commit_2022, commit_2023]

        # Esegui il test
        result = local_dao.dataCommitLinkYear('main', 2022, 'repository')

        # Stampa i commit per debug
        print("Commits in result:", result)

        self.assertEqual(len(result), 2, "Il numero di commit dovrebbe essere 2.")
        self.assertIn(commit_2022, result, "Il commit per l'anno 2022 dovrebbe essere presente nella lista.")
        self.assertIn(commit_2023, result, "Il commit per l'anno 2023 dovrebbe essere presente nella lista.")

    @patch('model.DataAccessLayer.LocalDAO.Repository', autospec=True)
    def test_getCommit(self, mock_repository):
        local_dao = LocalDAO()

        # Simula un commit con hash specifico
        commit_hash = '123456789abcdef'
        commit = MagicMock()
        commit.hash = commit_hash

        # Configura il mock per restituire il commit simulato
        mock_repository.return_value.traverse_commits.return_value = [commit]

        # Esegui il test
        result = local_dao.getCommit(commit_hash, 'repository')

        # Stampa il commit per debug
        print("Commit in result:", result)

        self.assertEqual(result, commit, "Il commit restituito dovrebbe essere quello simulato.")

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommit_valid_commit_in_repo(self, mock_Repository):
        # Configurare il mock per restituire un commit valido
        mock_commit = MagicMock()
        mock_commit.hash = "hash1"
        mock_Repository.return_value.traverse_commits.return_value = [mock_commit]

        # Eseguire il test
        local_dao = LocalDAO()
        result = local_dao.getCommit("hash1", "repository_with_commits")

        # Verificare il risultato
        self.assertEqual(result, mock_commit)

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommit_valid_commit_not_in_repo(self, mock_Repository):
        # Configurare il mock per restituire un repository vuoto
        mock_Repository.return_value.traverse_commits.return_value = []

        # Eseguire il test
        local_dao = LocalDAO()

        with self.assertRaises(ValueError):
            local_dao.getCommit("hash2", "empty_repository")

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommit_invalid_commit_hash(self, mock_Repository):
        # Configurare il mock per restituire un commit valido
        mock_commit = MagicMock()
        mock_commit.hash = "hash1"
        mock_Repository.return_value.traverse_commits.return_value = [mock_commit]

        # Eseguire il test
        local_dao = LocalDAO()

        with self.assertRaises(ValueError):
            local_dao.getCommit("invalid_hash", "repository_with_commits")

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommit_missing_commit_hash(self, mock_Repository):
        # Configurare il mock per restituire un commit valido
        mock_commit = MagicMock()
        mock_commit.hash = "hash1"
        mock_Repository.return_value.traverse_commits.return_value = [mock_commit]

        # Eseguire il test
        local_dao = LocalDAO()

        with self.assertRaises(ValueError):
            local_dao.getCommit("", "repository_with_commits")

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommit_empty_repository(self, mock_Repository):
        # Configurare il mock per restituire un repository vuoto
        mock_Repository.return_value.traverse_commits.return_value = []

        # Eseguire il test
        local_dao = LocalDAO()

        with self.assertRaises(ValueError):
            local_dao.getCommit("hash3", "empty_repository")

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommitsFromDate_valid_date(self, mock_Repository):
        # Configurare il mock per restituire due commit validi
        mock_commit1 = MagicMock()
        mock_commit2 = MagicMock()
        mock_Repository.return_value.traverse_commits.return_value = [mock_commit1, mock_commit2]

        # Eseguire il test
        local_dao = LocalDAO()
        result = local_dao.getCommitsFromDate(datetime(2022, 1, 1), 2023, 'repository_with_commits')

        # Verificare il risultato
        self.assertEqual(len(result), 2)

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommitsFromDate_invalid_date(self, mock_Repository):
        # Configurare il mock per restituire un repository vuoto
        mock_Repository.return_value.traverse_commits.return_value = []

        # Eseguire il test
        local_dao = LocalDAO()

        with self.assertRaises(ValueError):
            local_dao.getCommitsFromDate(datetime(2023, 1, 1), 2023, 'empty_repository')

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommitInInterval_valid_interval(self, mock_Repository):
        # Configurare il mock per restituire due commit validi
        mock_commit1 = MagicMock()
        mock_commit2 = MagicMock()
        mock_commit1.hash = "hash1"
        mock_commit2.hash = "hash2"
        mock_Repository.return_value.traverse_commits.return_value = [mock_commit1, mock_commit2]

        # Eseguire il test
        with patch("model.DataAccessLayer.LocalDAO.Repository", mock_Repository):
            local_dao = LocalDAO()
            result = local_dao.getCommitInInterval("hash1", "hash2", 'repository_with_commits')

        # Verificare il risultato
        self.assertEqual(len(result), 2)
        self.assertIn("hash1", result)
        self.assertIn("hash2", result)

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommitInInterval_invalid_start_commit(self, mock_Repository):
        # Configurare il mock per restituire due commit validi
        mock_commit1 = MagicMock()
        mock_commit2 = MagicMock()
        mock_commit1.hash = "hash1"
        mock_commit2.hash = "hash2"
        mock_Repository.return_value.traverse_commits.return_value = [mock_commit1, mock_commit2]

        # Eseguire il test con start_commit non valido
        with patch("model.DataAccessLayer.LocalDAO.Repository", mock_Repository):
            local_dao = LocalDAO()
            result = local_dao.getCommitInInterval("invalid_hash", "hash2", 'repository_with_commits')
        # Verificare il risultato
        # l'hash finale non lo prende e nemmeno quello iniziale.
        self.assertEqual(len(result), 0)

    @patch("model.DataAccessLayer.LocalDAO.Repository")
    def test_getCommitInInterval_invalid_end_commit(self, mock_Repository):
        # Configurare il mock per restituire due commit validi
        mock_commit1 = MagicMock()
        mock_commit2 = MagicMock()
        mock_commit1.hash = "hash1"
        mock_commit2.hash = "hash2"
        mock_Repository.return_value.traverse_commits.return_value = [mock_commit1, mock_commit2]

        # Eseguire il test con end_commit non valido
        with patch("model.DataAccessLayer.LocalDAO.Repository", mock_Repository):
            local_dao = LocalDAO()
            result = local_dao.getCommitInInterval("hash1", "invalid_hash", 'repository_with_commits')

        # il risultato ha due commit hash1 e hash2 proprio perché parte da hash1 e arriva ad hash2
        self.assertEqual(len(result), 2)
        self.assertIn("hash1", result)
        self.assertIn("hash2", result)

    def test_checkout_existing_branch(self):
        # Verifica il checkout di un branch esistente
        test_instance = LocalDAO()
        repo = git.Repo("repository")
        branches = [str(branch) for branch in repo.branches]
        branch = branches[0]
        test_instance.checkout_to(branch)

    def test_checkout_with_error(self):
        # Simula un errore durante il checkout
        # prova a fare il checkout di un branch che non esiste
        test_instance = LocalDAO()

        with self.assertRaises(subprocess.CalledProcessError):
            branches = self.get_all_branches()
            nonExistentString = self.generate_random_branch_name()
            if nonExistentString in branches:
                nonExistentString = self.generate_random_branch_name()
            test_instance.checkout_to(nonExistentString)

    def get_all_branches(self):
        repo = git.Repo("repository")
        branches = [str(branch) for branch in repo.branches]
        return branches

    def generate_random_branch_name(self, length=10):
        # Genera un nome di branch randomico
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))


if __name__ == '__main__':
    unittest.main()
