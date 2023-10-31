import tkinter as tk
from tkinter import font
import customtkinter as ctk
from ttkthemes import ThemedTk
from .widgets.ListBox import ListBox
from model.Domain import Repository
from controller.mainPageContoller import get_selected_repo, request_for_repos
from view.widgets.SideButton import SideButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt

def draw_tree_graph(arg):
    G = nx.DiGraph()
    G.add_node("A")
    G.add_edge("A", "B")
    G.add_edge("A", "C")
    G.add_edge("B", "D")
    G.add_edge("B", "E")
    G.add_edge("C", "F")

    pos = nx.spring_layout(G)  # Posizionamento dei nodi nel grafico

    # Creare un frame per il grafo ad albero
    frame_tree = ttk.Frame(arg)
    frame_tree.pack()

    # Creare un oggetto Figure di Matplotlib per il grafo ad albero
    fig_tree = Figure(figsize=(4, 3), dpi=100)
    ax_tree = fig_tree.add_subplot(111)

    # Aggiungi un'etichetta per ciascun nodo
    node_labels = {node: node for node in G.nodes}

    # Aggiungi un evento quando il mouse passa sopra un nodo
    def on_node_hover(event):
        if event.xdata is not None and event.ydata is not None:
            for node in G.nodes:
                
                x, y = pos[node]
                if abs(x - event.xdata) < 0.1 and abs(y - event.ydata) < 0.1:
                    ax_tree.set_title(f"Node: {node}", fontsize=12, color='blue')
                    print(f"{node}")
                else:
                    ax_tree.set_title("")

            tree_canvas.draw()

    tree_canvas = FigureCanvasTkAgg(fig_tree, master=frame_tree)
    tree_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Disegna il grafo ad albero con etichette per i nodi
    nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=50, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", ax=ax_tree)
    tree_canvas.draw()

    tree_canvas.mpl_connect('motion_notify_event', on_node_hover)



class ProjectMetricsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master)
        ctk.set_appearance_mode("dark")
       
        self.master = master
               
       
        
        
        self.frame = ctk.CTkFrame(self, width= 400, height= 400)
        self.frame.pack( fill = "x", expand= True)
        
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
                
      
        # Aggiungi un pulsante per disegnare il grafo ad albero
        draw_tree_graph(self)
      

        self.backButton = SideButton(self, self.master.previousPage, side = "left", imgpath="resources\left-arrow.png")
        self.backButton.place(x= -150, y= 10 )
            
        
        
        
        
        # Avvia il ciclo principale dell'applicazione
        
        

