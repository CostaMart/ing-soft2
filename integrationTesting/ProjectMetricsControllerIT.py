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


from controller.mainPageContoller import MainPageController
from unittest.mock import patch, Mock
import tkinter as tk
from model.LocalRepoModel import LocalRepoModel
import subprocess as sub
from git import Repo
