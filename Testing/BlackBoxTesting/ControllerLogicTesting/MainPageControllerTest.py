import os
import shutil
import unittest
from unittest.mock import MagicMock, patch, Mock, create_autospec
from typing import List, Callable
import requests
from git import Repo
import git
from git import Reference

from controller.mainPageContoller import MainPageController
from model.LocalRepoModel import LocalRepoModel


class TestMainPageController(unittest.TestCase):
    test_directory = None
    repo_url = None
    controller = None
    branches_size = None

    @classmethod
    def setUpClass(cls):
        # Inizializza una nuova istanza di MainPageController prima di ogni test
        cls.controller = MainPageController()
        repoName = 'flatpack'
        url = f"https://api.github.com/search/repositories?q={repoName}+language:java"
        response = requests.get(url)
        risultati = response.json()["items"]
        cls.repo_url = risultati[0]["html_url"]
        cls.test_directory = "repository"
        os.makedirs(cls.test_directory, exist_ok=True)


    @classmethod
    def tearDownClass(cls):
        # shutil.rmtree("repository", ignore_errors=True)
        pass

    def setUp(self):
        pass

    def test_getAllJavaClassByLocalRepoModel(self):
        # Verifica che il metodo restituisca una lista di classi Java
        classes = self.controller.getAllJavaClassByLocalRepoModel(rootDirectory='repository')
        self.assertIsInstance(classes, list)


    def test_get_status_code_from_local_model(self):
        # Mocking the globalModel and its get_status_code method
        mock_global_model = MagicMock()
        mock_global_model.get_status_code.return_value = 200

        # Mocking the CRUDRepo and its last_http_response attribute
        mock_crud_repo = MagicMock()
        mock_crud_repo.last_http_response = 200

        # Creating an instance of MainPageController with the mocked objects
        controller = MainPageController()
        controller.globalModel = mock_global_model
        controller.repoModel.CRUD = mock_crud_repo

        # Calling the method to test
        result = controller.getStatusCodeFromLocalModel()

        # Asserting that the result is expect
        self.assertEqual(result, 200)

    # test for method requestRepoUpdate()

    def test_no_callbacks(self):
        # Arrange
        repo_updater = MagicMock()
        controller = MainPageController()
        controller.globalModel.RepoDataUpdate = repo_updater

        # Act
        controller.requestRepoUpdate()

        # Assert
        repo_updater.assert_called_once()

    def test_only_callback_before_A(self):
        cb = MagicMock()
        self.controller.requestRepoUpdate(callbackBefore=cb)
        cb.assert_called_once()

    def test_only_callbacks_B(self):
        callback = MagicMock()
        self.controller.requestRepoUpdate(callbackBefore=callback)
        # attendi thread
        callback.assert_called()

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    def test_checkRepo(self, mock_exists, mock_isdir):
        # Verifica che il metodo restituisca True se il percorso .git esiste ed è una directory
        result = self.controller.checkRepo()
        self.assertTrue(result)

    @patch('os.path.exists', return_value=False)
    @patch('os.path.isdir', return_value=False)
    def test_checkRepo_not_exists(self, mock_exists, mock_isdir):
        # Verifica che il metodo restituisca False se il percorso .git non esiste o non è una directory
        result = self.controller.checkRepo()
        self.assertFalse(result)

    def test_B_requestRepoUpdate(self):
        # Verifica che la variabile sia False all'inizio
        self.assertFalse(self.controller.update_in_progress)

        # callback di esempio
        callback_before_mock = lambda: print("Callback Before")
        callback_after_mock = lambda: print("Callback After")

        # Chiama il metodo di test
        self.controller.requestRepoUpdate(callback_before_mock, callback_after_mock)

        # Verifica che la variabile sia True durante l'esecuzione
        self.assertTrue(self.controller.update_in_progress)

        # Aspetta che l'aggiornamento abbia completato l'esecuzione
        while self.controller.update_in_progress:
            pass

        # Verifica che la variabile sia tornata a False dopo l'esecuzione
        self.assertFalse(self.controller.update_in_progress)

    # Test per request_for_repos
    def test_request_for_repos_category_A(self):
        # Categoria A: Query senza attributi (es. "python")
        callback_mock = MagicMock()
        self.controller.request_for_repos("python", callback_mock)

        # Verifica che la variabile sia True durante l'esecuzione
        self.assertTrue(self.controller.is_request_for_repos_executing())

        # Aspetta che l'aggiornamento abbia completato l'esecuzione
        while self.controller.is_request_for_repos_executing():
            pass

        # Verifica che la callback sia stata chiamata
        callback_mock.assert_called_once()

    def test_request_for_repos_category_B(self):
        # Categoria B: Query con attributo "author" (es. "author:john")
        callback_mock = MagicMock()
        self.controller.request_for_repos("author:john", callback_mock)

        # Verifica che la variabile sia True durante l'esecuzione
        self.assertTrue(self.controller.is_request_for_repos_executing())

        # Aspetta che l'aggiornamento abbia completato l'esecuzione
        while self.controller.is_request_for_repos_executing():
            pass

        # Verifica che la callback sia stata chiamata
        callback_mock.assert_called_once()

    def test_request_for_repos_category_C(self):
        # Categoria C: Query con attributo "repoName" (es. "repoName:example")
        callback_mock = MagicMock()
        self.controller.request_for_repos("repoName:flatpack", callback_mock)
        # Verifica che la variabile sia True durante l'esecuzione
        self.assertTrue(self.controller.is_request_for_repos_executing())

        # Aspetta che l'aggiornamento abbia completato l'esecuzione
        while self.controller.is_request_for_repos_executing():
            pass
        # Verifica che la callback sia stata chiamata
        callback_mock.assert_called_once()

    def test_request_for_repos_category_D(self):
        # Categoria D: Query con entrambi gli attributi author e repoName
        callback_mock = MagicMock()
        self.controller.request_for_repos("author:Appendium repoName:flatpack", callback_mock)

        # Verifica che la variabile sia True durante l'esecuzione
        self.assertTrue(self.controller.is_request_for_repos_executing())

        # Aspetta che l'aggiornamento abbia completato l'esecuzione
        while self.controller.is_request_for_repos_executing():
            pass

        # Verifica che la callback sia stata chiamata
        callback_mock.assert_called_once()

    # Test per get_selected_repo

    def test_A_get_selected_repo_valid_url(self):
        # Categoria A: URL valido
        url = self.repo_url
        result = self.controller.get_selected_repo(url)
        self.assertTrue(result)

    @patch('subprocess.call')
    def test_z_clone_repository_with_invalid_url(self, mock_subprocess_call):
        # Configura il mock per simulare un fallimento durante il clone
        mock_subprocess_call.side_effect = Exception("Invalid URL")

        try:
            self.controller.get_selected_repo("Invalid URL")
        except Exception as e:
            self.assertEqual(str(e), "Invalid URL")


    def test_update_A_branches_with_default_repo(self):

        mock_loadBar = Mock()

        self.controller.update_branches(mock_loadBar)

        mock_loadBar.configure.assert_called_once()
        mock_loadBar.update.assert_called_once()
        repo = git.Repo("repository")
        branches_size = len(repo.branches)
        self.assertEqual(mock_loadBar.step.call_count, branches_size)

    def create_mock_repo_with_branches(self, branch_names):
        mock_references = []
        for name in branch_names:
            mock_reference = Mock()
            mock_reference.name = f"refs/origin/{name}"
            mock_references.append(mock_reference)

        mock_repo_instance = Mock()
        mock_repo_instance.references = mock_references
        return mock_repo_instance

    def test_update_B_branches(self):
        mock_loadBar = Mock()
        # Crea un mock di un repository con i branch specificati
        mock_repo = self.create_mock_repo_with_branches(["branch1", "branch2", "branch3"])
        self.controller.globalModel = MagicMock()
        with patch.object(self.controller.globalModel, 'switch_branch', return_value=True) as switch_branch_mock:
            self.controller.update_branches(mock_loadBar, mock_repo)

        # Verifica che i metodi siano stati chiamati correttamente
        mock_loadBar.configure.assert_called_once()
        mock_loadBar.update.assert_called_once()
        self.assertEqual(mock_loadBar.step.call_count, 3)

    def test_update_C_branches_with_no_branches(self):
        mock_loadBar = Mock()

        # Crea un mock di un repository con i branch specificati
        mock_repo = self.create_mock_repo_with_branches([])
        self.controller.globalModel = MagicMock()
        with patch.object(self.controller.globalModel, 'switch_branch', return_value=True) as switch_branch_mock:
            self.controller.update_branches(mock_loadBar, mock_repo)

        # Verifica che i metodi siano stati chiamati correttamente
        mock_loadBar.configure.assert_not_called()
        mock_loadBar.update.assert_not_called()
        self.assertEqual(mock_loadBar.step.call_count, 0)



if __name__ == '__main__':
    unittest.main()