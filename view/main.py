import tkinter as tk
import customtkinter as ctk
from ttkthemes import ThemedTk
from .ListBox import ListBox
from model.Domain import Repository
import time
import threading
from controller.mainPageContoller import get_repo_list, get_selected_repo

class IngSoftApp(ctk.CTk):
    
     
    
    """ main page dell'app """
    def __init__(self):
        
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
        
        self.updateRepoList()
        
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
        self.message = tk.Label(self, textvariable= self.text, background="#1d1e1e", foreground= "#FFFFFF" )
        self.message.config(font= font)
        self.message.pack()
        
    def updateRepoList(self, newList = None):
        self.listBox.cleanList()
        
        if (newList != None):
            self.testRepoList = newList
        
        for repo in self.testRepoList:
            command = self._generateCommand(repo.url)
            self.listBox.addBox(repo.name, command = command)

    def _generateCommand(self, value):
        """ restituisce una closure che verrà assegnata al tasto corrsipondente """
        def asyncFun(event):
            thread = threading.Thread(target= self.downloadRepo, args = [value, 0])
            thread.start()
        return asyncFun
    
    def downloadRepo(self, value, intero):
        self.showMessage(f"now downloading: {value}")
        get_selected_repo(value)
        self.showMessage("download complete")
        time.sleep(2)
        self.showMessage("")
        
    def showMessage(self, msg):
        self.text.set(msg)
    
    def _start_request(self):
        self.testRepoList = get_repo_list(self.entry.get(), self.updateRepoList)
       
   
