import tkinter as tk
from tkinter import font, Toplevel
import customtkinter as ctk
from ttkthemes import ThemedTk
from .widgets.ListBox import ListBox
from model.Domain import Repository
import time
import threading
from controller.mainPageContoller import get_selected_repo, request_for_repos
from view.widgets.LoadingIcon import RotatingIcon
from view.ProjectMetricsPage import ProjectMetricsPage
from view.main import MainPage

class IngSoftApp(ctk.CTk):
    
    """ main page dell'app """
    def __init__(self, gitv):
        
        self.testRepoList = []
        self.pageStack = []
        
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        self.title("Ing_soft")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.maxsize(1600,1000)
        
       
        
        # Avvia il ciclo principale dell'applicazione
        newPage = MainPage(self, gitv= gitv)
        self.pageStack.append(newPage)
        newPage.place(relwidth = 1, relheight = 1, rely = 0, relx = 0)
        
        self.mainloop()
        
    def newPage(self, newPage):
        """"add a new page to the stack"""
        page = newPage(self)
        page.place(relwidth = 1, relheight = 1, rely = 0, relx = 1)
        self._pageTransitionAnimation(self.pageStack[-1], page, 0)
        self.pageStack[-1].destroy()
        
        self.pageStack.append(page)  
               
    def _pageTransitionAnimation(self, leftPage, rigPage, l):
        
        while(l < 1):
            
            leftPage.place(relwidth = 1, relheight = 1, relx = -l)
            rigPage.place(relwidth = 1, relheight = 1, relx = 1 - l)
            l = l + 0.1
            time.sleep(0.01)
            self.update()
        l= 1
        
        leftPage.place(relwidth = 1, relheight = 1, rely = 0, relx = -l)
        rigPage.place(relwidth = 1, relheight = 1, rely = 0, relx = 1 - l)
       
        
            