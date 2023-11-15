
 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import model.chartOrganizer as co
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 # Assicurati di importare correttamente il modulo co con la funzione loc_number

class LocGraph():
    def __init__(self, master, process_dict):
        fig_loc = Figure(figsize=(5, 5), dpi=100)
        self.ax_loc = fig_loc.add_subplot(111)
        fig_loc.set_facecolor("#2b2b2b")
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.ax_loc.plot(y2, x1, label='Linee di Codice', marker='o')
        self.ax_loc.plot(y2, x2, label='Linee vuote', marker='o')
        self.ax_loc.plot(y2, x3, label='Commenti', marker='o')
        self.ax_loc.set_facecolor("#2b2b2b")
        self.ax_loc.spines['top'].set_visible(False)
        self.ax_loc.spines['right'].set_visible(False)
        self.ax_loc.spines['bottom'].set_color("white")
        self.ax_loc.spines['left'].set_color("white")
        self.ax_loc.tick_params(axis='x', colors='white')
        self.ax_loc.tick_params(axis='y', colors='white')
        self.ax_loc.legend()
        self.ax_loc.set_title("Amount (in LOC) of previous changes", color="white")
        self.ax_loc.set_xticklabels(y2, rotation=30, ha='right')
        
        if len(y2) < 10:
            right = len(y2) -1
        else:
            right = 10
        self.ax_loc.set_xlim(left = y2[0], right = y2[right])
        
        self.canvas_loc = FigureCanvasTkAgg(fig_loc, master=master)

    def draw(self):
        self.canvas_loc.draw()

    def pack(self, **args):
        self.canvas_loc.get_tk_widget().pack(**args)

    
      
        

class RevisionGraph():
    
    
    def __init__(self, master, process_dict):
        
       
        x, y = co.revision_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        # Grafico revisioni
        fig_revision = Figure(figsize=(5, 5), dpi=100)
        fig_revision.set_facecolor("#2b2b2b")
        
        self.ax_revision = fig_revision.add_subplot(111)
        self.ax_revision.bar(y2, x)
        self.ax_revision.set_facecolor("#2b2b2b")
        self.ax_revision.spines['top'].set_visible(False)
        self.ax_revision.spines['right'].set_visible(False)
        self.ax_revision.spines['bottom'].set_color('#2b2b2b')
        self.ax_revision.spines['left'].set_color('#2b2b2b')
        self.ax_revision.spines['bottom'].set_color("white")
        self.ax_revision.spines['left'].set_color("white")
        self.ax_revision.tick_params(axis='x', colors='white')
        self.ax_revision.tick_params(axis='y', colors='white')
        self.ax_revision.legend()
        self.ax_revision.set_title("Number of revisions", color= "white")
        self.ax_revision.set_xticklabels(y2, rotation=30, ha='right')

        
        if len(y2) < 10:
            right = len(y2) -1
        else:
            right = 10
        self.ax_revision.set_xlim(left = y2[0], right = y2[right])
        
        self.canvas_revision = FigureCanvasTkAgg(fig_revision, master=master)
        self.canvaswidgt = self.canvas_revision.get_tk_widget()
        

    def draw(self):
        self.canvas_revision.draw()
        
    def pack(self,**args):
    
        self.canvaswidgt.pack(**args)
        

class BugFixGraph():
    
    def __init__(self, master, process_dict):
       
     
        x, y = co.bugfix(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.fig_bugfix = Figure(figsize=(5, 5), dpi=100)
        self.fig_bugfix.set_facecolor("#2b2b2b")
        self.ax_bugfix = self.fig_bugfix.add_subplot(111)
        self.ax_bugfix.bar(y2, x)
        self.ax_bugfix.set_facecolor("#2b2b2b")
        self.ax_bugfix.spines['top'].set_visible(False)
        self.ax_bugfix.spines['right'].set_visible(False)
        self.ax_bugfix.spines['bottom'].set_color('white')
        self.ax_bugfix.spines['left'].set_color('white')
        self.ax_bugfix.tick_params(axis='x', colors='white')
        self.ax_bugfix.tick_params(axis='y', colors='white')
        self.ax_bugfix.legend()
        self.ax_bugfix.set_title("Number of bugfix commits", color= "white")
        self.ax_bugfix.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_bugfix = FigureCanvasTkAgg(self.fig_bugfix, master=master)
        
        if len(y2) < 10:
            right = len(y2) -1
        else:
            right = 10
        self.ax_bugfix.set_xlim(left = y2[0], right = y2[right])

       

    
    def draw(self):
        self.canvas_bugfix.draw()
        
    def pack(self,**args):
        self.canvas_bugfix.get_tk_widget().pack(**args)
    

class ChurnGraph():
    
    def __init__(self, master, process_dict):
        
        
        x, y = co.codeC(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.fig_codechurn = Figure(figsize=(5, 5), dpi=100)
        self.fig_codechurn.set_facecolor("#2b2b2b")
        self.ax_codechurn = self.fig_codechurn.add_subplot(111)
        self.ax_codechurn.bar(y2, x)
        self.ax_codechurn.set_facecolor("#2b2b2b")
        self.ax_codechurn.spines['top'].set_visible(False)
        self.ax_codechurn.spines['right'].set_visible(False)
        self.ax_codechurn.spines['bottom'].set_color('white')
        self.ax_codechurn.spines['left'].set_color('white')
        self.ax_codechurn.tick_params(axis='x', colors='white')
        self.ax_codechurn.tick_params(axis='y', colors='white')
        self.ax_codechurn.legend()
        self.ax_codechurn.set_title("Number of code churn commits", color= "white")
        self.ax_codechurn.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_codechurn = FigureCanvasTkAgg(self.fig_codechurn, master=master)
        
        if len(y2) < 10:
            right = len(y2) -1
        else:
            right = 10
        self.ax_codechurn.set_xlim(left = y2[0], right = y2[right])
      
    def draw(self):
        self.canvas_codechurn.draw()
        
    def pack(self,**args):
        self.canvas_codechurn.get_tk_widget().pack(**args)
    
class WeeksGraph():
    
    def __init__(self, master, process_dict):
        
        
        x, y = co.weeks(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.fig_weeks = Figure(figsize=(5, 5), dpi=100)
        self.fig_weeks.set_facecolor("#2b2b2b")
        self.ax_weeks = self.fig_weeks.add_subplot(111)
        self.ax_weeks.bar(y2, x)
        self.ax_weeks.set_facecolor("#2b2b2b")
        self.ax_weeks.spines['top'].set_visible(False)
        self.ax_weeks.spines['right'].set_visible(False)
        self.ax_weeks.spines['bottom'].set_color('white')
        self.ax_weeks.spines['left'].set_color('white')
        self.ax_weeks.tick_params(axis='x', colors='white')
        self.ax_weeks.tick_params(axis='y', colors='white')
        self.ax_weeks.legend()
        self.ax_weeks.set_title("Number of weeks", color= "white")
        self.ax_weeks.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_weeks = FigureCanvasTkAgg(self.fig_weeks, master=master)
        if len(y2) < 10:
            right = len(y2) -1
        else:
            right = 10
        self.ax_weeks.set_xlim(left = y2[0], right = y2[right])
       
       
       
    def draw(self):
        self.canvas_weeks.draw()
        
    def pack(self,**args):
        self.canvas_weeks.get_tk_widget().pack(**args)

class AuthorsGraph():
    
    def __init__(self, master, process_dict):
        x, y = co.authors(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.fig_authors = Figure(figsize=(5, 5), dpi=100)
        self.fig_authors.set_facecolor("#2b2b2b")
        self.ax_authors = self.fig_authors.add_subplot(111)
        self.ax_authors.bar(y2, x)
        self.ax_authors.set_facecolor("#2b2b2b")
        self.ax_authors.spines['bottom'].set_color('white')
        self.ax_authors.spines['left'].set_color('white')
        self.ax_authors.spines['top'].set_visible(False)
        self.ax_authors.spines['right'].set_visible(False)
        self.ax_authors.tick_params(axis='x', colors='white')
        self.ax_authors.tick_params(axis='y', colors='white')
        self.ax_authors.legend()
        self.ax_authors.set_title("Number of authors", color= "white")
        self.ax_authors.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_authors = FigureCanvasTkAgg(self.fig_authors, master=master)

        if len(y2) < 10:
            right = len(y2) -1
        else:
            right = 10
        self.ax_authors.set_xlim(left = y2[0], right = y2[right])
        
        
    def draw(self):
        self.canvas_authors.draw()
        
    def pack(self,**args):
        self.canvas_authors.get_tk_widget().pack(**args)


class CboGraph():

    def __init__(self,master, process_dict):
        fig_cbo = Figure(figsize=(10, 10), dpi=100)
        self.ax_cbo = fig_cbo.add_subplot(111)
        x, y = co.cbo(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.ax_cbo.plot(y2, x, label='Valore cbo', marker='o')
        self.ax_cbo.set_title("CBO (Coupling Between Object classes)")
        self.ax_cbo.set_xticklabels(y2, rotation=30, ha='right')
        self.canvas_cbo = FigureCanvasTkAgg(fig_cbo, master=master)



    def draw(self):
        self.canvas_cbo.draw()
        
    def pack(self,**args):
        self.canvas_cbo.get_tk_widget().pack(**args)
    

class WmcGraph():

    def __init__(self,master, process_dict):
        fig_wmc = Figure(figsize=(10, 10), dpi=100)
        self.ax_wmc = fig_wmc.add_subplot(111)
        x, y = co.wmc(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.ax_wmc.plot(y2, x, label='Valore wmc', marker='o')
        self.ax_wmc.set_title("WMC (Weighted Methods per Class)")
        self.ax_wmc.set_xticklabels(y2, rotation=30, ha='right')
        self.canvas_wmc = FigureCanvasTkAgg(fig_wmc, master=master)

    def draw(self):
        self.canvas_wmc.draw()

    def pack(self,**args):
        self.canvas_wmc.get_tk_widget().pack(**args)    


class DitGraph():

    def __init__(self,master, process_dict):
        fig_dit = Figure(figsize=(10, 10), dpi=100)
        self.ax_dit = fig_dit.add_subplot(111)
        x, y = co.dit(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.ax_dit.plot(y2, x, label='Valore dit', marker='o')
        self.ax_dit.set_title("DIT (Depth of Inheritance)")
        self.ax_dit.set_xticklabels(y2, rotation=30, ha='right')
        self.canvas_dit = FigureCanvasTkAgg(fig_dit, master=master)

    def draw(self):
        self.canvas_dit.draw()

    def pack(self,**args):
        self.canvas_dit.get_tk_widget().pack(**args)    


class NocGraph():

    def __init__(self,master, process_dict):
        fig_noc = Figure(figsize=(10, 10), dpi=100)
        self.ax_noc = fig_noc.add_subplot(111)
        x, y = co.noc(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.ax_noc.plot(y2, x, label='Valore noc', marker='o')
        self.ax_noc.set_title("NOC (Number of Children) ")
        self.ax_noc.set_xticklabels(y2, rotation=30, ha='right')
        self.canvas_noc = FigureCanvasTkAgg(fig_noc, master=master)

    def draw(self):
        self.canvas_noc.draw()

    def pack(self,**args):
        self.canvas_noc.get_tk_widget().pack(**args)   
        

class RfcGraph():

    def __init__(self,master, process_dict):
        fig_rfc = Figure(figsize=(10, 10), dpi=100)
        self.ax_rfc = fig_rfc.add_subplot(111)
        x, y = co.rfc(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.ax_rfc.plot(y2, x, label='Valore rfc', marker='o')
        self.ax_rfc.set_title("RFC (Response for a Class)")
        self.ax_rfc.set_xticklabels(y2, rotation=30, ha='right')
        self.canvas_rfc= FigureCanvasTkAgg(fig_rfc, master=master)

    def draw(self):
        self.canvas_rfc.draw()

    def pack(self,**args):
        self.canvas_rfc.get_tk_widget().pack(**args)   
        

class LcomGraph():

    def __init__(self,master, process_dict):
        fig_lcom = Figure(figsize=(10, 10), dpi=100)
        self.ax_lcom = fig_lcom.add_subplot(111)
        x, y = co.lcom(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.ax_lcom.plot(y2, x, label='Valore lcom', marker='o')
        self.ax_lcom.set_title("LCOM (Lack of Cohesion of Methods)")
        self.ax_lcom.set_xticklabels(y2, rotation=30, ha='right')
        self.canvas_lcom= FigureCanvasTkAgg(fig_lcom, master=master)

    def draw(self):
        self.canvas_lcom.draw()

    def pack(self,**args):
        self.canvas_lcom.get_tk_widget().pack(**args)  
        