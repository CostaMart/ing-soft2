import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from view.widgets.Graphics.ChartFrame import ChartFrame


class GridView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

    def create_grid(self, chart_data):
        num_cols = 1
        num_rows = len(chart_data)

        for i in range(num_rows):
            self.grid_rowconfigure(i, weight=1, minsize=2)
        for j in range(num_cols + 5):  # Aggiungi spazio per i pulsanti Next e Previous
            self.grid_columnconfigure(j, weight=1, minsize=5)

            for i in range(num_rows):
                for j in range(num_cols):
                    frame = ChartFrame(self, chart_data[i])
                    frame.grid(row=i, column=j + 1, sticky="nsew")

                    prev_button = tk.Button(self, text="Previous", command=frame.prev_chart)
                    prev_button.grid(row=i, column=0)

                    next_button = tk.Button(self, text="Next", command=frame.next_chart)
                    next_button.grid(row=i, column=num_cols + 1)

                    frame.set_buttons(prev_button, next_button)



# # Inizializza la finestra principale
# root = tk.Tk()
#
# # Crea un frame per la GridView
# grid_frame = tk.Frame(root)
# grid_frame.pack()
#
# # Inizializza la GridView all'interno del frame
# grid_view = GridView(grid_frame)
#
# # Crea i dati del grafico
# chart_data = [
#     [('pie', ['A', 'B'], [30, 70]), ('bar', ['X', 'Y'], [40, 60])],
#     [('line', [1, 2, 3, 4, 5], [10, 20, 15, 25, 30]), ('pie', ['C', 'D'], [45, 55])]
# ]
#
# # Passa i dati del grafico alla GridView
# grid_view.create_grid(chart_data)
#
# # Avvia il loop principale
# root.mainloop()
