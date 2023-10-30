from PIL import Image, ImageTk, ImageOps
import tkinter as tk
import threading

class RotatingIcon(tk.Canvas):
    def __init__(self, master, iconPath, rotationSpeed = -3.5, backgroundColor = "black"):
        super().__init__(master, highlightthickness= 0 , bg= backgroundColor, width=30, height=28)
        
        self.keepRotating = True
        self.rotationSpeed = rotationSpeed

        # Carica l'immagine che vuoi ruotare
        self.image = Image.open(iconPath)
        self.image = self.image.resize((15,15), Image.LANCZOS)
        self.image = self.image = self.image.crop()
        self.image = ImageOps.expand(self.image, border=10, fill=backgroundColor)
        self.tk_image = ImageTk.PhotoImage(self.image, size= (15,15))
        self.image_id = self.create_image(10, 10, image=self.tk_image)

        # Avvia l'animazione
        t = threading.Thread(target= self.animate, args= [0])
        t.start()

    def animate(self, angle):
        """start animation on animation thread"""
        if self.keepRotating == True:
            # Ruota l'immagine di 10 gradi
            imageToDisplay = self.image.rotate(angle = angle, resample= Image.BICUBIC)
            self.tk_imageToDisplay = ImageTk.PhotoImage(imageToDisplay)
            
            self.delete(self.image_id)
            self.image_id = self.create_image(15, 15, image=self.tk_imageToDisplay)
            
            
            # Aggiorna l'immagine sul canvas
            self.itemconfig(id, image=self.tk_imageToDisplay)

            # Ripeti l'animazione dopo 100 millisecondi
            
            self.master.after(20, self.animate, (angle + self.rotationSpeed) % 360)

    def destroy(self) -> None:
        self.keepRotating = False
        return super().destroy()