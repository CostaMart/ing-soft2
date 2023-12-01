import multiprocessing
import time
import unittest
from time import sleep
from unittest.mock import patch, MagicMock

from backend.start_endpoint import ComputationEndpoint
from model.ComputingEndpointModel import ComputingEndpointModel


class TestComputingEndpointModel(unittest.TestCase):
    model = None

    @classmethod
    def setUpClass(cls):
        # Create the ComputingEndpointModel object at the beginning of each test
        cls.model = ComputingEndpointModel()
        cls.model.activateLocal()
        sleep(3)

    @classmethod
    def tearDownClass(cls):
        # Destroy the ComputingEndpointModel object at the end of each test
        cls.model.destroy()


    def test_is_active_local(self):
        # Act
        verifier = self.model.isActiveLocal()

        # Assert
        self.assertEqual(verifier, True)

    def test_is_active_local_raises_exception(self):
        # Arrange - Manually replace the parent_conn attribute with a MagicMock
        original_parent_conn = self.model.parent_conn
        self.model.parent_conn = MagicMock()
        self.model.parent_conn.recv.side_effect = Exception("Errore di connessione")

        # Act
        is_active = self.model.isActiveLocal()

        # Assert
        self.assertEqual(is_active, False)  # The method should return False if an exception is raised

        # Revert the change
        self.model.parent_conn = original_parent_conn

    def test_send_message_to_endpoint_valid_message(self):
        # Act
        self.model.sendMessageToEndpoint({"fun": "ping", "num1": 1, "num2": 2})
        time.sleep(1)  # Give the process time to handle the message

        message = self.model.receiveMessageFromEndpoint()
        self.assertEqual(message, 3)

    def test_send_message_to_endpoint_invalid_message(self):


        self.model.sendMessageToEndpoint("a")
        message = self.model.receiveMessageFromEndpoint()
        self.assertEqual(
            "Errore: il messaggio deve essere un dizionario che contiene il parametro 'fun' per specificare la funzione.",
            message)
