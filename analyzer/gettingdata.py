import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
import csv

'''
nicedata.json is in analyzer/data
'''

DATA_PATH = Path(__file__).parent / "data"
TOTALCOUNT_PATH = DATA_PATH / "totalcounts-1.tsv"
NICEDATA_PATH = DATA_PATH / "nicedata.json"

def getWord(word):
    wordYears = []
    wordValues = []
    normalizationValues = {}
    with open(TOTALCOUNT_PATH, "r", newline='', encoding="utf-8") as dick:
        reader = csv.reader(dick, delimiter="\t") 
        for row in reader:
            for year in row:
                try:
                    # print(year)
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
        

def drawGraph(years, values, save_path=None):
    
    # plt.xlabel('Years')
    # plt.plot(years, values)
    # plt.ylim(bottom=0)
    # plt.grid(True, linestyle='--', alpha=0.5)

    # plt.show()


    # --- STYLE ---
    plt.style.use("seaborn-v0_8-whitegrid")  # clean, modern base style

    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)  # consistent display + save size

    # Smooth, thin line without markers
    ax.plot(years, values, color="#4285F4", linewidth=3)

    # --- AXIS & LABELS ---
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Word Frequency Over Time", fontsize=16, weight="bold")

    # Remove top/right borders for a cleaner look
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Lighter gridlines
    ax.grid(True, color="#E0E0E0")

    # Subtle tick styling
    ax.tick_params(colors="#555555", labelsize=10)

    # Tight layout ensures the saved figure matches the displayed one
    plt.tight_layout()

    # --- SAVE EXACTLY AS DISPLAYED ---
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.show()

def graph_of_word(word, save_path=None):

    years, values = getWord(word)
    drawGraph(years, values, save_path)

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

if __name__ == '__main__':

    graph_of_word(input(), )
    # print(classify(list(years), list(values)))