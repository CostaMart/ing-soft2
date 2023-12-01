import unittest
import os
import model.process_metrics as pm
import model.repo_utils as ru
class TestMetriche(unittest.TestCase):

    repository = "testingMetriche\\Prova-per-ing-soft"
    classe = "azz.java"
    invalidClasse = "104.java"
    invalidFolder = "104"
    file1 = "papa.txt"
    file2 = "angelone.txt"
    
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
        result = pm.calcola_code_churn(ru.trova_file_classe(self.file1, folder=self.repository), ru.trova_file_classe(self.file2, folder = self.repository))
        self.assertGreaterEqual(result, 0)
        # caso primo file cattivo
        result = pm.calcola_code_churn(ru.trova_file_classe("nient.txt", folder=self.repository), ru.trova_file_classe(self.file2, folder =self.repository))
        self.assertLessEqual(result, 0)
        # caso secondo file cattivo
        result = pm.calcola_code_churn(ru.trova_file_classe(self.file1, folder=self.repository), ru.trova_file_classe("nient.txt", folder=self.repository))
        self.assertLessEqual(result, 0)
        # caso entrambi file cattivi
        result = pm.calcola_code_churn(ru.trova_file_classe("nient.txt", folder=self.repository), ru.trova_file_classe("nient.txt", folder=self.repository))
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

    def test


if __name__ == '__main__':
    unittest.main()
