import tkinter as tk
from tkinter import ttk
from PageOne import PageOne
from PageTwo import PageTwo
import os
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self, title = "GameParadise"): 
        super().__init__()
        
        self.title(title)
        self.geometry("1080x550+75+75")
        self.resizable(False, False)

        self.__createWidgets(tab2 = "Klanten", tab3 = "Catalogus") # creates notebook and widgets on root window
        
    def __createWidgets(self, tab1 = "Start", tab2 = "Figure 1", tab3 = "Figure 2"): 
        style = ttk.Style()
        style.map("TNotebook.Tab", foreground = [("selected", "black")]) # solves invisible active title text in conda environment with Python 3.9.7

        self.notebook = ttk.Notebook(self) 
        self.notebook.pack()

        # adding tabs & widgets:
        self.mainPage = tk.Frame(self.notebook, relief = tk.RAISED, borderwidth = 5)
        self.notebook.add(self.mainPage, text = tab1)

        self.pageOne = PageOne(self.notebook, relief = tk.RAISED, borderwidth = 5) 
        self.notebook.add(self.pageOne, text = tab2)

        self.pageTwo = PageTwo(self.notebook, relief = tk.RAISED, borderwidth = 5)
        self.notebook.add(self.pageTwo, text = tab3)

        font = "Verdana"
        tk.Label(self.mainPage, text = "Rapportage GameParadise", font = (font, 16, "bold"), foreground = "orange").grid(row = 0, column = 1, sticky = "w", pady = 20)
        tk.Label(self.mainPage, text = "Selecteer rapportage:", font = (font, 12, "bold"), foreground = "#5B5B5B").grid(row = 1, column = 0, sticky = "w", padx = 20)
        tk.Button(self.mainPage, text = "Klanten", command = lambda: self.notebook.select(tab_id = self.pageOne)).grid(row = 1, column = 1, sticky = "w")
        tk.Button(self.mainPage, text = "Catalogus", command = lambda: self.notebook.select(tab_id = self.pageTwo)).grid(row = 2, column = 1, sticky = "w")

        # adding image
        folder = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(folder, "GameParadise.png") 
        
        image = Image.open(file)
        resizedImg = image.resize((int(image.width * 0.5), int(image.height * 0.5)))
        tkImg = ImageTk.PhotoImage(resizedImg)
        
        self.imageLabel = tk.Label(self.mainPage, relief = tk.RAISED, borderwidth = 3)
        self.imageLabel.img = tkImg
        self.imageLabel.config(image = self.imageLabel.img)
        self.imageLabel.grid(row = 1, rowspan = 10, column = 2, padx = 25, pady = 25)


