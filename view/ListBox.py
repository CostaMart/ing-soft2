import tkinter as tk
import customtkinter as ctk
from ttkthemes import ThemedTk

class ListBox(ctk.CTkScrollableFrame):
    """ classe che rappresenta una lista scrollabile di elementi che possono essere aggiunti dinamicamente """
    
    def __init__(self, master):
        super().__init__(master= master)
        self.row = 0
        
    def addBox(self, text: str):
        """  aggiunge un elemento alla lista """
        newbox = self._ListItem(self, text)
        newbox.pack(fill = ctk.X, expand = True, pady = 1)
    
    
    
    
    
    
    class _ListItem(ctk.CTkFrame):
        
        def __init__(self, master: any, title: str):
            super().__init__(master = master, height= 40)
            
            self.configure(fg_color="#1d1e1e")
            my_font = ctk.CTkFont(family="Arial black", size=16)
            label = ctk.CTkLabel(self, text= title, font= my_font)
            label.pack(side= ctk.LEFT, padx = 10)
            
            self.bind(sequence= "<Enter>", command= self.on_enter)
            self.bind(sequence= "<Leave>", command= self.on_leave)
            self.bind(sequence= "<Button-1>", command = self.function_test)
        
        def function_test(self, event):
            print("funziona")
        
        def on_enter(self, event):
            self.configure(fg_color="#847F7C")
            event.widget.configure(cursor="hand2")
            
            
        def on_leave(self, event):
            self.configure(fg_color="#1d1e1e")
            event.widget.configure(cursor="arrow")