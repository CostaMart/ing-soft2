import tkinter as tk
import customtkinter as ctk
import time
from controller.StartAppContoller import StartAppController
from view.MainPage import MainPage


class IngSoftApp(ctk.CTk):
    """ rappresenta l'intera applicazione, gestisce la navigazione tra le pagine e l'accesso ai dati globali dell'applicazione """

    def __init__(self, gitv, endpointStatus):
        
        self.edpointStatus = endpointStatus
        self.contoller = StartAppController()
        self.testRepoList = []
        self.pageStack = []

        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        ctk.set_appearance_mode("dark")
        self.title("Ing_soft")
        self.geometry("1200x800")
        self.minsize(800, 600)
        self.maxsize(1920, 1080)



        self.contoller.getLocalRepoData()

        # Avvia il ciclo principale dell'applicazione
        newPage = MainPage(self, gitv=gitv)
        self.pageStack.append(newPage)
        newPage.place(relwidth=1, relheight=1, rely=0, relx=0)

        self.mainloop()

    # ----------------------------- METODI PER LA GESTINE DELLA PAGINA E DEI DATI -----------------------------
    def previousPage(self):
        """"ritorna alla pagina precedente contenuta nel page stack, utilizza un'animazione di sliding"""
        page = self.pageStack[-2]
        page.place(relwidth=1, relheight=1, rely=0, relx=1)
        self._previousPageAnimation(self.pageStack[-1], page, 0)
        old = self.pageStack.pop()
        old.destroy()

    def newPage(self, newPage):
        """passa la schermata ad una nuova pagina, ossia quella passata come parametro (è necessario passare il costruttore della pagina come funzione, ossia senza parentesi tonde)"""
        page = newPage(self)
        page.place(relwidth=1, relheight=1, rely=0, relx=1)
        self._newPageAnimation(self.pageStack[-1], page, 0)
        self.pageStack[-1].place_forget()
        self.pageStack.append(page)
    
    def on_closing(self):
        self.contoller.closeSubProcess()
        self.destroy()
        # ----------------------------- METODI PER LA GESTIONE DELLA GRAFICA -----------------------------

    def _newPageAnimation(self, leftPage, rigPage, l):
        """utilty function, avvia un'animazione di sliding
        pensta unicamente per essere utilzzata da newpage"""
        while (l < 1):
            leftPage.place(relwidth=1, relheight=1, relx=-l)
            rigPage.place(relwidth=1, relheight=1, relx=1 - l)
            l = l + 0.1
            time.sleep(0.01)
            self.update()
        l = 1

        leftPage.place(relwidth=1, relheight=1, rely=0, relx=-l)
        rigPage.place(relwidth=1, relheight=1, rely=0, relx=1 - l)

    def _previousPageAnimation(self, leftPage, rigPage, l):
        """utilty function, avvia un'animazione di sliding
        pensta unicamente per essere utilzzata da previousPage"""

        while (l < 1):
            leftPage.place(relwidth=1, relheight=1, relx=l)
            rigPage.place(relwidth=1, relheight=1, relx=- 1 + l)
            l = l + 0.1
            time.sleep(0.01)
            self.update()
        l = 1

        leftPage.place(relwidth=1, relheight=1, rely=0, relx=-l)
        rigPage.place(relwidth=1, relheight=1, rely=0, relx=1 - l)
