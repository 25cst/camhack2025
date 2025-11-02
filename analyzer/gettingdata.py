import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
import csv

'''
nice_data.json is in analyzer/data
'''

DATA_PATH = Path(__file__).parent / "data"
TOTALCOUNT_PATH = DATA_PATH / "totalcounts-1.tsv"
NICEDATA_PATH = DATA_PATH / "nice_data.json"

def getWord(word):
    wordYears = []
    wordValues = []
    normalizationValues = {}
    with open(TOTALCOUNT_PATH, "r", newline='', encoding="utf-8") as dick:
        reader = csv.reader(dick, delimiter="\t") 
        for row in reader:
            for year in row:
                try:
                    print(year)
                    year_data = year.split(',')
                    normalizationValues[int(year_data[0])]=int(year_data[1])
                except:
                    # print(year, "not found")
                    pass
    with open(NICEDATA_PATH) as f:
        data = json.load(f)
        cock = data[word]
        for j in cock:
            if normalizationValues[j['year']] and int(j['year'])>=1800:    
                wordValues.append(float(j['match_count'])/float(normalizationValues[j['year']]))
                wordYears.append(int(j['year']))
           
    return wordYears, wordValues
        

def drawGraph(years, values):
    
    plt.xlabel('Years')
    plt.plot(years, values)
    plt.ylim(bottom=0)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.show()

def classify(dataset, years):
    # Classifies a word's dataset into easy hard or bad
    smallstep = 1
    bigstep = 5
    
    smolmax = 0
    bigmax = 0
    biggestdata = 0
    smollestdata=0
    for i in range(years - bigstep):
        if i==1:
            smollestdata=dataset[i+1900]
        else:
            smollestdata=min(smollestdata, dataset[i+1900])
        biggestdata = max(biggestdata, dataset[i+1900])
        smolmax = max(dataset[i+1900 + bigstep] - dataset[i+1900], smolmax)
        bigmax = max(dataset[i+1900 + bigstep] - dataset[i+1900], bigmax)
    

    difficulty = (smolmax/(biggestdata - smollestdata)) + (bigmax/(biggestdata - smollestdata))
    return difficulty

wrd = 'the'

years, values = getWord(wrd)

drawGraph(years, values)

print(classify(list(years), list(values)))