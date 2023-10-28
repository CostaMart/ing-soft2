import tkinter as tk
import customtkinter as ctk
from ttkthemes import ThemedTk
from .ListBox import ListBox
from model.Domain import Repository



class RepoPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Ing_soft")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.maxsize(1600,1000)
        