import subprocess

def run_tests(test_paths):
    for path in test_paths:
        # Esegui i test uno alla volta
        cmd = ["pytest", "-s", path, "--verbose", "--color=yes"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Stampa l'output dei test
        print(result.stdout)

        # Se ci sono errori nei test, stampa l'output di errore
        if result.returncode != 0:
            print(result.stderr)
            return result.returncode  # Termina immediatamente se un test fallisce

    # Tutti i test sono stati eseguiti con successo
    return 0

if __name__ == "__main__":
    test_paths = [
        "Testing/WhiteBoxTesting/DataAccessLayerTesting/LocalDAOTesting.py",
        "Testing/WhiteBoxTesting/ControllerLogicTesting/MainPageControllerTest.py",
        "Testing/WhiteBoxTesting/ModelTesting/LocalRepoModelTestingWhiteBox.py",
        "Testing/WhiteBoxTesting/ModelTesting/RepoModelTest.py",
        "Testing/WhiteBoxTesting/DataAccessLayerTesting/DAORepoTesting.py",
        "Testing/WhiteBoxTesting/ModelTesting/ComputingEndpointModelTest.py",
        "Testing/WhiteBoxTesting/ControllerLogicTesting/ProjectMetricsControllerTest.py",
    ]

    run_tests(test_paths)


    test_paths_1=["ooTest.py"]

    exit_code = run_tests(test_paths_1)

    # Termina lo script con il codice di ritorno dei test
    exit(exit_code)