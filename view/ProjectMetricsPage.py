import tkinter as tk
from tkinter import font
import customtkinter as ctk
from ttkthemes import ThemedTk
from .widgets.ListBox import ListBox
from model.Domain import Repository
import time
import threading
from controller.mainPageContoller import get_selected_repo, request_for_repos
from view.widgets.SideButton import SideButton



class ProjectMetricsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master)
        ctk.set_appearance_mode("dark")
       
        self.master = master
               
        
        
        self.backButton = SideButton(self, self.master.previousPage, side = "left", imgpath="resources\left-arrow.png")
        self.backButton.place(x= -150, y= 10 )
        
        
            
            
            
       
            
        
        
        self.testRepoList = []
        
        # Avvia il ciclo principale dell'applicazione
        
        

