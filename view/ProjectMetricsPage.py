import os.path
import tkinter as tk
from tkinter import font
import customtkinter as ctk
from view.widgets.SideButton import SideButton
from view.widgets.Plot import PlotCartesian
from controller.ProjectMetricsContoller import MetricsPageContoller
import tkinter as tk







class ProjectMetricsPage(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master = master)
        ctk.set_appearance_mode("dark")
       
        self.controller = MetricsPageContoller() 
        self.master = master
               
       
        p = PlotCartesian(self, self.controller.getLocalRepoData().name, [1,2,3,4], [1,1,1,1])
        p.pack(fill = "x")
        
        self.but = ctk.CTkButton(self, command= lambda: print(master.repoData) )
        self.but.pack()
        left_arrow = os.path.join("resources","left-arrow.png")
        
        self.backButton = SideButton(self, self.master.previousPage, side = "left", imgpath=left_arrow)
        self.backButton.place(x= -150, y= 10 )
            
        
        
        
        
        # Avvia il ciclo principale dell'applicazione
        
        

