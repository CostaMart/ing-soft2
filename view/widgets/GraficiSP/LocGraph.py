
 

import tkinter
from matplotlib.figure import Figure
import model.chartOrganizer as co
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LocGraph():
    
    
    def __init__(self,master, process_dict):
        fig_loc = Figure(figsize=(10, 10), dpi=100)
        self.ax_loc = fig_loc.add_subplot(111)
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.ax_loc.plot(y2, x1, label='Linee di Codice', marker='o')
        self.ax_loc.plot(y2, x2, label='Linee vuote', marker='o')
        self.ax_loc.plot(y2, x3, label='Commenti', marker='o')
        self.ax_loc.legend()
        self.ax_loc.set_title("Amount (in LOC) of previous changes")
        self.ax_loc.set_xticklabels(y2, rotation=30, ha='right')
        self.canvas_loc = FigureCanvasTkAgg(fig_loc, master=master)
        
    def draw(self):
        self.canvas_loc.draw()
        
    def pack(self,**args):
        self.canvas_loc.get_tk_widget().pack(**args)
    
          
        

class RevisionGraph():
    
    
    def __init__(self, master, process_dict):
        
       
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        # Grafico revisioni
        fig_revision = Figure(figsize=(10, 10), dpi=100)
        self.ax_revision = fig_revision.add_subplot(111)
        x, y = co.revision_number(process_dict)
        self.ax_revision.bar(y2, x)
        self.ax_revision.legend()
        self.ax_revision.set_title("Number of revisions")
        self.ax_revision.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_revision = FigureCanvasTkAgg(fig_revision, master=master)
        

    def draw(self):
        self.canvas_revision.draw()
        
    def pack(self,**args):
        self.canvas_revision.get_tk_widget().pack(**args)
        

class BugFixGraph():
    
    def __init__(self, master, process_dict):
       
     
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.fig_bugfix = Figure(figsize=(10, 10), dpi=100)
        self.ax_bugfix = self.fig_bugfix.add_subplot(111)
        x, y = co.bugfix(process_dict)
        self.ax_bugfix.bar(y2, x)
        self.ax_bugfix.legend()
        self.ax_bugfix.set_title("Number of bugfix commits")
        self.ax_bugfix.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_bugfix = FigureCanvasTkAgg(self.fig_bugfix, master=master)
        

       

    
    def draw(self):
        self.canvas_bugfix.draw()
        
    def pack(self,**args):
        self.canvas_bugfix.get_tk_widget().pack(**args)
    

class ChurnGraph():
    
    def __init__(self, master, process_dict):
        
        
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.fig_codechurn = Figure(figsize=(10, 10), dpi=100)
        self.ax_codechurn = self.fig_codechurn.add_subplot(111)
        x, y = co.codeC(process_dict)
        self.ax_codechurn.bar(y2, x)
        self.ax_codechurn.legend()
        self.ax_codechurn.set_title("Number of code churn commits")
        self.ax_codechurn.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_codechurn = FigureCanvasTkAgg(self.fig_codechurn, master=master)
        
      
    def draw(self):
        self.canvas_codechurn.draw()
        
    def pack(self,**args):
        self.canvas_codechurn.get_tk_widget().pack(**args)
    
class WeeksGraph():
    
    def __init__(self, master, process_dict):
        
        
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.fig_weeks = Figure(figsize=(10, 10), dpi=100)
        self.ax_weeks = self.fig_weeks.add_subplot(111)
        x, y = co.weeks(process_dict)
        self.ax_weeks.bar(y2, x)
        self.ax_weeks.legend()
        self.ax_weeks.set_title("Number of weeks")
        self.ax_weeks.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_weeks = FigureCanvasTkAgg(self.fig_weeks, master=master)
       
    def draw(self):
        self.canvas_weeks.draw()
        
    def pack(self,**args):
        self.canvas_weeks.get_tk_widget().pack(**args)

class AuthorsGraph():
    
    def __init__(self, master, process_dict):
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        self.fig_authors = Figure(figsize=(10, 10), dpi=100)
        self.ax_authors = self.fig_authors.add_subplot(111)
        x, y = co.authors(process_dict)
        self.ax_authors.bar(y2, x)
        self.ax_authors.legend()
        self.ax_authors.set_title("Number of authors")
        self.ax_authors.set_xticklabels(y2, rotation=30, ha='right')

        self.canvas_authors = FigureCanvasTkAgg(self.fig_authors, master=self)
     

        
    def draw(self):
        self.canvas_authors.draw()
        
    def pack(self,**args):
        self.canvas_authors.get_tk_widget().pack(**args)
    