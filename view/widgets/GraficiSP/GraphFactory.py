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
    
    @staticmethod
    def _baseGraph(master) -> Union[Figure, Axes]:
        """ crea la base del grafico """
        fig_loc = Figure(figsize=(8,5), dpi=100)
        ax_loc = fig_loc.add_subplot(111)
        fig_loc.subplots_adjust(left=0.176, bottom=0.205, right=0.9, top=0.88, wspace=0.2, hspace=0)
        fig_loc.set_facecolor("#2b2b2b")
        ax_loc.set_facecolor("#2b2b2b")
        ax_loc.spines['top'].set_visible(False)
        ax_loc.spines['right'].set_visible(False)
        ax_loc.spines['bottom'].set_color("white")
        ax_loc.spines['left'].set_color("white")
        ax_loc.tick_params(axis='x', colors='white')
        ax_loc.tick_params(axis='y', colors='white')
        ax_loc.legend()
        
        return fig_loc, ax_loc
    
    @staticmethod
    def makeLocGraph(master, process_dict) -> Union[tk.Canvas, NavigationToolbar2Tk]:
        
        fig, axloc= GraphFactory._baseGraph(master)
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.plot(y2, x1, label='Linee di Codice', marker='o')
        axloc.plot(y2, x2, label='Linee vuote', marker='o')
        axloc.plot(y2, x3, label='Commenti', marker='o')
        axloc.set_title("Amount (in LOC) of previous change" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        canvas_loc = FigureCanvasTkAgg(fig, master=master)
        toolbar_revision = NavigationToolbar2Tk(canvas_loc)
        canvas_loc.draw()
        return canvas_loc.get_tk_widget(), toolbar_revision