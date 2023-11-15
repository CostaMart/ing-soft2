import os.path
from tkinter import ttk
from typing import List
import customtkinter as ctk
from view.widgets.SideButton import SideButton
from view.widgets.Plot import PlotCartesian
from controller.ProjectMetricsContoller import ProjectMetricsController
import tkinter as tk
from matplotlib import dates as mdates
from icecream import ic
from .ControllerFalso import ControllerFalso
from .widgets.Graphics.GridView import GridView
from icecream import ic
import model.repo_utils as ru
import git
from pydriller import Repository, Commit
from PIL.Image import open
import model.chartOrganizer as co
import pandas as pd
from matplotlib.dates import date2num
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from datetime import datetime

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
        
        
        self.yearList = self.controller.getYearList()
        self.computationPanel()
        
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


    # -----------------------------gli update si chiamano a catena tra di loro quando viene aggioranto un componetne -----------------------------
          
   # -----------------------------update start commit list-----------------------------   
    def start_updateStartCommitList(self, year):
        """ esegue l'update della lista di commit di partenza dell'analisi """
        me = self
        
        def _end_updateStartCommitList(commitList):    
            commitHashes = [commit.hash for commit in commitList]
            me.startCommitSelector.configure(values = commitHashes)
            me.startCommitSelector.update()
            me.startCommitSelector.set(commitHashes[0])
            me.updateClassList(commitHashes[0])

    
        self.disableSelectorPanel()
        self.controller.updateCommitsListByYear(year, callback = _end_updateStartCommitList)
        
    
    # -----------------------------update lista classi-----------------------------
    def updateClassList(self, hash):
        """ esegue l'update della lista delle classi """
        
        self.disableSelectorPanel()
        newList = self.controller.getClassesList(hash)
        if len(newList) == 0:
            newList = ["no classes available"]  
        self.classSelector.configure(values = newList)
        self.classSelector.set(list(newList)[0])
        self.start_updateArriveYearList(self.startYearSelector.get())
    
    # -----------------------------update anno di arrivo-----------------------------
    def start_updateArriveYearList(self, startingYear):
        
        self.disableSelectorPanel()
        years = self.yearList
        
        
        def _end_updateArriveYearList(arriveYears = 0):
            startingYear = int(self.startYearSelector.get())
            newYearList = [str(year) for year in years if year >= startingYear]
            self.arriveYearSelector.configure(values = newYearList) 
            self.arriveYearSelector.update()
            self.arriveYearSelector.set(newYearList[0])
            self.start_updateArriveCommitList(self.classSelector.get()) 
        
        self.controller.updateRepoYearList(callback= _end_updateArriveYearList)
        
    # -----------------------------update commit di arrivo -----------------------------    
    def start_updateArriveCommitList(self, className):
        """ esegue l'update della lista di commit di arrivo dell'analisi """
        self.disableSelectorPanel()
        className = self.classSelector.get()      
        startCommit = self.controller.getCommitByhash(self.startCommitSelector.get())
        
        def _end_updateArriveCommitList(commitList: List[Commit]):
           
            
            finalList = [commit.hash for commit in commitList if className in self.controller.getClassesList(commit.hash)]
            
            if len(finalList) == 0:
                finalList =["select a class"]
            
            self.arriveCommitSelector.configure(values = finalList)
            self.arriveCommitSelector.update()
            self.arriveCommitSelector.set(finalList[0])
            self.enableSelectorPanel()
        
        self.controller.getCommiListFromDate(startCommit.committer_date, self.arriveYearSelector.get(), callback= ic(_end_updateArriveCommitList))
         
   
    # ----------------------------- GUI MANAGEMENT METHODS -----------------------------
    def disableSelectorPanel(self):
        """disabilita il pannello di selezione dei commit"""
        self.startYearSelector.configure(state= "disabled")
        self.startCommitSelector.configure(state= "disabled")
        self.classSelector.configure(state= "disabled")
        self.arriveYearSelector.configure(state= "disabled")
        self.arriveCommitSelector.configure(state= "disabled")
        
    def enableSelectorPanel(self):
        """abilita il pannello di selezione dei commit"""
        self.startYearSelector.configure(state= "normal")
        self.startCommitSelector.configure(state= "normal")
        self.classSelector.configure(state= "normal")
        self.arriveYearSelector.configure(state= "normal")
        self.arriveCommitSelector.configure(state= "normal")
        
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
    
    def computationPanel(self):
        self.lowerFrame = ctk.CTkFrame(self, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.lowerFrame.pack(fill = "x", expand = True)
        
        self.lowerFrameLabel = ctk.CTkLabel(self.lowerFrame, text = """select where to start and where to finish your analysis \n keep in mind: long therm analysis will require more time""")
        self.lowerFrameLabel.pack()
        
        self.optionFrame = ctk.CTkFrame(self.lowerFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.optionFrame.pack()
        
        # selettore di inizio analisi
        startYearSelectorSubFrame = ctk.CTkFrame(self.optionFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        startYearSelectorSubFrame.grid(column = 0, row = 0)
        self.startYearSelector = ctk.CTkOptionMenu(startYearSelectorSubFrame, values= [str(year) for year in self.yearList] , command= self.start_updateStartCommitList, dynamic_resizing= False)
        self.startYearSelector.pack(pady = 10)
        self.startCommitSelector = ctk.CTkOptionMenu(startYearSelectorSubFrame, values= ["start commit"], command= self.updateClassList, dynamic_resizing= False)
        self.startCommitSelector.pack()
        self.startCommitSelector.configure(state ="disabled")
        
        # selettore di classe
        self.classSelector = ctk.CTkOptionMenu(self.optionFrame, values= ["class"], command= self.start_updateArriveCommitList, dynamic_resizing= False)
        self.classSelector.grid(column = 1, row = 0, padx = 20)
        self.classSelector.configure(state ="disabled")
        
        # selettore di arrivo
        arriveYearSelectorSubFrame = ctk.CTkFrame(self.optionFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        arriveYearSelectorSubFrame.grid(column = 2, row = 0, pady = 10)
        self.arriveYearSelector = ctk.CTkOptionMenu(arriveYearSelectorSubFrame, values= ["arrive year"], dynamic_resizing= False, command = self.start_updateArriveCommitList)
        self.arriveYearSelector.pack()
        self.arriveCommitSelector = ctk.CTkOptionMenu(arriveYearSelectorSubFrame, values= ["arrive commit"], dynamic_resizing= False)
        self.arriveCommitSelector.pack()

        # bottone di start dell'analisi affidata ad un altro processo
        start_button = ctk.CTkButton(self, text="Start Analysis", command=self.start_endpoint)
        start_button.pack()

        # configurazione iniziale selettori
        self.start_updateStartCommitList(self.yearList[0])
    

    def start_endpoint(self):
        """Viene chiamata la classe ComputationEndpoint per iniziare l'analisi delle metriche"""
        """gli vengono passate le funzioni per calcolare le metriche e i parametri necessari per eseguire l'analisi"""
        """utilizzo i metodi del controller per passargli le funzioni che deve eseguire come messaggi"""
        
        # prende il nome della classe dal selettore
        class_name = self.classSelector.get()

        # lista di commit dall'inizio alla fine dell'analisi
        start_commit_hash = self.startCommitSelector.get()
        arrive_commit_hash = self.arriveCommitSelector.get()

        commit_list = self.controller.getCommitsBetweenHashes(start_commit_hash, arrive_commit_hash)
        # prima di inviare il messaggio si fa una verifica che la lista non è vuota
        if commit_list:
            self.controller.sendMessage(
                {
                    "fun": "generate_metrics",
                    "nome_classe": class_name,
                    "commits_dict": commit_list
                }
            )
        else:
            print("La lista di commit è vuota o non valida. Impossibile avviare l'analisi.")
        
        process_dict = self.controller.receiveMessage()
        print(process_dict)
        self.paned_window = tk.PanedWindow(self, orient=tk.VERTICAL, sashwidth=10)
        self.paned_window.pack(expand=True, fill="both")

        # Grafico Loc
        fig_loc = Figure(figsize=(10, 10), dpi=100)
        ax_loc = fig_loc.add_subplot(111)
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        ax_loc.plot(y2, x1, label='Linee di Codice', marker='o')
        ax_loc.plot(y2, x2, label='Linee vuote', marker='o')
        ax_loc.plot(y2, x3, label='Commenti', marker='o')
        ax_loc.legend()
        ax_loc.set_title("Amount (in LOC) of previous changes")
        ax_loc.set_xticklabels(y2, rotation=30, ha='right')
        

        canvas_loc = FigureCanvasTkAgg(fig_loc, master=self)
        canvas_loc.draw()
        canvas_loc.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Grafico revisioni
        fig_revision = Figure(figsize=(10, 10), dpi=100)
        ax_revision = fig_revision.add_subplot(111)
        x, y = co.revision_number(process_dict)
        ax_revision.bar(y2, x)
        ax_revision.legend()
        ax_revision.set_title("Number of revisions")
        ax_revision.set_xticklabels(y2, rotation=30, ha='right')

        canvas_revision = FigureCanvasTkAgg(fig_revision, master=self)
        canvas_revision.draw()
        canvas_revision.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        # Grafico bugfix
        fig_bugfix = Figure(figsize=(10, 10), dpi=100)
        ax_bugfix = fig_bugfix.add_subplot(111)
        x, y = co.bugfix(process_dict)
        ax_bugfix.bar(y2, x)
        ax_bugfix.legend()
        ax_bugfix.set_title("Number of bugfix commits")
        ax_bugfix.set_xticklabels(y2, rotation=30, ha='right')

        canvas_bugfix = FigureCanvasTkAgg(fig_bugfix, master=self)
        canvas_bugfix.draw()
        canvas_bugfix.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Grafico code churn
        fig_codechurn = Figure(figsize=(10, 10), dpi=100)
        ax_codechurn = fig_codechurn.add_subplot(111)
        x, y = co.codeC(process_dict)
        ax_codechurn.bar(y2, x)
        ax_codechurn.legend()
        ax_codechurn.set_title("Number of code churn commits")
        ax_codechurn.set_xticklabels(y2, rotation=30, ha='right')

        canvas_codechurn = FigureCanvasTkAgg(fig_codechurn, master=self)
        canvas_codechurn.draw()
        canvas_codechurn.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Grafico weeks
        fig_weeks = Figure(figsize=(10, 10), dpi=100)
        ax_weeks = fig_weeks.add_subplot(111)
        x, y = co.weeks(process_dict)
        ax_weeks.bar(y2, x)
        ax_weeks.legend()
        ax_weeks.set_title("Number of weeks")
        ax_weeks.set_xticklabels(y2, rotation=30, ha='right')

        canvas_weeks = FigureCanvasTkAgg(fig_weeks, master=self)
        canvas_weeks.draw()
        canvas_weeks.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Grafico authors
        fig_authors = Figure(figsize=(10, 10), dpi=100)
        ax_authors = fig_authors.add_subplot(111)
        x, y = co.authors(process_dict)
        ax_authors.bar(y2, x)
        ax_authors.legend()
        ax_authors.set_title("Number of authors")
        ax_authors.set_xticklabels(y2, rotation=30, ha='right')

        canvas_authors = FigureCanvasTkAgg(fig_authors, master=self)
        canvas_authors.draw()
        canvas_authors.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



        # Aggiungi i canvas al PanedWindow
        self.paned_window.add(canvas_loc.get_tk_widget(), stretch="never", minsize=100)
        self.paned_window.add(canvas_revision.get_tk_widget(), stretch="never", minsize=100)
        self.paned_window.add(canvas_bugfix.get_tk_widget(), stretch="never", minsize=100)
        self.paned_window.add(canvas_codechurn.get_tk_widget(), stretch="never", minsize=100)
        self.paned_window.add(canvas_weeks.get_tk_widget(), stretch="never", minsize=100)
        self.paned_window.add(canvas_authors.get_tk_widget(), stretch="never", minsize=100)
        
