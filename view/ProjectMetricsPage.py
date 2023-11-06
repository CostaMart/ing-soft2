import os.path
from tkinter import ttk

import customtkinter as ctk
from view.widgets.SideButton import SideButton
from view.widgets.Plot import PlotCartesian
from controller.ProjectMetricsContoller import ProjectMetricsController
import tkinter as tk
from icecream import ic
from .ControllerFalso import ControllerFalso

from .widgets.Graphics.GridView import GridView


from icecream import ic
import model.repo_utils as ru


class ProjectMetricsPage(ctk.CTkScrollableFrame):
    
    def __init__(self, master, debug = False):
        super().__init__(master = master)
        self.grid_frame = None  # Aggiungi una variabile per tenere traccia del frame della griglia
        ctk.set_appearance_mode("dark")
        
        if debug == True:
            self.controller = ControllerFalso()
            self.repoData = self.controller.getLocalRepoData()
        else:
            self.controller = ProjectMetricsController() 
            self.repoData = self.controller.getLocalRepoData()
            self.master = master

        self.initTopFrames()
        self.externalProjectFrame.pack(pady = 12)
        
        self.initOptionFrame()
        self.optionFrameOut.pack(side = ctk.RIGHT, padx = 20, fill= "y", expand = True)


        self.but = ctk.CTkButton(self, command= lambda: print(master.repoData) )
        self.but.pack()
        left_arrow = os.path.join("resources","left-arrow.png")
        
        self.backButton = SideButton(self, self.master.previousPage, side = "left", imgpath=left_arrow)
        self.backButton.place(x= -150, y= 10 )
        
        


# ----------------------------- GESTIONE UI METHODS -----------------------------        
    def initTopFrames(self):
        my_font = ctk.CTkFont(weight= "bold", size= 16)
        my_font_big =  ctk.CTkFont(weight= "bold", size= 20)
        self.externalProjectFrame = ctk.CTkFrame(self)
        self.label = ctk.CTkLabel(self.externalProjectFrame, text= str(self.repoData.name).upper(), font = my_font_big)
        self.label.pack(pady = 2, anchor = "w")
        

        self.internalFrame = ctk.CTkFrame(self.externalProjectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.internalFrame.pack(side = ctk.LEFT)
        self.projectFrame = ctk.CTkFrame(self.internalFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.projectFrame.pack(pady= 10, padx = 10)
        
        
        self.subFrame1 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame1.pack(anchor = "w", padx = 10)
        self.label = ctk.CTkLabel(self.subFrame1, text= f"Git URL: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame1, text= f"{self.repoData.git_url}")
        self.label.pack()
        
        self.subFrame2 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame2.pack(anchor = "w", padx = 10)
        self.label = ctk.CTkLabel(self.subFrame2, text= f"project license: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        
        license = "None"
        if self.repoData.license != None:
            license = self.repoData.license['name']
        
        self.label = ctk.CTkLabel(self.subFrame2, text= f"{license}")
        self.label.pack()
            
        self.subFrame3 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame3.pack(anchor = "w", padx = 10)
        self.label = ctk.CTkLabel(self.subFrame3, text= f"Repo owner: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame3, text= f"r{self.repoData.owner['login']}")
        self.label.pack()
        self.subFrame4 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame4.pack(anchor = "w", padx = 10)
        self.label = ctk.CTkLabel(self.subFrame4, text= f"Repo owner URL: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame4, text= f"{self.repoData.owner['url']}")
        self.label.pack()

    def initOptionFrame(self):
        self.optionFrameOut = ctk.CTkFrame(self.externalProjectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e", width=200,
                                           height=100)
        self.optionFrame = ctk.CTkFrame(self.optionFrameOut, bg_color="#1d1e1e", fg_color="#1d1e1e", width=80)
        self.optionFrame.pack(fill="x")

        relList = self.controller.getLocalRepoData().releases
        classList = self.controller.getClassesListR()
        
        
        if len(relList) == 0:
            relList = ["no releases"]
        else:
            relList = ru.get_git_tags(folder="repository")
            
        self.optionMenuClass = ctk.CTkOptionMenu(self.optionFrame, values=classList)
        self.optionMenuRelease = ctk.CTkOptionMenu(self.optionFrame, values=relList, command= self.updateGUI)
        

        if len(relList) > 0:
            self.optionMenuRelease.set(relList[0])
        else:
            self.optionMenuRelease.set("Nessuna release disponibile")
        self.optionMenuRelease.pack(padx=10, pady=5)

        
        if len(classList) == 0:
            classList = ["no classes"]

        if len(classList) > 0:
            self.optionMenuClass.set(classList[0])
        else:
            self.optionMenuClass.set("Nessuna classe disponibile")
        self.optionMenuClass.pack(padx=10, pady=2.5)

        self.optionButton = ctk.CTkButton(self.optionFrame, text="start analysis", command=self.on_option_button_click)
        self.optionButton.pack(pady=10)



    def on_option_button_click(self):
        if self.grid_frame is not None:
            self.grid_frame.destroy()  # Rimuovi il frame della griglia se esiste già

        self.grid_frame = ctk.CTkFrame(self.internalFrame)  # Crea un nuovo frame per la griglia
        self.grid_frame.pack(side=tk.RIGHT, padx=20, fill="y", expand=True)

        # Inizializza la GridView all'interno del frame con i dati del grafico
        chart_data = [
            [('pie', ['A', 'B'], [30, 70]), ('bar', ['X', 'Y'], [40, 60])],
            [('line', [1, 2, 3, 4, 5], [10, 20, 15, 25, 30]), ('pie', ['C', 'D'], [45, 55])]
        ]
        grid_view = GridView(self.grid_frame)
        grid_view.create_grid(chart_data)  # Passa i dati del grafico alla GridView

        self.grid_frame.update()  # Aggiorna il frame della griglia per mostrare i nuovi grafici
    
    def updateGUI(self, release):
        self.controller.getClassesList(release)
        peto = ic(self.controller.getClassesListR())
        self.optionMenuClass.configure(values = peto)
        ic(release)