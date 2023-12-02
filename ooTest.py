import unittest
import multiprocessing
import model.ComputingEndpointModel  as ce
import backend.functionFactory as FunctionFactory
import inspect
from model.FilterProject import  get_all_release_tag_repo
import model.DataAccessLayer.DAORepo as dao
from unittest.mock import patch, Mock
from unittest.mock import patch, MagicMock
import requests

class TestOO(unittest.TestCase):
    #####  functionFactory  ######
    def setUp(self):
            self.factory = FunctionFactory.FunctionFactory()

    def test_getExistingFunction(self):
        # Verifica che la funzione esista nel modulo 'compute'
        funct_name = "generate_metrics"
        function = self.factory.getFunct(funct_name)
        self.assertIsNotNone(function)
        self.assertTrue(inspect.isfunction(function))

    def test_getNonExistingFunction(self):
        # Verifica che la funzione non esista nel modulo 'compute'
        funct_name = "funzione_inesistente"
        function = self.factory.getFunct(funct_name)
        self.assertIsNone(function)
    
    #### Fine functionFactory #####
    #### DAORepo  #################
    @patch('model.DataAccessLayer.DAORepo.DAORepo.get_all_release_tag_repo')
    def test_set_release_tags_success(self, mock_get_all_release_tag_repo):
        # Configura il mock per restituire una lista di tag di release
        mock_tags = ["v1.0.0", "v1.1.0", "v1.2.0"]
        mock_get_all_release_tag_repo.return_value = mock_tags
        dao_repo = dao.DAORepo()
        dao_repo._set_release_tags("owner", "repo_name")
        self.assertEqual(dao_repo.get_all_release_tag_repo(), mock_tags)

    @patch('model.DataAccessLayer.DAORepo.DAORepo.get_all_release_tag_repo')
    def test_set_release_tags_failure(self, mock_get_all_release_tag_repo):
        # Configura il mock per restituire None, simulando un fallimento
        mock_get_all_release_tag_repo.return_value = None
        dao_repo = dao.DAORepo()
        self.assertIsNone(dao_repo._set_release_tags("owner", "repo_name"))

    
    @patch('requests.get')
    def test_getRepoByNameeAuthor_failure(self, mock_requests_get):
        # Configura il mock della risposta HTTP con uno stato diverso da 200
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getRepoByNameeAuthor('repo_owner', 'repo_name')
        self.assertIsNone(result)

    @patch('requests.get')
    def test_getRepoList_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "repo1",
                    "html_url": "https://github.com/repo1",
                    "description": "Description 1",
                },
                {
                    "name": "repo2",
                    "html_url": "https://github.com/repo2",
                    "description": "Description 2",
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        dao_repo = dao.DAORepo()
        result = dao_repo.getRepoList("java")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[1].url, "https://github.com/repo2")
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=java+language:java")

    @patch('requests.get')
    def test_getRepoList_empty_name(self, mock_requests_get):
        dao_repo = dao.DAORepo()
        result = dao_repo.getRepoList("")
        self.assertEqual(result, [])
        mock_requests_get.assert_not_called()

    @patch('requests.get')
    def test_getJavaRepoList_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "repo1",
                    "html_url": "https://github.com/repo1",
                    "description": "Description 1",
                },
                {
                    "name": "repo2",
                    "html_url": "https://github.com/repo2",
                    "description": "Description 2",
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        # Chiamare il metodo getJavaRepoList
        result = your_instance.getJavaRepoList("java")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[1].url, "https://github.com/repo2")
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=java+language:java")

    @patch('requests.get')
    def test_getJavaRepoList_empty_result(self, mock_requests_get):
        # Configura il mock della risposta HTTP con risultato vuoto
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getJavaRepoList("java")
        self.assertEqual(result, [])
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=java+language:java")

    @patch('requests.get')
    def test_get_all_release_tag_repo_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"tag_name": "v1.0.0"},
            {"tag_name": "v1.1.0"},
            {"tag_name": "v1.2.0"},
        ]
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.get_all_release_tag_repo("owner_name", "repo_name")
        self.assertEqual(result, ["v1.0.0", "v1.1.0", "v1.2.0"])
        mock_requests_get.assert_called_once_with("https://api.github.com/repos/owner_name/repo_name/releases")

    @patch('requests.get')
    def test_get_all_release_tag_repo_failure(self, mock_requests_get):
        # Configura il mock della risposta HTTP con errore
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.get_all_release_tag_repo("owner_name", "repo_name")
        self.assertIsNone(result)
        mock_requests_get.assert_called_once_with("https://api.github.com/repos/owner_name/repo_name/releases")

    @patch('requests.get')
    def test_getJavaRepoListForAuthorAndRepo_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "repo1",
                    "html_url": "https://github.com/repo1",
                    "description": "Description 1",
                },
                {
                    "name": "repo2",
                    "html_url": "https://github.com/repo2",
                    "description": "Description 2",
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getJavaRepoListForAuthorAndRepo("author_name", "repo_name")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[1].url, "https://github.com/repo2")
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=user:author_name+repo:repo_name+language:java")

    @patch('requests.get')
    def test_getJavaRepoListForAuthorAndRepo_failure(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getJavaRepoListForAuthorAndRepo("author_name", "repo_name")
        self.assertEqual(result, [])
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=user:author_name+repo:repo_name+language:java")

    @patch('requests.get')
    def test_getRepoListByAuthor_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "repo1",
                    "html_url": "https://github.com/repo1",
                    "description": "Description 1",
                },
                {
                    "name": "repo2",
                    "html_url": "https://github.com/repo2",
                    "description": "Description 2",
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getRepoListByAuthor("author_name")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[1].url, "https://github.com/repo2")
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=user:author_name+language:java")

    @patch('requests.get')
    def test_getRepoListByAuthor_failure(self, mock_requests_get):
        # Configura il mock della risposta HTTP con errore
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        your_instance =dao.DAORepo()
        result = your_instance.getRepoListByAuthor("author_name")
        self.assertEqual(result, [])
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=user:author_name+language:java")
if __name__ == '__main__':
    unittest.main()