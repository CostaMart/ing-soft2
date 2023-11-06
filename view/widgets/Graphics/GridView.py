import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class GridView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()


    def create_grid(self, chart_data):
        num_rows = len(chart_data)
        num_cols = len(chart_data[0])
        for i in range(num_rows):
            self.grid_rowconfigure(i, weight=1, minsize=2)  # Imposta l'altezza minima delle righe
        for j in range(num_cols):
            self.grid_columnconfigure(j, weight=1, minsize=5)  # Imposta la larghezza minima delle colonne

        for i in range(num_rows):
            for j in range(num_cols):
                chart_type, labels, sizes = chart_data[i][j]
                frame = tk.Frame(self, bg="white", padx=2, pady=2)  # Riduci il valore di padx e pady
                frame.grid(row=i, column=j, sticky="nsew")
                self.show_chart(chart_type, labels, sizes, frame, width=5, height=5)  # Imposta larghezza e altezza del grafico

    def show_chart(self, chart_type, labels, sizes, frame, width, height):
        fig, ax = plt.subplots(figsize=(width , height ), dpi=100)  # Regola la dimensione del grafico
        if chart_type == 'pie':
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        elif chart_type == 'line':
            ax.plot(labels, sizes, marker='o', color='b', label='Data')
            ax.set_xlabel('X-Axis')
            ax.set_ylabel('Y-Axis')
            ax.legend()
        elif chart_type == 'bar':
            ax.bar(labels, sizes, color='skyblue')
            ax.set_xlabel('Categories')
            ax.set_ylabel('Values')
        ax.grid(True)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack()
