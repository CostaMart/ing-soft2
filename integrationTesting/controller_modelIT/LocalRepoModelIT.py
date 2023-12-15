from datetime import datetime
import shutil
import threading
import time
import unittest
import sys
import os
import git
from icecream import ic

directory_corrente = os.path.abspath(os.path.dirname(__file__))

divided = directory_corrente.split(os.sep)
final = []

for division in divided:
    if division == "ing-soft2":
        break
    final.append(division)
final.append("ing-soft2")
final_dir = os.sep.join(final)
sys.path.append(final_dir)


from controller.ProjectMetricsContoller import ProjectMetricsController
from unittest.mock import patch, Mock
import tkinter as tk
from model.LocalRepoModel import LocalRepoModel
from model.ComputingEndpointModel import ComputingEndpointModel
import subprocess as sub
from git import Repo, Commit
from multiprocessing.connection import Connection


class LocalRepoModelIT(unittest.TestCase):
    # test integrazione con LocalDAO
    def test_LocalDAO_cls1(self):
        # funzione sotto test
        repo = LocalRepoModel()
        self.assertIsNotNone(repo.CRUD)

    @patch("shutil.rmtree")
    @patch("subprocess.call")
    def test_LocalDAO_cls2(self, rmtree: Mock, subP: Mock):
        repo = LocalRepoModel()
        # funzione sotto test
        repo.createLocalRepo("myRepo")
        rmtree.assert_called_once()
        subP.assert_called_once()

    @patch("os.path.abspath")
    @patch("os.walk")
    def test_LocalDAO_cls3(self, walk: Mock, path: Mock):
        path.return_value = "path"
        walk.return_value = [("root", "dirs", ["files.java"])]
        local = LocalRepoModel()
        # funzione sotto test
        value = local.getAllJavaClassProject("repository")
        self.assertIsNotNone(value)

    @patch("git.repo.base.Repo.iter_commits")
    @patch("git.Repo")
    def test_LocalDAO_cls4(self, repo: Mock, iterCommit: Mock):
        class treeDriver:
            def __getitem__(self, index):
                return "commitHash"

        class CommitDriver:
            tree = treeDriver()

        repo.return_value = Repo()
        iterCommit.return_value = [CommitDriver()]

        local = LocalRepoModel()
        # call sotto test
        value = local.getCommitWithClassList("commitHash")
        self.assertEqual(value, iterCommit.return_value)

    @patch("pydriller.Repository.traverse_commits")
    def test_LocalDAO_cls5(self, traverse: Mock):
        class CommitDriver:
            committer_date = datetime(year=2023, month=12, day=23)
            branches = ["branch1", "branch2"]

        traverse.return_value = [CommitDriver()]
        local = LocalRepoModel()
        # call sotto test
        year = local.getYearList()
        self.assertEqual(year, {2023: {"branch1", "branch2"}})

    @patch("git.Tree.traverse")
    @patch("git.Tree")
    @patch("git.objects.commit.Commit.tree")
    @patch("git.objects.commit.Commit")
    @patch("git.repo.base.Repo.commit")
    def test_LocalDAO_cls6(
        self,
        commitfun: Mock,
        repoCommit: Mock,
        commitTree: Mock,
        tree: Mock,
        traverse: Mock,
    ):
        class mYTree:
            def traverse(self):
                return [
                    git.Blob(
                        "local",
                        "12345678901234567890".encode("utf-8"),
                        path="myfile.java",
                    )
                ]

        class myCommitDriver:
            tree = mYTree()

            def be():
                return

        commitfun.return_value = myCommitDriver()
        commitTree.return_value = mYTree()

        local = LocalRepoModel()
        # call site sotto test
        value = local.getClassListFromGivenCommit("commit1")
        self.assertEqual(value, {"myfile.java"})


if __name__ == "__main__":
    unittest.main()
