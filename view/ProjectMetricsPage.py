import tkinter as tk
from tkinter import font
import customtkinter as ctk
from ttkthemes import ThemedTk
from .widgets.ListBox import ListBox
from model.Domain import Repository
import time
import threading
from controller.mainPageContoller import get_selected_repo, request_for_repos
from view.widgets.LoadingIcon import RotatingIcon


class ProjectMetricsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master)
        ctk.set_appearance_mode("dark")
       
        
        frame = ctk.CTkFrame(self)
        frame.pack(fill = ctk.BOTH)       
        
        
        frame2 = ctk.CTkFrame(self)
        frame2.pack(pady = 40, fill= ctk.BOTH)
        label = ctk.CTkLabel(frame2, text= "buono")
        label.pack()
        
        
        ctk.CTkButton(self).pack()
            
            
            
       
            
        
        
        self.testRepoList = []
        
        # Avvia il ciclo principale dell'applicazione
        
        

