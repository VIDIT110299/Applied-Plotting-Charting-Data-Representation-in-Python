
# coding: utf-8

# # Assignment 3 - Building a Custom Visualization
# 
# ---
# 
# In this assignment you must choose one of the options presented below and submit a visual as well as your source code for peer grading. The details of how you solve the assignment are up to you, although your assignment must use matplotlib so that your peers can evaluate your work. The options differ in challenge level, but there are no grades associated with the challenge level you chose. However, your peers will be asked to ensure you at least met a minimum quality for a given technique in order to pass. Implement the technique fully (or exceed it!) and you should be able to earn full grades for the assignment.
# 
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ferreira, N., Fisher, D., & Konig, A. C. (2014, April). [Sample-oriented task-driven visualizations: allowing users to make better, more confident decisions.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 571-580). ACM. ([video](https://www.youtube.com/watch?v=BI7GAs-va-Q))
# 
# 
# In this [paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) the authors describe the challenges users face when trying to make judgements about probabilistic data generated through samples. As an example, they look at a bar chart of four years of data (replicated below in Figure 1). Each year has a y-axis value, which is derived from a sample of a larger dataset. For instance, the first value might be the number votes in a given district or riding for 1992, with the average being around 33,000. On top of this is plotted the confidence interval -- the range of the number of votes which encapsulates 95% of the data (see the boxplot lectures for more information, and the yerr parameter of barcharts).
# 
# <br>
# <img src="readonly/Assignment3Fig1.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 1 from (Ferreira et al, 2014).</h4>
# 
# <br>
# 
# A challenge that users face is that, for a given y-axis value (e.g. 42,000), it is difficult to know which x-axis values are most likely to be representative, because the confidence levels overlap and their distributions are different (the lengths of the confidence interval bars are unequal). One of the solutions the authors propose for this problem (Figure 2c) is to allow users to indicate the y-axis value of interest (e.g. 42,000) and then draw a horizontal line and color bars based on this value. So bars might be colored red if they are definitely above this value (given the confidence interval), blue if they are definitely below this value, or white if they contain this value.
# 
# 
# <br>
# <img src="readonly/Assignment3Fig2c.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  Figure 2c from (Ferreira et al. 2014). Note that the colorbar legend at the bottom as well as the arrows are not required in the assignment descriptions below.</h4>
# 
# <br>
# <br>
# 
# **Easiest option:** Implement the bar coloring as described above - a color scale with only three colors, (e.g. blue, white, and red). Assume the user provides the y axis value of interest as a parameter or variable.
# 
# 
# **Harder option:** Implement the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).
# 
# **Even Harder option:** Add interactivity to the above, which allows the user to click on the y axis to set the value of interest. The bar colors should change with respect to what value the user has selected.
# 
# **Hardest option:** Allow the user to interactively set a range of y values they are interested in, and recolor based on this (e.g. a y-axis band, see the paper for more details).
# 
# ---

# In[26]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem
import matplotlib.colors as mcol
import matplotlib.cm as cm

get_ipython().magic('matplotlib notebook')


np.random.seed(12345)

df = pd.DataFrame([np.random.normal(33500,150000,3650), 
                   np.random.normal(41000,90000,3650), 
                   np.random.normal(41000,120000,3650), 
                   np.random.normal(48000,55000,3650)], 
                  index=[1992,1993,1994,1995])

n = np.arange(len(df.index))
dMeans = df.mean(axis=1)
threshold = sum(dMeans)/4    # user-provided threshold value
yerr = df.sem(axis=1).values * 1.96  #standard error of means

cm1 = mcol.LinearSegmentedColormap.from_list("c",["white","slateblue"]) #define a color map

cnorm = mcol.Normalize(vmin=0,vmax=100) # Make a normalizer that will map the data values

cpick = cm.ScalarMappable(norm=cnorm,cmap=cm1) #create a color picker
cpick.set_array([])

clrIx = (((dMeans + yerr) - threshold) / (yerr *2)) * 100

for idx, c in enumerate(clrIx):
    if c >= 100:
        clrIx[idx] = 100
    elif c <= 0:
        clrIx[idx] = 0
    else:
        clrIx[idx] = int(c)
    
fig, ax = plt.subplots()
for x in n:
    if clrIx[x] == 100:
        ax.bar(x, df.mean(axis=1).iloc[x], yerr=yerr[x], capsize=10, width=0.99, color='darkred')
    elif clrIx[x] == 0:
        ax.bar(x, df.mean(axis=1).iloc[x], yerr=yerr[x], capsize=10, width=0.99, color='darkblue')
    else:    
        ax.bar(x, df.mean(axis=1).iloc[x], yerr=yerr[x], capsize=10, width=0.99, color=cpick.to_rgba(clrIx[x]))
    
lines = ax.plot([-0.5, 5.0], [threshold, threshold], 'k--')
plt.setp(lines, color='y', linewidth=2.0)
ax.set_xticks(n)
ax.set_xticklabels(df.index.values)


# In[ ]:



