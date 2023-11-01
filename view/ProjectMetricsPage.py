import tkinter as tk
from tkinter import font
import customtkinter as ctk
from view.widgets.SideButton import SideButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk







class ProjectMetricsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master)
        ctk.set_appearance_mode("dark")
       
        self.master = master
               
       
        
        
        self.frame = ctk.CTkFrame(self, width= 400, height= 400)
        self.frame.pack( fill = "x", expand= True)
        
        label = ctk.CTkLabel(self.frame, text = self.master.repoData.name)
        label.pack()
        # Creare un oggetto Figure di Matplotlib
        fig = Figure(figsize=(5, 4), dpi=100, facecolor= "#2b2b2b")
        
        # Aggiungere un subplot al figure
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5], [10, 5, 12, 6, 15])  # Esempio di dati per il grafico
        
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_color('white')  # Asse delle ascisse (X)
        ax.spines['left'].set_color('white')
        
        ax.tick_params(axis='both', colors='white')
        ax.set_facecolor("#2b2b2b")
        # Creare un oggetto FigureCanvasTkAgg per il grafico
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill= "x")
        
        self.but = ctk.CTkButton(self, command= lambda: print(master.repoData) )
        self.but.pack()
      
        
       
      

        self.backButton = SideButton(self, self.master.previousPage, side = "left", imgpath="resources\left-arrow.png")
        self.backButton.place(x= -150, y= 10 )
            
        
        
        
        
        # Avvia il ciclo principale dell'applicazione
        
        

