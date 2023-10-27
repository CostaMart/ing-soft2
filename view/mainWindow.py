import tkinter as tk
import customtkinter as ctk
from ttkthemes import ThemedTk
from widgets.ListBox import ListBox


class IngSoftApp(ctk.CTk):
    """ main page dell'app """
    
    def __init__(self):
        
        self.testRepoList = ["rep1", "rep2"]
        
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Ing_soft")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.maxsize(1600,1000)
        
        self._initSearchBlock()
        
        self.listBox = ListBox(self)
        self.listBox.pack( padx = 10, fill = ctk.X, expand = True)
        
        # qui dovrebbe recuperare i repo
        """ for repo in repoList:
            self.listBox.addBox(repo.name)
         """
        
        for repo in self.testRepoList:
             self.listBox.addBox(repo)
         
        # Avvia il ciclo principale dell'applicazione
        self.mainloop()
    
    def _initSearchBlock(self):
        """ inizializza la sezione con il form di ricerca """
        
        my_font = ctk.CTkFont(family="Arial black", size=25)
       
        label = ctk.CTkLabel(self, text= "Search for a repo ", width= 10, font = my_font)
        label.pack(side = ctk.TOP, pady = 30)
        

        self.entry = ctk.CTkEntry(self, width= 400)
        self.entry.pack()
        
        searchBut = ctk.CTkButton(self, text= "Search")
        searchBut.pack(pady = 10)
    
        
        
if __name__ == "__main__":
    IngSoftApp()