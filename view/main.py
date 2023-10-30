import tkinter as tk
from tkinter import font
import customtkinter as ctk
from ttkthemes import ThemedTk
from .ListBox import ListBox
from model.Domain import Repository
import time
import threading
from controller.mainPageContoller import get_selected_repo, request_for_repos
from view.LoadingIcon import RotatingIcon

class IngSoftApp(ctk.CTk):
    
     
    
    """ main page dell'app """
    def __init__(self, gitv):
        
        self.testRepoList = []
        
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        self.title("Ing_soft")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.maxsize(1600,1000)
        
        self._initSearchBlock()
        
        self.listBox = ListBox(self)
        self.listBox.pack( padx = 10, fill = ctk.X, expand = True)
        
        self.gitStatusFrame = tk.Frame(self, height= 15)
        self.gitStatusFrame.config(bg= "#2b2b2b")
        self.gitStatusFrame.pack(fill= "x")
        f = font.Font(size=7)
        self.gitStatusLabel = tk.Label(self.gitStatusFrame , text = gitv, background="#2b2b2b", foreground= "white", font= f )
        self.gitStatusLabel.place(x= 5, y= 0) 
        
        self.testRepoList = []
        
        # Avvia il ciclo principale dell'applicazione
        self.mainloop()
    
    def _initSearchBlock(self):
        """ inizializza la sezione con il form di ricerca """
        
        my_font = ctk.CTkFont(family="Arial black", size=25)
       
        label = ctk.CTkLabel(self, text= "Search for a repo ", width= 10, font = my_font)
        label.pack(side = ctk.TOP, pady = 30)
        

        self.entry = ctk.CTkEntry(self, width= 400)
        self.entry.pack()
        
        searchBut = ctk.CTkButton(self, text= "Search", command= self._start_request)
        searchBut.pack(pady = 10)
        
        self.text = tk.StringVar()
        font = ("Arial black", 12)  # Sostituisci con il font e la grandezza desiderati
        
        self.messageBox = tk.Frame(self)
        self.messageBox.configure(bg = "#1d1e1e")
        self.messageBox.pack(fill= "x")
        self.message = tk.Label(self.messageBox, textvariable= self.text, background="#1d1e1e", foreground= "#FFFFFF")
        self.message.config(font= font)
        self.message.pack()
        
    def _updateRepoList(self, query, val):
        """ medoto che esegue l'update della lista  """
        respolist = request_for_repos(query= query)
        
        self.listBox.cleanList()
        
        if (respolist != None):
            self.testRepoList = respolist
        
        for repo in self.testRepoList:
            command = self._generateCommand(repo.url)
            self.listBox.addBox(repo.name, command = command)

    def _generateCommand(self, value):
        """ restituisce una closure che verrà assegnata al tasto corrsipondente, realizzando una closure ogni tasto, quando premuto, richiederà il download del repo relativo """
        
        def asyncFun(event):
            thread = threading.Thread(target= self._downloadRepo, args = [value, 0])
            thread.start()
        return asyncFun
    
    def _downloadRepo(self, value, intero):
        
        """ avvia il download del repo selezionato mostrando un messaggio sullo stato del download, viene utilzzata da generateCommand per generare una closure """
        icon = RotatingIcon(self.messageBox, iconPath= "resources\\rotationLoading.png", backgroundColor= "#1d1e1e")
        icon.pack()
        self.showMessage(f"now downloading: {value}")
        get_selected_repo(value)
        self.showMessage("download complete")
        icon.destroy()
        time.sleep(2)
        self.showMessage("")
    
    def showMessage(self, msg):
        """ modifica il messaggio visualizzato """
        self.text.set(msg)
    
    def _start_request(self):
        "avvia la richiesta di update della lista su un thread separato"
        t = threading.Thread(target= self._updateRepoList, args= (self.entry.get(), 0) )
        t.start()
   
