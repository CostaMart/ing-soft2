from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import customtkinter as ctk

class ChartApp:
    def __init__(self, master):
        self.master = master
        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(padx=10, pady=10)

    def show_chart(self, chart_type, labels, sizes):
        if chart_type == 'pie':
            self.create_pie_chart(labels, sizes)
        elif chart_type == 'line':
            self.create_line_chart(labels, sizes)
        elif chart_type == 'bar':
            self.create_bar_chart(labels, sizes)

    def create_bar_chart(self, labels, values):
        fig, ax = plt.subplots()
        ax.bar(labels, values, color='skyblue')
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().pack()
        ax.grid(True)  # Mostra le griglie di fondo

    def create_line_chart(self, x, y):
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', color='b', label='Data')
        ax.set_xlabel('X-Axis')
        ax.set_ylabel('Y-Axis')
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().pack()
        ax.grid(True)  # Mostra le griglie di fondo

    def create_pie_chart(self, labels, sizes):
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().pack()
        ax.grid(True)  # Mostra le griglie di fondo

    def update_chart(self, chart_type, labels, sizes):
        self.clear_chart()  # Cancella eventuali grafici già presenti nel frame
        self.show_chart(chart_type, labels, sizes)

    def clear_chart(self):
        for widget in self.frame.winfo_children():
            widget.destroy()