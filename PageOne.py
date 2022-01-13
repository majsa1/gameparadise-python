import tkinter as tk
from tkinter import StringVar
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CsvManager import CsvManager

class PageOne(tk.Frame): 
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, background = "#8B8989", *args, **kwargs)
        
        # textvariable, initialize radiobuttons with "numbers"
        self.choice = StringVar(self, "Numbers")

        # set colors and font
        self.fgColor = "white"
        self.bgColor = "#8B8989"
        self.font = "Verdana"

        # fetch data
        csvManager = CsvManager()
        self.ageArray = csvManager.getArrayFromCsv("Klant+leeftijd.csv", "LEEFTIJD")
        self.genderArray = csvManager.getArrayFromCsv("Klant+leeftijd.csv", "GESLACHT")

        # initialize charts & widgets
        self.getChartData()
        self.createCharts()
        self.createWidgets()       

    def getChartData(self):
        # data for pie chart
        self.genderLabels, self.genderCounts = np.unique(self.genderArray, return_counts = True) 

        # data for bar chart
        f = np.where(self.genderArray == "V")
        self.femaleAges = self.ageArray[f]
        m = np.where(self.genderArray == "M")
        self.maleAges = self.ageArray[m]

        bins = [[20, 30], [30, 40], [40, 50], [50, 60], [60, 70]]
        totalAgeCounts = np.array([])
        self.femaleAgeCounts = np.array([], int)
        self.maleAgeCounts = np.array([], int)
     
        for age in bins:
            totalAgeCounts = np.append(totalAgeCounts, np.count_nonzero((self.ageArray >= age[0]) & (self.ageArray < age[1])))
            self.femaleAgeCounts = np.append(self.femaleAgeCounts, np.count_nonzero((self.femaleAges >= age[0]) & (self.femaleAges < age[1])))
            self.maleAgeCounts = np.append(self.maleAgeCounts, np.count_nonzero((self.maleAges >= age[0]) & (self.maleAges < age[1])))

        self.femaleAgePercentages = (self.femaleAgeCounts / totalAgeCounts).tolist()
        self.femaleAgePercentages = ["{:.0%}".format(number) for number in self.femaleAgePercentages]
        self.maleAgePercentages = (self.maleAgeCounts / totalAgeCounts).tolist()
        self.maleAgePercentages = ["{:.0%}".format(number) for number in self.maleAgePercentages]

    def createCharts(self): 
        fColor = "#FFC125"
        mColor = "#5B5B5B"

        figure = Figure(figsize = (7.5, 4.0), dpi = 100)
    
        # pie chart
        chart1 = figure.add_subplot(121)
        explode = (0, 0.05)
        legendLabels = ["Man" if x == "M" else "Vrouw" for x in self.genderLabels]
        pieLabels = self.genderCounts if self.choice.get() == "Numbers" else None
        autopct = None if self.choice.get() == "Numbers" else "%1.0f%%"
        chart1.pie(self.genderCounts, labels = pieLabels, labeldistance = 0.6, startangle = 90, explode = explode, 
            autopct = autopct, textprops = {"color": self.fgColor}, colors = [mColor, fColor])
        chart1.set_title("Diagram A", color = self.fgColor)
        chart1.legend(labels = legendLabels)

        # bar chart
        chart2 = figure.add_subplot(122)
        ageLabels = ["20-29", "30-39", "40-49", "50-60", "60+"]
        mBarLabels = self.maleAgeCounts if self.choice.get() == "Numbers" else self.maleAgePercentages
        fBarLabels = self.femaleAgeCounts if self.choice.get() == "Numbers" else self.femaleAgePercentages
        mbar = chart2.bar(ageLabels, self.maleAgeCounts, label = "Man", color = mColor)
        fbar = chart2.bar(ageLabels, self.femaleAgeCounts, bottom = self.maleAgeCounts, label = "Vrouw", color = fColor)
        chart2.bar_label(mbar, labels = mBarLabels, label_type = "center", color = self.fgColor)
        chart2.bar_label(fbar, labels = fBarLabels, label_type = "center", color = self.fgColor)
        chart2.set_ylabel("Aantal", color = self.fgColor)
        chart2.set_xlabel("Leeftijd", color = self.fgColor)
        chart2.tick_params(colors = self.fgColor, labelsize = "medium", width = 2)
        chart2.spines["bottom"].set_color(self.fgColor)
        chart2.spines["top"].set_color(self.fgColor) 
        chart2.spines["right"].set_color(self.fgColor)
        chart2.spines["left"].set_color(self.fgColor)
        chart2.set_title("Diagram B", color = self.fgColor)
        chart2.legend()

        figure.patch.set_facecolor(self.bgColor)
        chart2.patch.set_facecolor(self.bgColor) 
        figure.tight_layout(pad = 2.0)

        canvas = FigureCanvasTkAgg(figure, self)  
        canvas.draw()
        canvas.get_tk_widget().grid(row = 1, column = 1, rowspan = 8)

    def createWidgets(self):
        pad = 10
        tk.Label(self, text = "Klanten GAMEPARADISE", background = self.bgColor, foreground = self.fgColor, font = (self.font, 16)
            ).grid(column = 0, row = 0, sticky = "w", padx = pad, pady = pad)

        texts = [
            "Diagram A laat de verdeling van mannen en vrouwen zien in het klantenbestand van GameParadise.", 
            "In diagram B zijn de klanten van GameParadise gegroepeerd naar leeftijd en geslacht.",
            "Laat gegevens zien in:"
        ]
        for index, text in enumerate(texts):
            label = tk.Label(self, text = text, background = self.bgColor, foreground = self.fgColor, font = self.font, wraplength = 200, 
                justify = "left")
            label.grid(row = index + 3, column = 0, sticky = "w", padx = pad)

        countsButton = tk.Radiobutton(self, background = self.bgColor, foreground = self.fgColor, text = "Aantallen", font = self.font,
            variable = self.choice, value = "Numbers", command = self.createCharts)
        percentageButton = tk.Radiobutton(self, background = self.bgColor, foreground = self.fgColor, text = "Percentages", font = self.font,
            variable = self.choice, value = "Percentages", command = self.createCharts)
        countsButton.grid(row = 6, column = 0, sticky = "nw", padx = pad)
        percentageButton.grid(row = 6, column = 0, sticky = "sw", padx = pad)
