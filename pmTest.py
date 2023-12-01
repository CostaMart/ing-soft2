import unittest
import os
import model.process_metrics as pm
import model.repo_utils as ru
from pydriller import Repository
from pandas import DataFrame
import model.spMetrics as sp
class TestMetriche(unittest.TestCase):

    repository = "testingMetriche\\Prova-per-ing-soft"
    repo_fuori = "testingMetriche"
    classe = "azz.java"
    invalidClasse = "104.java"
    invalidFolder = "104"
    file1 = "papa.txt"
    file2 = "angelone.txt"
    commit = "615c5403d94b89eb6380b1832f31afd5caab995a"
    diction = [('615c5403d94b89eb6380b1832f31afd5caab995a', '2023-11-06 16:18:49+01:00'),
 ('cbdd35d610093c131a1f7a03d1b6b4c5ff020bdc', '2023-11-06 16:25:13+01:00'),
 ('b4e3ae581bb983d394e38606a08bb9f172d9f59b', '2023-11-06 16:26:42+01:00')]






    
    ######   INIZIO TESTING PROCESS METRICS   ######
    def test_controlla_numero_revisioni_per_classe(self):
        # Test with valid class name
        result = pm.controlla_numero_revisioni_per_classe(self.classe, folder =self.repository)
        self.assertGreaterEqual(result, 0)
        # Test with invalid class name 
        result = pm.controlla_numero_revisioni_per_classe(self.invalidClasse, folder =self.repository)
        self.assertLessEqual(result, 0)  
        # Test with invalid folder
        result = pm.controlla_numero_revisioni_per_classe(self.classe, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)

    def test_calcola_numero_bug_fix(self):
        result = pm.calcola_numero_bug_fix(folder =self.repository)
        self.assertGreaterEqual(result, 0)
        result = pm.calcola_numero_bug_fix(folder =self.invalidFolder)
        self.assertLess(result, 0)

    def test_calcola_code_churn(self):
        # caso file buoni
        result = pm.calcola_code_churn(ru.trova_file_classe(self.file1, folder=self.repo_fuori), ru.trova_file_classe(self.file2, folder = self.repo_fuori))
        self.assertGreaterEqual(result, 0)
        # caso primo file cattivo
        result = pm.calcola_code_churn(ru.trova_file_classe("nient.txt", folder=self.repo_fuori), ru.trova_file_classe(self.file2, folder =self.repo_fuori))
        self.assertLessEqual(result, 0)
        # caso secondo file cattivo
        result = pm.calcola_code_churn(ru.trova_file_classe(self.file1, folder=self.repo_fuori), ru.trova_file_classe("nient.txt", folder=self.repo_fuori))
        self.assertLessEqual(result, 0)
        # caso entrambi file cattivi
        result = pm.calcola_code_churn(ru.trova_file_classe("nient.txt", folder=self.repo_fuori), ru.trova_file_classe("nient.txt", folder=self.repo_fuori))
        self.assertLessEqual(result, 0)

    def test_calcola_loc(self):
        # tutto buono
        result = pm.calcola_loc(self.classe, folder =self.repository)
        self.assertGreaterEqual(result[0], 0)
        # caso classe cattiva
        result = pm.calcola_loc(self.invalidClasse, folder =self.repository)
        self.assertLessEqual(result, 0)
        # caso cartella cattiva
        result = pm.calcola_loc(self.classe, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)

    def test_calcola_autori_distinti_per_file(self):
        # tutto buono
        result = pm.calcola_autori_distinti_per_file(self.classe, folder =self.repository)
        self.assertGreater(len(result), 0)
        # caso classe cattiva
        result = pm.calcola_autori_distinti_per_file(self.invalidClasse, folder =self.repository)
        self.assertLessEqual(result, 0)
        # caso cartella cattiva
        result = pm.calcola_autori_distinti_per_file(self.classe, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)

    def test_calcola_settimane_file(self):
        # tutto buono
        result = pm.calcola_settimane_file(self.classe, folder =self.repository)
        self.assertGreater(result, 0)
        # caso classe cattiva
        result = pm.calcola_settimane_file(self.invalidClasse, folder =self.repository)
        self.assertLessEqual(result, 0)
        # caso cartella cattiva
        result = pm.calcola_settimane_file(self.classe, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)
    
    ##### FINE TESTING PROCESS METRICS #####
    ##### INIZIO TESTING REPO UTILS ########

    def test_repo_to_use(self):
        result = ru.repo_to_use(self.repository)
        self.assertIsInstance(result, Repository)
        result = ru.repo_to_use(self.invalidFolder)
        self.assertLess(result, 0)

    def test_data_commit(self): 
        result = ru.dataCommit(self.repository)
        self.assertIsInstance(result, DataFrame)
        result = ru.dataCommit(self.invalidFolder)
        self.assertLess(result, 0)

    def test_data_commit_link(self):
        result = ru.dataCommitLink(Repository(self.repository))
        self.assertIsInstance(result, DataFrame)
        result = ru.dataCommitLink("nonrepo")
        self.assertLess(result, 0)

    def test_data_commit_link_year(self):
        result = ru.dataCommitLinkYear(Repository(self.repository), 2023)
        self.assertIsInstance(result, DataFrame)
        result = ru.dataCommitLinkYear("nonrepo", 2023)
        self.assertLess(result, 0)
        result = ru.dataCommitLinkYear(Repository(self.repository), "2025")
        self.assertLess(result, 0)
        result = ru.dataCommitLinkYear("nonrepo", "2025")
        self.assertLess(result, 0)
        result = ru.dataCommitLinkYear(Repository(self.repository), 3001)
        self.assertLess(result, 0)

    def test_trova_file_classe(self):
        result = ru.trova_file_classe(self.classe, self.repository)
        self.assertIsInstance(result, str)
        result = ru.trova_file_classe(self.classe, self.invalidFolder)
        self.assertLess(result, 0)
        result = ru.trova_file_classe(self.invalidClasse, self.repository)
        self.assertIsNone(result)
        result = ru.trova_file_classe(self.invalidClasse, self.invalidFolder)
        self.assertLess(result, 0)

    def test_cerca_file_java(self):
        result = ru.cerca_file_java(self.repository)
        self.assertIsInstance(result, list)
        result = ru.cerca_file_java(self.invalidFolder)
        self.assertLess(result, 0)

    def test_get_commit_date(self):
        result = ru.get_commit_date(self.commit, self.repository)
        self.assertIsInstance(result, str)
        result = ru.get_commit_date(self.commit, self.invalidFolder)
        self.assertIsNone(result)
        result = ru.get_commit_date("nessuno", self.repository)
        self.assertIsNone(result)
        result = ru.get_commit_date("nessuno", self.invalidFolder)
        self.assertIsNone(result)

    def test_extract_years_from_commits(self):
        result = ru.extract_years_from_commits(self.repository)
        self.assertIsInstance(result, list)
        result = ru.extract_years_from_commits(self.invalidFolder)
        self.assertLess(result, 0)

    ###### FINE TESTING REPO UTILS  ########
    ###### INIZIO TESTING SP-METRICS #######
    
    def test_sp_process_metrics(self):
        result = sp.generate_process_metrics(self.classe, self.diction, self.repository)
        self.assertIsInstance(result, DataFrame)
        result = sp.generate_process_metrics(self.invalidClasse, self.diction, self.repository)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.classe, "qualcosanonBuono", self.repository)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.classe, self.diction, self.invalidFolder)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.invalidClasse, 11, self.invalidFolder)
        self.assertLess(result, 0)

    


if __name__ == '__main__':
    unittest.main()
