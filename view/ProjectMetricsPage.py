import os.path
from tkinter import ttk
from typing import List
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
import git
from pydriller import Repository, Commit
from PIL.Image import open

class ProjectMetricsPage(ctk.CTkScrollableFrame):
    
    def __init__(self, master, debug = False):
        super().__init__(master = master)
        self.grid_frame = None  # Aggiungi una variabile per tenere traccia del frame della griglia
        ctk.set_appearance_mode("dark")
       
        self.mode = tk.StringVar()       
        self.commitList = []
        
        if debug == True:
            self.controller = ControllerFalso()
            self.repoData = self.controller.getLocalRepoData()
        else:
            self.controller = ProjectMetricsController() 
            self.repoData = self.controller.getLocalRepoData()
            self.master = master
        
        font = ctk.CTkFont(size= 40)
        self.topFrame = ctk.CTkFrame(self, bg_color="#1d1e1e", fg_color="#1d1e1e" )
        self.topFrame.pack(fill = "x", expand = True)
        self.repoName = ctk.CTkLabel(self.topFrame, text= self.controller.getLocalRepoData().name.upper(), font= font, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.repoName.pack()
         
        self.initTopFrames()
        self.externalProjectFrame.pack(pady = 12)
        
        self.initComputationModeSelector()
        
        # self.initComputationBox()
        
        # self.initOptionFrame()
        # self.optionFrameOut.pack(side = ctk.RIGHT, padx = 20, fill= "y", expand = True)


        
        left_arrow = os.path.join("resources","left-arrow.png")
        
        self.backButton = SideButton(self, self.master.previousPage, side = "left", imgpath=left_arrow)
        self.backButton.place(x= -150, y= 80)
        
        


# ----------------------------- UI METHODS -----------------------------        
    def initTopFrames(self):
        """ inizializza la parte superiore della GUI come il nome del repo e le informazioni generali """
        
        my_font = ctk.CTkFont(weight= "bold", size= 16)
        my_font_big =  ctk.CTkFont(weight= "bold", size= 20)
        
        self.externalProjectFrame = ctk.CTkFrame(self)
        self.label = ctk.CTkLabel(self.externalProjectFrame, text= "Repo general info", font = my_font_big)
        self.label.pack(anchor = "w")
        
        self.internalFrame = ctk.CTkFrame(self.externalProjectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.internalFrame.pack(side = ctk.LEFT, fill = "y", expand = True)
        
        self.projectFrame = ctk.CTkFrame(self.internalFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.projectFrame.pack(padx = 10)
        
        
        self.subFrame1 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame1.pack(anchor = "w", padx = 10, pady = 10)
        self.label = ctk.CTkLabel(self.subFrame1, text= f"Git URL: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame1, text= f"{self.repoData.git_url}")
        self.label.pack()
        
        self.subFrame2 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame2.pack(anchor = "w", padx = 10, pady = 10)
        self.label = ctk.CTkLabel(self.subFrame2, text= f"project license: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        
        license = "None"
        if self.repoData.license != None:
            license = self.repoData.license['name']
        
        self.label = ctk.CTkLabel(self.subFrame2, text= f"{license}")
        self.label.pack()
            
        self.subFrame3 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame3.pack(anchor = "w", padx = 10, pady = 10)
        self.label = ctk.CTkLabel(self.subFrame3, text= f"Repo owner: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame3, text= f"{self.repoData.owner['login']}")
        self.label.pack()
        self.subFrame4 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame4.pack(anchor = "w", padx = 10, pady = 10)
        self.label = ctk.CTkLabel(self.subFrame4, text= f"Repo owner URL: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame4, text= f"{self.repoData.owner['url']}")
        self.label.pack()

    # metodi per la gestione delle liste centrali, sono scritti nell'ordine in cui verranno chiamati----------
    def updateStartingYearList(self):
        """esegue l'update della lista degli anni di partenza dell'analisi"""
        self.disableSelectorPanel()
        startYearList = self.controller.getRepoYearList()
        newYears = [str(year) for year in startYearList]
        self.startYearSelector.configure(values = newYears)
        self.startYearSelector.set(newYears[0])
        self.startYearSelector.update()
        self.updateStartCommitList(str(startYearList[0]))
        self.enableSelectorPanel()
            
    def updateStartCommitList(self, year):
        """ esegue l'update della lista di commit di partenza dell'analisi """
        self.commitList = ic(self.controller.getCommitsByYear(year))
        commitHashes = [commit.hash for commit in self.commitList]
        self.startCommitSelector.configure(values = commitHashes, state= "normal")
        self.startCommitSelector.update()
        self.updateClassList(commitHashes[0])
    
    def updateClassList(self, hash):
        """ esegue l'update della lista delle classi """
        newList = self.controller.getClassesList(hash)
        if len(newList) == 0:
            newList = ["no classes available"]  
        self.classSelector.configure(values = newList, state = "normal")
        self.classSelector.set([newList[0]])
        self.updateArriveYearList()
    
    def updateArriveYearList(self):
        arriveYears = self.controller.getRepoYearList()
        arriveYears = [str(year) for year in arriveYears if year >= int(self.startYearSelector.get())]
        self.arriveYearSelector.configure(values = arriveYears, state = "normal") 
        self.arriveYearSelector.update()      
        
    def updateArriveCommitList(self, startCommit):
        """ esegue l'update della lista di commit di arrivo dell'analisi """
        theCommit = [commit for commit in self.commitList if commit.hash == startCommit]
        commitsAfter = [commit.hash for commit in self.commitList if commit.committer_date >= theCommit[0].committer_date]
        self.optionMenuCommitArrive.configure(values = commitsAfter, state = "normal")
        self.optionMenuCommitArrive.update()
    
    #-------------------------------
    
    
    def disableSelectorPanel(self):
        self.startYearSelector(state= "disabled")
        self.startCommitSelector(state= "disabled")
        self.classSelector(state= "disabled")
        self.arriveYearSelector(state= "disabled")
        self.arriveCommitSelector(state= "disabled")
        
    def enableSelectorPanel(self):
        self.startYearSelector(state= "normal")
        self.startCommitSelector(state= "normal")
        self.classSelector(state= "normal")
        self.arriveYearSelector(state= "normal")
        self.arriveCommitSelector(state= "normal")
        
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
    
    def initComputationModeSelector(self):
        self.lowerFrame = ctk.CTkFrame(self, bg_color= "#1d1e1e")
        self.lowerFrame.pack(fill = "x", expand = True)
        self.optionFrame = ctk.CTkFrame(self.lowerFrame)
        self.optionFrame.pack()
        
        # selettore di inizio analisi
        startYearSelectorSubFrame = ctk.CTkFrame(self.optionFrame)
        startYearSelectorSubFrame.grid(column = 0, row = 0)
        self.startYearSelector = ctk.CTkOptionMenu(startYearSelectorSubFrame, values= ["start year"], command= self.updateStartCommitList, dynamic_resizing= False)
        self.startYearSelector.pack(pady = 10)
        self.startCommitSelector = ctk.CTkOptionMenu(startYearSelectorSubFrame, values= ["start commit"], command= self.updateClassList, dynamic_resizing= False)
        self.startCommitSelector.pack()
        self.startCommitSelector.configure(state ="disabled")
        
        # selettore di classe
        self.classSelector = ctk.CTkOptionMenu(self.optionFrame, values= ["class"], dynamic_resizing= False)
        self.classSelector.grid(column = 1, row = 0, padx = 20)
        self.classSelector.configure(state ="disabled")
        
        
        # selettore di arrivo
        arriveYearSelectorSubFrame = ctk.CTkFrame(self.optionFrame)
        arriveYearSelectorSubFrame.grid(column = 2, row = 0)
        self.arriveYearSelector = ctk.CTkOptionMenu(arriveYearSelectorSubFrame, values= ["arrive year"], dynamic_resizing= False)
        self.arriveYearSelector.pack(pady = 10)
        self.arriveCommitSelector = ctk.CTkOptionMenu(arriveYearSelectorSubFrame, values= ["arrive commit"], dynamic_resizing= False)
        self.arriveCommitSelector.pack()

        # configurazione iniziale selettori
        self.updateStartingYearList()
    
    

    
    
    
                  
            
        