import os.path
from typing import List
import customtkinter as ctk
from view.widgets.SideButton import SideButton
from controller.ProjectMetricsContoller import ProjectMetricsController
import tkinter as tk
from icecream import ic
from pydriller import Commit
import tkinter as tk
from .widgets.GraficiSP.GraphFactory import GraphFactory
from .widgets.LoadingIcon import RotatingIcon

class ProjectMetricsPage(ctk.CTkScrollableFrame):
    """ view rappresentante la pagina delle metriche """
    def __init__(self, master, debug = False):
        super().__init__(master = master)
        self.grid_frame = None  # Aggiungi una variabile per tenere traccia del frame della griglia
        ctk.set_appearance_mode("dark")
       
        self.mode = tk.StringVar()       
        self.commitList = []
        self.panelCreated = False
        
        self.controller = ProjectMetricsController() 
        self.repoData = self.controller.getLocalRepoData()
        self.master = master
        
        font = ctk.CTkFont(size= 40)
        self.topFrame = ctk.CTkFrame(self, bg_color="#1d1e1e", fg_color="#1d1e1e" )
        self.topFrame.pack(fill = "x", expand = True)
        self.repoName = ctk.CTkLabel(self.topFrame, text= self.controller.getLocalRepoData().name.upper(), font= font, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.repoName.pack()
         
        
        # inizializza primo pannello
        self.initTopFrames()
        self.externalProjectFrame.pack(pady = 12)
        
        #inizializza il pannello laterale
        self.initTopRightFrame()
        
        # inizializza lista di anni del repo in memoria
        self.yearBranchDict = ic(self.controller.getYearList())
        self.yearList = list(self.yearBranchDict.keys())
        
        # inizializza il pannello di selezione dei commit
        self.computationPanel()
        
 
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
        
    def initTopRightFrame(self):
        self.topRightFrame = ctk.CTkFrame(self, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.topRightFrame.pack()
        self.modeSelector = ctk.CTkSegmentedButton(self.topRightFrame, values= ["project metrics", "CK metrics"])
        self.modeSelector.pack()
        self.modeSelector.set("project metrics")

    def startRequest(self):
        """ in base al valore impostato sul selettore decide quale analisi far iniziare """
        if self.modeSelector.get() == "CK metrics":
            self.start_CKdataRequest()
        else:
            self.start_dataRequest()
  
    def loadingFrame(self):
        """ mostra un messaggio durante il caricamento """
        self.messageFrame = ctk.CTkFrame(master= self.lowerFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.messageFrame.pack()
        message = ctk.CTkLabel(master= self.messageFrame, text= "we are computing your request", bg_color="#1d1e1e", fg_color="#1d1e1e")
        message.pack()
        rotating = RotatingIcon(master= self.messageFrame, iconPath= os.path.join("resources","rotationLoading.png"), backgroundColor="#1d1e1e")
        rotating.pack()
        rotating.beginRotation()
  
    def start_dataRequest(self):
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
            self.controller.request_service(
                message = {
                    "fun": "generate_metrics",
                    "nome_classe": class_name,
                    "commits_dict": commit_list
                },
            callback = self.finalize_data_request
            )
            
            self.loadingFrame()
            self.disableSelectorPanel()
        else:
            print("La lista di commit è vuota o non valida. Impossibile avviare l'analisi.")
    
    def finalize_data_request(self, process_dict):
        """ utilizzata come call back da start data request per aggiornare la view """
        
        if self.panelCreated:
            self.graphFrame.destroy()
            self.panelCreated = False
        
        
        
        self.graphFrame = ctk.CTkFrame(self, bg_color= "#1d1e1e", fg_color= "#1d1e1e")
        self.graphFrame.pack(pady = 30)
        self.panelCreated= True
        
        

        graphFactory = GraphFactory()

       
        # Grafico Loc
        locFrame = ctk.CTkFrame(self.graphFrame)
        locFrame.grid(column= 0, row = 0, padx=10, pady = 20)
        loc, toolbar = graphFactory.makeGraph(master= locFrame, graph= "loc", process_dict = process_dict)
        toolbar.pack()
        loc.pack()
        # bottoneAmoroso2= ctk.CTkButton(locFrame, command= loc.zoom_in, text= "bottoncino simpatichino +")
        # bottoneAmoroso2.pack()

        

        # Grafico revisioni
        revisionFrame = ctk.CTkFrame(self.graphFrame)
        revisionFrame.grid(column= 1, row = 0, padx=10, pady = 20)
        revision, revToolbar = graphFactory.makeGraph(master= revisionFrame, graph= "revisions", process_dict= process_dict)
        revision.pack()

        
        # Grafico bugfix
        bugFrame = ctk.CTkFrame(self.graphFrame)
        bugFrame.grid(column= 0, row = 1, padx=10, pady = 20)
        churn, bugToolbar = graphFactory.makeGraph(master= bugFrame, graph= "bugfix", process_dict= process_dict)
        churn.pack()

       
        
        # Grafico code churn
        churnFrame = ctk.CTkFrame(self.graphFrame)
        churnFrame.grid(column= 1, row = 1, padx=10, pady = 20)
        churn, churnToolbar = graphFactory.makeGraph(master= churnFrame, graph= "churn", process_dict= process_dict)
        churn.pack()
   
        
        # Grafico weeks
        weeksFrame = ctk.CTkFrame(self.graphFrame)
        weeksFrame.grid(column= 0, row = 2, padx=10, pady = 20)
        weeks, churnToolbar = graphFactory.makeGraph(master= weeksFrame, graph= "weeks", process_dict= process_dict)
        weeks.pack()
   
      
        
        # Grafico authors
        authorsFrame = ctk.CTkFrame(self.graphFrame)
        authorsFrame.grid(column= 1, row = 2, padx=10, pady = 20)
        author, churnToolbar = graphFactory.makeGraph(master= authorsFrame, graph= "authors", process_dict= process_dict)
        author.pack()
        
        # grafico contributi     
        contributionsFrame = ctk.CTkFrame(self.graphFrame)
        contributionsFrame.grid(column= 0, row = 3, padx=10, pady = 20)
        contributions, churnToolbar = graphFactory.makeGraph(master= contributionsFrame, graph= "contributions", process_dict= process_dict)
        contributions.pack()
        
        self.enableSelectorPanel()
        self.messageFrame.forget()
                  
    def start_CKdataRequest(self):
        """Viene chiamata la classe ComputationEndpoint per iniziare l'analisi delle metriche"""
        """gli vengono passate le funzioni per calcolare le metriche e i parametri necessari per eseguire l'analisi"""
        """utilizzo i metodi del controller per passargli le funzioni che deve eseguire come messaggi"""

        # lista di commit dall'inizio alla fine dell'analisi
        start_commit_hash = self.startCommitSelector.get()
        arrive_commit_hash = self.arriveCommitSelector.get()

        commit_list = self.controller.getCommitsBetweenHashes(start_commit_hash, arrive_commit_hash)
        # prima di inviare il messaggio si fa una verifica che la lista non è vuota
        if commit_list:
            self.controller.request_service(
                {
                    "fun": "generate_metricsCK",
                    "commits_dict": commit_list
                },
                callback= self.finalize_CDdata_request
            )
            
            self.loadingFrame()
            self.disableSelectorPanel()
        else:
            print("La lista di commit è vuota o non valida. Impossibile avviare l'analisi.")
               
    def finalize_CDdata_request(self, process_dict):
        
        if self.panelCreated:
            self.graphFrame.destroy()
            self.panelCreated = False
        
        
        graphFactory = GraphFactory()
        
        self.graphFrame = ctk.CTkFrame(self, bg_color= "#1d1e1e", fg_color= "#1d1e1e")
        self.graphFrame.pack(pady = 30)
        self.panelCreated= True 
       
        # Grafico Cbo
        cboFrame = ctk.CTkFrame(self.graphFrame)
        cboFrame.grid(column= 0, row = 0, padx=10, pady = 20)
        cbo, churnToolbar = graphFactory.makeGraph(master= cboFrame, graph= "cbo", process_dict= process_dict)
        cbo.pack()
   
        
        # Grafico rfc
        rfcFrame = ctk.CTkFrame(self.graphFrame)
        rfcFrame.grid(column= 1, row = 0, padx=10, pady = 20)
        rfc, churnToolbar = graphFactory.makeGraph(master= rfcFrame, graph= "rfc", process_dict= process_dict)
        rfc.pack()
        
     
       
        # Grafico wmc
        wmcFrame = ctk.CTkFrame(self.graphFrame)
        wmcFrame.grid(column= 0, row = 1, padx=10, pady = 20)
        wmc, churnToolbar = graphFactory.makeGraph(master= wmcFrame, graph= "wmc", process_dict= process_dict)
        wmc.pack()
      
         # Grafico noc
        nocFrame = ctk.CTkFrame(self.graphFrame)
        nocFrame.grid(column= 1, row = 1, padx=10, pady = 20)
        noc, churnToolbar = graphFactory.makeGraph(master= nocFrame, graph= "noc", process_dict= process_dict)
        noc.pack()
       
         # Grafico dit
        ditFrame = ctk.CTkFrame(self.graphFrame)
        ditFrame.grid(column= 0, row = 2, padx=10, pady = 20)
        dit, churnToolbar = graphFactory.makeGraph(master= ditFrame, graph= "dit", process_dict= process_dict)
        dit.pack()
  
        # Grafico lcom
        lcomFrame = ctk.CTkFrame(self.graphFrame)
        lcomFrame.grid(column= 1, row = 2, padx=10, pady = 20)
        lcom, churnToolbar = graphFactory.makeGraph(master= lcomFrame, graph= "lcom", process_dict= process_dict)
        lcom.pack()
        
        self.enableSelectorPanel()
        self.messageFrame.forget()
    
    # ----------------------------- le seguenti funzioni controllano gli update del blocco di selezione per l'analisi dei commit  -----------------------------
    def computationPanel(self):
        """ inizializza il pannello centrale con le sue componenti """
        
        self.lowerFrame = ctk.CTkFrame(self, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.lowerFrame.pack(fill = "x", expand = True)
        
        self.lowerFrameLabel = ctk.CTkLabel(self.lowerFrame, text = """select where to start and where to finish your analysis \n keep in mind: long therm analysis will require more time""")
        self.lowerFrameLabel.pack(pady= 20)
        
        self.optionFrame = ctk.CTkFrame(self.lowerFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.optionFrame.pack()
        
        # selettore di inizio analisi
        startYearSelectorSubFrame = ctk.CTkFrame(self.optionFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        startYearSelectorSubFrame.grid(column = 0, row = 0)
        startLabel = ctk.CTkLabel(startYearSelectorSubFrame, text = "start point: ", bg_color="#1d1e1e", fg_color="#1d1e1e")
        startLabel.pack()
        self.startYearSelector = ctk.CTkOptionMenu(startYearSelectorSubFrame, values= [str(year) for year in self.yearList] , command= self.update_branchList, dynamic_resizing= False)
        self.startYearSelector.pack(pady = 10)
        
        # selettore di branch
        self.branchSelector = ctk.CTkOptionMenu(startYearSelectorSubFrame, values = [ic(branch) for branch in self.yearBranchDict[int(self.startYearSelector.get())] if "HEAD" not in branch], command= self.start_updateStartCommitList, dynamic_resizing= False)
        self.branchSelector.pack()
        
        # selettore di commit iniziale
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
        arriveLabel = ctk.CTkLabel(arriveYearSelectorSubFrame, text = "arrive point: ", bg_color="#1d1e1e", fg_color="#1d1e1e")
        arriveLabel.pack()
        self.arriveYearSelector = ctk.CTkOptionMenu(arriveYearSelectorSubFrame, values= ["arrive year"], dynamic_resizing= False, command = self.start_updateArriveCommitList)
        self.arriveYearSelector.pack(pady = 10)
        self.arriveCommitSelector = ctk.CTkOptionMenu(arriveYearSelectorSubFrame, values= ["arrive commit"], dynamic_resizing= False)
        self.arriveCommitSelector.pack()

        # bottone di start dell'analisi affidata ad un altro processo
        self.start_button = ctk.CTkButton(self.lowerFrame, text="Start Analysis", command=self.startRequest)
        self.start_button.pack(anchor = "s", pady= 10)

        # configurazione iniziale selettori
        ic(self.yearList)
        self.start_updateStartCommitList(self.yearList[0]) 
        
        
        
        
        
        
        
        
    def disableSelectorPanel(self):
        """disabilita il pannello di selezione dei commit"""
        self.startYearSelector.configure(state= "disabled")
        self.startCommitSelector.configure(state= "disabled")
        self.classSelector.configure(state= "disabled")
        self.arriveYearSelector.configure(state= "disabled")
        self.arriveCommitSelector.configure(state= "disabled")
        self.start_button.configure(state = "disabled")
            
    def enableSelectorPanel(self):
        """abilita il pannello di selezione dei commit"""
        self.startYearSelector.configure(state= "normal")
        self.startCommitSelector.configure(state= "normal")
        self.classSelector.configure(state= "normal")
        self.arriveYearSelector.configure(state= "normal")
        self.arriveCommitSelector.configure(state= "normal")
        self.start_button.configure(state = "normal")      
        
          
   # -----------------------------update start commit list-----------------------------   
    
    
    def update_branchList(self, year):
        values = [ic(branch) for branch in self.yearBranchDict[int(year)] if "HEAD" not in branch]
        self.branchSelector.configure(values = values)
        self.branchSelector.set(values[0])
        self.start_updateStartCommitList(year = year)
    
    def start_updateStartCommitList(self, branch = "any", year = "no Value"):
        """ esegue l'update della lista di commit di partenza dell'analisi """
        me = self
        
        if year == "no Value":
            year = self.startYearSelector.get()        
        
        
        def _end_updateStartCommitList(commitList):    
            commitHashes = [commit.hash for commit in commitList]
            me.startCommitSelector.configure(values = commitHashes)
            me.startCommitSelector.update()
            me.startCommitSelector.set(commitHashes[0])
            me.updateClassList(commitHashes[0])

    
        self.disableSelectorPanel()
        self.controller.updateCommitsListByYear(year, self.branchSelector.get(), callback = _end_updateStartCommitList)
        
    
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
         
   
    
 

