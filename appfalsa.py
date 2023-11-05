import customtkinter as ctk
from view.ProjectMetricsPage import ProjectMetricsPage
def button_callback():
    print("Button clicked!")

app = ctk.CTk()
app.geometry("800x500")
button = ProjectMetricsPage(app, True)
button.pack(fill = "both", expand = True)

app.mainloop()