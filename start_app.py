import os
import sys

from controller.StartAppContoller import StartAppController

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from view.App import IngSoftApp
from view.StartupPage import StartupPage

start = StartAppController()

isInstalled, version = start.isGitInstalled()

if isInstalled:
    IngSoftApp(gitv = version)
else:   
    StartupPage()

