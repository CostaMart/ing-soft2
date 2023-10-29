import subprocess
import sys
import os
import tkinter as tk
import customtkinter as ctk
from ttkthemes import ThemedTk
from model.Domain import Repository
from .LoadingIcon import RotatingIcon


class StartupPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Ing_soft")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.maxsize(1600,1000)
        
        frame = ctk.CTkFrame(self)
        frame.pack(fill = ctk.BOTH)       
        
        img = RotatingIcon(frame, "resources\\rotationLoading.png", backgroundColor= "#2b2b2b")
        img.pack()
        
        
        frame2 = ctk.CTkFrame(self)
        frame2.pack(pady = 40, fill= ctk.BOTH)
        label = ctk.CTkLabel(frame2, text= "this tool uses git, \n you need to install git on your device an make it executable from command line")
        label.pack()
        
        
    
            
            
            
       
            
        
        
        self.testRepoList = []
        
        # Avvia il ciclo principale dell'applicazione
        self.mainloop()
        

