import shutil
import threading
import time
import unittest
import sys
import os
import git
from icecream import ic

directory_corrente = os.path.abspath(os.path.dirname(__file__))

divided = ic(directory_corrente.split(os.sep))
final = []

for division in divided:
    if division == "ing-soft2":
        break
    final.append(division)
final.append("ing-soft2")
final_dir = os.sep.join(final)
ic(final_dir)
sys.path.append(final_dir)


from controller.StartAppContoller import StartAppController
from unittest.mock import patch, Mock
import tkinter as tk
from model.LocalRepoModel import LocalRepoModel
from model.ComputingEndpointModel import ComputingEndpointModel
import subprocess as sub
from git import Repo
from multiprocessing.connection import Connection


class myConnectionDriver:
    """imita il comportamento di Connection, non di interesse in questo test"""

    def send(self, msg):
        return

    def recv(self):
        return "destroy request ok"

    def close():
        return True


class StartAppControllerIT(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        ic("ready")
        """setup repoModel"""
        self.globalModel = LocalRepoModel()
        directory_path = "repository"
        ic(directory_path)
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            os.mkdir(directory_path)

        self.globalModel.createLocalRepo(
            "https://github.com/CostaMart/Prova-per-ing-soft.git"
        )
        self.globalModel.RepoDataUpdate()

        # init computationModel

        self.comp = ComputingEndpointModel()
        self.comp.child_conn = myConnectionDriver()
        self.comp.parent_conn = myConnectionDriver()

    # da qui testing per l'integrazione con localRepoModel

    def test_localRepoModel_cls1(self):
        return
        # dovrebbe testare repodataupdate ma continua a tornare errore 404

    # da qui test per compute endpoint
    def test_computeEndpoint_cls1(self):
        controller = StartAppController()
        # chiamata sotto test
        value = controller.isComputeEndpointActive()
        self.assertIsNotNone(value)
        return

    def test_computeEndpoint_cls2(self):
        mock = Mock(return_value=3)
        mockProcess = Mock()
        mockProcessStart = Mock()
        with patch(
            "integrationTesting.controller_modelIT.StartAppControllerIT.myConnectionDriver.recv",
            mock,
        ), patch("multiprocessing.Process", mockProcess), patch(
            "multiprocessing.Process.start", mockProcessStart
        ):
            controller = StartAppController()
            # chiamata sotto test
            active = controller.startComputationEndpoint()
            self.assertEqual(active, "local")
            return

    def test_computeEndpoint_cls3(self):
        mock = Mock()

        with patch("model.ComputingEndpointModel.ComputingEndpointModel.destroy", mock):
            controller = StartAppController()
            controller.ComputeEnd = self.comp

            # chiamata sotto test
            closingResult = controller.closeSubProcess()
            mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
