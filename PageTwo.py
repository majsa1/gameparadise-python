import tkinter as tk
from tkinter import StringVar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CsvManager import CsvManager

class PageTwo(tk.Frame): 
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, background = "#8B8989", *args, **kwargs)
        
        self.choice = StringVar(self, "Numbers")

        self.fgColor = "white"
        self.bgColor = "#8B8989"
        self.font = "Verdana"

        csvManager = CsvManager()
        self.gameOrConsoleArray = csvManager.getArrayFromCsv("Artikel+categorie.csv", "SPEL_OF_CONSOLE") 
        self.categoryArray = csvManager.getArrayFromCsv("Artikel+categorie.csv", "CATEGORIE") 
        self.typeArray = csvManager.getArrayFromCsv("Artikel+categorie.csv", "TYPE")

        self.getChartData()
        self.createCharts()
        self.createWidgets()

    def getChartData(self):
        # data for outer pie
        self.itemLabels, self.itemCounts = np.unique(self.gameOrConsoleArray, return_counts = True) 

        # data for inner pie
        # remove NULL-values
        self.categoryArray = np.delete(self.categoryArray, np.where(self.categoryArray == "nan")) 
        self.typeArray = np.delete(self.typeArray, np.where(self.typeArray == "nan"))

        self.categoryLabels, self.categoryCounts = np.unique(self.categoryArray, return_counts = True) 
        self.typeLabels, self.typeCounts = np.unique(self.typeArray, return_counts = True) 

        self.innerLabels = np.concatenate([self.typeLabels, self.categoryLabels])
        self.innerValues = np.concatenate([self.typeCounts, self.categoryCounts])

        # specify which labels to show in inner pie
        self.number = 3
        indexes = np.where(self.innerValues < self.number)
        
        for index in indexes:
            for i in index:
                self.innerLabels[i] = ""

        self.innerLabels = np.char.rstrip(self.innerLabels) # remove whitespaces from the end of labels

        # counts to be used for colormaps
        self.categoryAmount = np.count_nonzero(self.categoryCounts)
        self.typeAmount = np.count_nonzero(self.typeCounts)

    def createCharts(self): 
        figure = Figure(figsize = (4.0, 4.0), dpi = 100)
    
        chart = figure.add_subplot(111)
        labels = ["Consoles" if x == "CONSOLE" else "Spellen" for x in self.itemLabels]
        outerLabels = self.itemCounts if self.choice.get() == "Numbers" else None
        size = 0.3
        autopct = None if self.choice.get() == "Numbers" else "%1.0f%%"
        cmap1 = plt.get_cmap("gray") 
        cmap2 = plt.get_cmap("autumn") 
        outerColors = [cmap1(.6), cmap2(.6)]
        innerColors = [*cmap1(np.linspace(0, 1, self.typeAmount)), *cmap2(np.linspace(0, 1, self.categoryAmount))]
        
        chart.pie(self.itemCounts, radius = 1, labels = outerLabels, labeldistance = 1.25, wedgeprops = {"width": size, "edgecolor": "white"},
            autopct = autopct, pctdistance = 1.25, colors = outerColors, textprops = {"color": self.fgColor})

        chart.pie(self.innerValues, radius = 1 - size, labels = self.innerLabels, labeldistance = 1.0, wedgeprops = {"width": size, "edgecolor": self.fgColor}, 
            colors = innerColors, textprops = {"color": self.fgColor, "fontsize": 6, "weight": "bold"}, rotatelabels = True)

        chart.set_title("Diagram C", color = self.fgColor)
        chart.legend(labels = labels, loc = "lower right")

        figure.patch.set_facecolor(self.bgColor)
        chart.patch.set_facecolor(self.bgColor) 

        figure.tight_layout() 

        canvas = FigureCanvasTkAgg(figure, self)  
        canvas.draw()
        canvas.get_tk_widget().grid(row = 1, column = 1, rowspan = 10)

    def createWidgets(self):
        pad = 10
        tk.Label(self, text = "Catalogus GAMEPARADISE", background = self.bgColor, foreground = self.fgColor, font = (self.font, 16)
            ).grid(column = 0, row = 0, sticky = "w", padx = pad, pady = pad)

        texts = [ 
            "De buitenste ring van diagram C laat de verdeling van spellen en consoles zien die opgenomen zijn in de catalogus van GameParadise.", 
            f"In de binnenste ring zijn de spellen en de consoles verder verdeeld in categoriën en types. De categorieën en de types met {self.number} of meer artikelen zijn gelabeld.",
            "Reeds verkochte artikelen zijn buiten beschouwing gelaten.",
            "Laat gegevens zien in:"
        ]
        for index, text in enumerate(texts):
            self.label = tk.Label(self, text = text, background = self.bgColor, foreground = self.fgColor, font = self.font, wraplength = 250, 
                justify = "left")
            self.label.grid(row = index + 2, column = 0, sticky = "w", padx = pad)

        countsButton = tk.Radiobutton(self, background = self.bgColor, foreground = self.fgColor, text = "Aantallen", font = self.font,
            variable = self.choice, value = "Numbers", command = self.createCharts)
        percentageButton = tk.Radiobutton(self, background = self.bgColor, foreground = self.fgColor, text = "Percentages", font = self.font,
            variable = self.choice, value = "Percentages", command = self.createCharts)
        countsButton.grid(row = 6, column = 0, sticky = "w", padx = pad)
        percentageButton.grid(row = 7, column = 0, sticky = "w", padx = pad)