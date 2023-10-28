import tkinter as tk
import customtkinter as ctk
from ttkthemes import ThemedTk
from .ListBox import ListBox
from model.Domain import Repository
from controller.mainPageContoller import get_repo_list

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
        
        searchBut = ctk.CTkButton(self, text= "Search", command= self.start_request)
        searchBut.pack(pady = 10)
    
    def updateRepoList(self, newList = None):
        self.listBox.cleanList()
        
        if (newList != None):
            self.testRepoList = newList
            
        for repo in self.testRepoList:
            self.listBox.addBox(repo.name)

    def start_request(self):
        print(self.entry.get())
        self.testRepoList = get_repo_list(self.entry.get(), self.updateRepoList)
       
        
