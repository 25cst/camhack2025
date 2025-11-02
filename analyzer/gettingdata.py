import json
import matplotlib.pyplot as plt
import csv
from analyzer.main import classify
from pathlib import Path

'''
nice_data.json is in analyzer/data
'''

TOTALCOUNT_PATH = Path(__file__).parent / "data" / "totalcounts-1.tsv"
NICEDATA_PATH = Path(__file__).parent / "data" / "nice_data.json"

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

wrd = 'the'

years, values = getWord(wrd)

drawGraph(years, values)

print(classify(list(years), list(values)))