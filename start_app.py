import sys
import os
import tkinter as tk
import customtkinter as ctk
from ttkthemes import ThemedTk
from model.Domain import Repository
from controller.StartAppContoller import StartAppController
from icecream import ic
import time

if __name__ == "__main__":
    
    

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    from view.App import IngSoftApp
    from view.StartupPage import StartupPage

    start = StartAppController()


    status = start.startComputationEndpoint()
    time.sleep(5)


    isInstalled, version = start.isGitInstalled()
    response = start.isComputeEndpointActive()


    if isInstalled:
        IngSoftApp(gitv = version, endpointStatus = status)
    else:   
        StartupPage()
    

