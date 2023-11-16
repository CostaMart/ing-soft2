from typing import Union
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import model.chartOrganizer as co
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from icecream import ic

class GraphFactory:
    """ factory class che produce il grafico richiesto """
    
    def __init__(self) -> None:
        self.graphsList =  {name.lstrip('_'): getattr(self, name) for name in dir(self) if callable(getattr(self, name))}
        
    
    def makeGraph(self, master, graph : str, process_dict) -> Union[tk.Canvas, NavigationToolbar2Tk]:
        """ crea il grafico generale, poi chiamando uno dei metodi di specializzazione crea il grafico specializzato richiesto """
        
        fig_loc = Figure(figsize=(8,5), dpi=100)
        ax_loc = fig_loc.add_subplot(111)
        fig_loc.set_facecolor("#2b2b2b")
        ax_loc.set_facecolor("#2b2b2b")
        ax_loc.spines['top'].set_visible(False)
        ax_loc.spines['right'].set_visible(False)
        ax_loc.spines['bottom'].set_color("white")
        ax_loc.spines['left'].set_color("white")
        ax_loc.tick_params(axis='x', colors='white')
        ax_loc.tick_params(axis='y', colors='white')

        graphProducer = self.graphsList[graph]
        fig = graphProducer(process_dict, fig_loc, ax_loc)
        
        
      
        canvas_loc = FigureCanvasTkAgg(fig, master=master)
        toolbar_revision = NavigationToolbar2Tk(canvas_loc)
        canvas_loc.draw()
       
        return canvas_loc.get_tk_widget(), toolbar_revision
    
   
    def _Loc(self, process_dict, fig, axloc) -> Figure:
        """ contiene solo la specializzazione del grafico, vengono aggiunti gli elementi per renderlo un grafico LOC """
        
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.plot(y2, x1, label='Linee di Codice', marker='o')
        axloc.plot(y2, x2, label='Linee vuote', marker='o')
        axloc.plot(y2, x3, label='Commenti', marker='o')
        axloc.set_title("Amount (in LOC) of previous change" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        axloc.legend()
        
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        
        return fig