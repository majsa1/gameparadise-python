import os
import pandas as pd
import numpy as np

class CsvManager:
    def __init__(self):
        self._location = os.path.dirname(os.path.abspath(__file__))

    def getArrayFromCsv(self, fileName, columnName):
        file = os.path.join(self._location, fileName) 
        item = pd.read_csv(file, encoding = "ISO-8859-1",sep=",")
        list = item[columnName].values.tolist()
        array = np.array(list)
        return array