import customtkinter as ctk
from PIL.Image import Image, open


class SideButton(ctk.CTkFrame):
    def __init__(self, master, onPress, onPressParam = None, side = "right", imgpath = None):
        
        super().__init__(master, height= 30, width= 200, fg_color= "#1d1e1e")
        
        if imgpath == None:
            self.button = ctk.CTkLabel (self, text= "go to repo", bg_color= "#1d1e1e")
        else:
            img = ctk.CTkImage(dark_image= open(imgpath) )
            self.button = ctk.CTkLabel (self, image = img, text= "")
            
        if onPressParam == None:
            self.button.bind("<Button-1>" , command = lambda x: onPress())
        else:
            self.button.bind("<Button-1>" , command = lambda x: onPress(onPressParam))
            
        self.button.bind(sequence= "<Enter>", command= self.on_enter)
        self.button.bind(sequence= "<Leave>", command= self.on_leave)
        
        if side != "left":
            self.button.place(x = 10, y = 1.01)
        else:
            self.button.place(relx = 0.8)
            
            
    def on_enter(self, event):
            self.configure(fg_color="#847F7C")
            self.button.configure(fg_color="#847F7C")
            event.widget.configure(cursor="hand2")
                        
    def on_leave(self, event):
        self.configure(fg_color="#1d1e1e")
        self.button.configure(fg_color="#1d1e1e")
        event.widget.configure(cursor="arrow")