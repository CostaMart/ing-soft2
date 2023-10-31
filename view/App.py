import tkinter as tk
import customtkinter as ctk
import time
from controller.mainPageContoller import get_selected_repo, request_for_repos
from view.main import MainPage

class IngSoftApp(ctk.CTk):
    
    """ rappresenta l'intera applicazione, gestisce la navigazione tra le pagine"""
    
    def __init__(self, gitv):
        
        self.testRepoList = []
        self.pageStack = []
        
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        self.title("Ing_soft")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.maxsize(1600,1000)
        
       
        
        # Avvia il ciclo principale dell'applicazione
        newPage = MainPage(self, gitv= gitv)
        self.pageStack.append(newPage)
        newPage.place(relwidth = 1, relheight = 1, rely = 0, relx = 0)
        
        self.mainloop()
           
    def previousPage(self):
        """"add a new page to the stack"""
        page = self.pageStack[-2]
        page.place(relwidth = 1, relheight = 1, rely = 0, relx = 1)
        self._previousPageAnimation(self.pageStack[-1], page, 0)
        old = self.pageStack.pop()
        old.destroy()  
        
    def newPage(self, newPage):
        """"add a new page to the stack"""
        page = newPage(self)
        page.place(relwidth = 1, relheight = 1, rely = 0, relx = 1)
        self._newPageAnimation(self.pageStack[-1], page, 0)
        self.pageStack[-1].place_forget()
        
        self.pageStack.append(page)  
               
    def _newPageAnimation(self, leftPage, rigPage, l):
        
        while(l < 1):
            
            leftPage.place(relwidth = 1, relheight = 1, relx = -l)
            rigPage.place(relwidth = 1, relheight = 1, relx = 1 - l)
            l = l + 0.1
            time.sleep(0.01)
            self.update()
        l= 1
        
        leftPage.place(relwidth = 1, relheight = 1, rely = 0, relx = -l)
        rigPage.place(relwidth = 1, relheight = 1, rely = 0, relx = 1 - l)
       
    def _previousPageAnimation(self, leftPage, rigPage, l):
        
        while(l < 1):
            
            leftPage.place(relwidth = 1, relheight = 1, relx = l)
            rigPage.place(relwidth = 1, relheight = 1, relx = - 1 + l)
            l = l + 0.1
            time.sleep(0.01)
            self.update()
        l= 1
        
        leftPage.place(relwidth = 1, relheight = 1, rely = 0, relx = -l)
        rigPage.place(relwidth = 1, relheight = 1, rely = 0, relx = 1 - l)   
            