import json
import matplotlib.pyplot as plt
import csv
from analyzer.main import classify



def getWord(word):
    wordYears = []
    wordValues = []
    normalizationValues = {}
    with open("totalcounts-1.tsv", "r", newline='', encoding="utf-8") as dick:
        reader = csv.reader(dick, delimiter="\t") 
        for row in reader:
            for year in row:
                
                try:
                    normalizationValues[int(year.split(',')[0])]=str(year).split(',')[1]
                except:
                    pass
        with open('./nicedata_5_6.json') as f:
            data = json.load(f)
            cock = data[word]
            for j in cock:
                
                if normalizationValues[j['year']] and int(j['year'])>=1900:    
                    wordValues.append(float(j['volume_count'])/float(normalizationValues[j['year']]))
                    wordYears.append(int(j['year']))
           
    return wordYears, wordValues
        

def drawGraph(years, values):
    
    s = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    plt.xlabel('Years')
    plt.plot(years, values)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.show()

wrd = 'fuck'

years, values = getWord(wrd)

drawGraph(years, values)

print(classify(list(years), list(values)))