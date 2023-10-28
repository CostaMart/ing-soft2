import tkinter as tk
import customtkinter as ctk
from ttkthemes import ThemedTk

class ListBox(ctk.CTkScrollableFrame):
    """ classe che rappresenta una lista scrollabile di elementi che possono essere aggiunti dinamicamente """
    
    def __init__(self, master):
        super().__init__(master= master)
        self.childList = []
        
    def addBox(self, text: str, command = None):
        """  aggiunge un elemento alla lista """
        newbox = self._ListItem(self, text, command = command)
        self.childList.append(newbox)
        newbox.pack(fill = ctk.X, expand = True, pady = 1)
    
    def cleanList(self):
        """ rimuove tutti gli elementi dalla lista """

        for child in self.childList:
            child.destroy()
    
    
    
    
    class _ListItem(ctk.CTkFrame):
        
        def __init__(self, master: any, title: str, command = None):
            super().__init__(master = master, height= 40)
            
            self.configure(fg_color="#1d1e1e")
            my_font = ctk.CTkFont(family="Arial black", size=16)
            label = ctk.CTkLabel(self, text= title, font= my_font)
            label.pack(side= ctk.LEFT, padx = 10)
            
            self.bind(sequence= "<Enter>", command= self.on_enter)
            self.bind(sequence= "<Leave>", command= self.on_leave)
            self.bind(sequence= "<Button-1>", command = command)
        
        
        def on_enter(self, event):
            self.configure(fg_color="#847F7C")
            event.widget.configure(cursor="hand2")
            
            
        def on_leave(self, event):
            self.configure(fg_color="#1d1e1e")
            event.widget.configure(cursor="arrow")