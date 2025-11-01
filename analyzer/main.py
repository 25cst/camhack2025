import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import scipy
testDict = {}
years = 120
for i in range(years):
    var = (i-60)
    testDict[i+1900]= 1.02**(-(var*var)/5) 


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
    

# 0.9486 --> 2
# 0.613

x = np.array(list(testDict.keys()))
y = np.array(list(testDict.values()))


f_cubic = scipy.interpolate.interp1d(x, y, kind='cubic')  # smoother curve
Y = f_cubic(x)


print(classify(testDict, years))
plt.plot(x, Y, color='blue', label='Cubic interpolation')
plt.show()

