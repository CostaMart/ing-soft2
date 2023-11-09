
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class ChartFrame(tk.Frame):
    def __init__(self, master=None, chart_data=None):
        super().__init__(master)
        self.chart_data = chart_data
        self.current_chart_index = 0
        self.prev_button = None
        self.next_button = None
        self.show_chart()

    def show_chart(self):
        # Pulisci il frame prima di mostrare un nuovo grafico
        for widget in self.winfo_children():
            widget.destroy()

        chart_type, labels, sizes = self.chart_data[self.current_chart_index]
        fig, ax = plt.subplots(figsize=(2, 2), dpi=100)
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
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack()

        # Disabilita i pulsanti "Next" e "Previous" se si è all'inizio o alla fine della lista
        if self.prev_button is not None:
            if self.current_chart_index == 0:
                self.prev_button.config(state=tk.DISABLED)
            else:
                self.prev_button.config(state=tk.NORMAL)

        if self.next_button is not None:
            if self.current_chart_index == len(self.chart_data) - 1:
                self.next_button.config(state=tk.DISABLED)
            else:
                self.next_button.config(state=tk.NORMAL)

    def set_buttons(self, prev_button, next_button):
        self.prev_button = prev_button
        self.next_button = next_button

    def next_chart(self):
        self.current_chart_index += 1
        self.show_chart()

    def prev_chart(self):
        self.current_chart_index -= 1
        self.show_chart()
