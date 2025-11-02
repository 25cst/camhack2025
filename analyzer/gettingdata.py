import json

import os
os.environ["MPLBACKEND"] = "Agg"

import matplotlib.pyplot as plt

import numpy as np
from pathlib import Path
import pandas as pd
import csv
import functools

'''
nicedata.json is in analyzer/data
'''

DATA_PATH = Path(__file__).parent / "data"
TOTALCOUNT_PATH = DATA_PATH / "totalcounts-1.tsv"
NICEDATA_PATH = DATA_PATH / "nicedata.json"
IMG_SAVE_PATH = Path(__file__).parent / "img" / "graph.png"

def getWord(word):
    normalizationValues = {}

    # load data
    with open(TOTALCOUNT_PATH, "r", newline='', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t") 
        for row in reader:
            for year in row:
                try:
                    # print(year)
                    year_data = year.split(',')
                    year_int = int(year_data[0])
                    normalizationValues[year_int]=int(year_data[1])
                except:
                    # print(year, "not found")
                    pass

    with open(NICEDATA_PATH) as f:
        data = json.load(f)
        word_data = data[word]
        # for j in cock:
        #     if normalizationValues[j['year']] and int(j['year'])>=1800:    
        #         wordValues.append(float(j['match_count'])/float(normalizationValues[j['year']]))
        #         wordYears.append(int(j['year']))
    
    years = np.array([int(entry["year"]) for entry in word_data if int(entry["year"]) >= 1800])
    counts = np.array([float(entry["match_count"]) for entry in word_data if int(entry["year"]) >= 1800])
    norms = np.array([normalizationValues.get(year, np.nan) for year in years])

    values = counts/norms
    values = (values/max(values))
    # normalise 0 to 1 so that we can overlay
    # values = values/max(values)

    return years, values
        

def drawGraph(years: list[np.ndarray], values: list[np.ndarray], words, save_path=None, show=False):
    """
    Plot one real word (first in list) and multiple guesses over time.
    The real word stays clearly visible; guesses fade progressively.

    Args:
        years:  list of np.ndarray (years[0] = real word, rest = guesses)
        values: list of np.ndarray (values[0] = real word, rest = guesses)
        save_path: optional path (e.g. "output.png") to save the figure
    Returns:
        (fig, ax) for further customization if needed.
    """
    if len(years) == 0 or len(values) == 0 or len(years) != len(values):
        raise ValueError("years and values must be non-empty lists of equal length.")

    # --- Figure setup ---
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    # Clean grid & axis styling (Google Trends–style)
    # ax.grid(True, color="#E0E0E0", linewidth=1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["bottom"].set_color("#888888")
    # ax.grid(True, color="#444444", alpha=0.2, linewidth=0.8)
    ax.grid(False)
    ax.tick_params(colors="#aaaaaa", labelsize=10)
    ax.set_ylim(bottom=0, top=1.1)

    # --- Real word (first entry) ---
    real_x = np.asarray(years[0], dtype=float)
    real_y = np.asarray(values[0], dtype=float)
    mask = np.isfinite(real_x) & np.isfinite(real_y)
    ax.plot(
        real_x[mask],
        real_y[mask],
        linewidth=3.5,
        color="#000000",  # Google blue
        alpha=1.0,
        label="Real Word",
        zorder=10
    )

    # --- Guesses (rest of the list) ---

    guess_colors = [
        "#FF4C4C",  # bright coral red
        "#FFA500",  # amber orange
        "#827B1F",  # bright yellow
        "#00C853",  # vivid green
        "#00B8D9",  # cyan / teal
        "#2979FF",  # clear electric blue
        "#AA00FF",  # vibrant violet
    ][::-1]

    n_guesses = len(years) - 1
    if n_guesses > 0:
        cmap = plt.get_cmap("plasma")
        for i in range(n_guesses):
            x_i = np.asarray(years[i + 1], dtype=float)
            y_i = np.asarray(values[i + 1], dtype=float)
            mask = np.isfinite(x_i) & np.isfinite(y_i)
            x_i, y_i = x_i[mask], y_i[mask]

            # Fade older guesses
            color = cmap(i / max(1, n_guesses - 1))
            alpha = 0.3 + 0.7 * ((i+1) / n_guesses)
            ax.plot(
                x_i,
                y_i,
                linewidth=2,
                color=guess_colors[i],
                alpha=alpha,
                label=words[i + 1],
                zorder = 5- i,
            )

    # --- Labels & Title ---
    # ax.set_xlabel("Year", fontsize=12, color="#cccccc")
    ax.set_ylabel("", fontsize=12)  # hide label text
    ax.tick_params(axis='y', which='both', left=False, labelleft=False)  # hide y ticks
    # ax.set_title("Word Frequency Over Time", fontsize=16, weight="bold", color="#333333")
    ax.legend(
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(1.02, 1),  # moves legend outside the right edge
        borderaxespad=0,
    )

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight", transparent=True)
        plt.close(fig)
    if show:
        plt.show()

def graph_of_words(words, years=[], values=[], save_path=None, show=False):

    for word in words:
        yy, vv = getWord(word)
        years.append(yy)
        values.append(vv)
    drawGraph(years, values, words, save_path, show)
    return years, values

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

    graph_of_words(["the", "war"], save_path=IMG_SAVE_PATH, show=True)
    # print(classify(list(years), list(values)))