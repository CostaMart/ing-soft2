import os.path
import tkinter as tk
from tkinter import font
import customtkinter as ctk
from view.widgets.SideButton import SideButton
from view.widgets.Plot import PlotCartesian
from controller.ProjectMetricsContoller import MetricsPageContoller
import tkinter as tk
from icecream import ic

class ProjectMetricsPage(ctk.CTkScrollableFrame):
    
    def __init__(self, master):
        super().__init__(master = master)
        ctk.set_appearance_mode("dark")
       
        self.controller = MetricsPageContoller() 
        self.repoData = self.controller.getLocalRepoData()
        self.master = master
        
        self.initTopFrames()
        
        p = PlotCartesian(self, self.repoData.name, [1,2,3,4], [1,1,1,1])
        p.pack(fill = "x")
        
        self.but = ctk.CTkButton(self, command= lambda: print(master.repoData) )
        self.but.pack()
        left_arrow = os.path.join("resources","left-arrow.png")
        
        self.backButton = SideButton(self, self.master.previousPage, side = "left", imgpath=left_arrow)
        self.backButton.place(x= -150, y= 10 )
            
        
        
# ----------------------------- GESTIONE UI METHODS -----------------------------        
    def initTopFrames(self):
       
        self.externalProjectFrame = ctk.CTkFrame(self)
        self.externalProjectFrame.pack(pady = 12)
        
        self.label = ctk.CTkLabel(self.externalProjectFrame, text= self.repoData.name)
        self.label.pack()
        my_font = ctk.CTkFont(weight= "bold", size= 16)

        self.internalFrame = ctk.CTkFrame(self.externalProjectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.internalFrame.pack()
        self.projectFrame = ctk.CTkFrame(self.internalFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.projectFrame.pack(pady= 10, padx = 10)
        
        
        self.subFrame1 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame1.pack(anchor = "w", padx = 10)
        self.label = ctk.CTkLabel(self.subFrame1, text= f"Git URL: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame1, text= f"{self.repoData.git_url}")
        self.label.pack()
        
        self.subFrame2 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame2.pack(anchor = "w", padx = 10)
        self.label = ctk.CTkLabel(self.subFrame2, text= f"project license: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame2, text= f"{self.repoData.license['name']}")
        self.label.pack()
        
        self.subFrame3 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame3.pack(anchor = "w", padx = 10)
        self.label = ctk.CTkLabel(self.subFrame3, text= f"epo owner: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame3, text= f"r{self.repoData.owner['login']}")
        self.label.pack()
        
        self.subFrame4 = ctk.CTkFrame(self.projectFrame, bg_color="#1d1e1e", fg_color="#1d1e1e")
        self.subFrame4.pack(anchor = "w", padx = 10)
        self.label = ctk.CTkLabel(self.subFrame4, text= f"Repo owner URL: ", font = my_font)
        self.label.pack(side = ctk.LEFT)
        self.label = ctk.CTkLabel(self.subFrame4, text= f"{self.repoData.owner['url']}")
        self.label.pack()
       

