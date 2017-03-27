
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

# In[2]:

# Use the following data for this assignment:

import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(33500,150000,3650), 
                   np.random.normal(41000,90000,3650), 
                   np.random.normal(41000,120000,3650), 
                   np.random.normal(48000,55000,3650)], 
                  index=[1992,1993,1994,1995])
df

#---------------------------------------------------------------------

# imports
from scipy.stats import t
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
#import matplotlib.colorbar
from matplotlib.colorbar import Colorbar
from matplotlib.colorbar import ColorbarBase
get_ipython().magic('matplotlib notebook')


#---------------------------------------------------------------------

# get data from provided DataFrame into individual Series
s92 = df[df.index==1992].squeeze()
s93 = df[df.index==1993].squeeze()
s94 = df[df.index==1994].squeeze()
s95 = df[df.index==1995].squeeze()

# Add the data series into a list for easier iteration below
sYears = [s92, s93, s94, s95]

# Initialize some empty lists for calculated values
m = []  #sample means
n = []  #number of observations in each sample
s = []  #sample standard deviations 
ci = []  # confidence intervals on means

# Calculate summary statistics and 95% confidence intervals for each data series
for i in range(0,len(sYears)):
    m.append(np.mean(sYears[i]))
    n.append(len(sYears[i])-1)
    s.append(sYears[i].std())
    ci.append(t.ppf(0.95, n[i]-1)*s[i]/n[i]**(1/2))



#---------------------------------------------------------------------

# Method/Function declarations

def getEbarYVals(i):
    # return a tuple containing the Y end points for the error bars on the ith bar in bar plot
    ymin0 = ebars[0].get_segments()[i][0][1]
    ymax0 = ebars[0].get_segments()[i][1][1]
    return (ymin0,ymax0)
          
    
def calcP(testLow,testHigh,ebar):
    # calculate a factor for comparison of reference range to CI on mean
    # this is not based on probability, but some crazy comparison scheme that I came up with.
    # P factor ranges from 0 to 1
    # 0 or less indicates the mean is well below the reference range (should present in blue color)
    # 1 or greater indicates the mean is well above the reference range (should present in red color)
    
    if ebar[0] < testLow and ebar[1] > testHigh:
        # test range is completely within mean CI.  p values for neutral (white) colors, at 0.5
        p = 0.5
    
    elif ebar[0] > testHigh:
        #test range is very low in comparison, produce higher p values around 1 for red colors
        p = 0.5 + (ebar[0] - testHigh) / (ebar[1]-ebar[0]) * 0.15
        
    elif ebar[1] < testLow:
        #test range is very high in comparison, produce lower p values around 0 for blue colors
        p = 0.5 - (testLow - ebar[1]) / (ebar[1]-ebar[0]) * 0.15
        
    elif testHigh > ebar[1] and ebar[1] > testLow > ebar[0]:
        #partial overlap but test range is a bit higher - produce lower p values
        # overlap < 1
        p = 0.5 - (ebar[1] - testLow) / (ebar[1]-ebar[0]) * 0.15
        
    elif testLow < ebar[0] and ebar[1] < testHigh < ebar[0]:
        #partial overlap but test range is a bit lower - produce higher p values
        # overlap < 1
        p = 0.5 + (testHigh - ebar[0]) / (ebar[1]-ebar[0]) * 0.15
    
    return p
    
    
    
def setShadedBox(ymin,ymax,xmin,xmax):
    # adjust the shaded rectangle to the user-selected reference range
    cXY = hbox.get_xy()
    cXY[0][0] = xmin
    cXY[0][1] = ymin
    
    cXY[1][0] = xmin
    cXY[1][1] = ymax
    
    cXY[2][0] = xmax
    cXY[2][1] = ymax
    
    cXY[3][0] = xmax
    cXY[3][1] = ymin
    
    cXY[4][0] = xmin
    cXY[4][1] = ymin
    
    hbox.set_xy(cXY)
    
    
    
def rangeSelected(ymin,ymax):
    # event handler for when user selects a reference range using SpanSelector widget
    setShadedBox(ymin,ymax,0,5)
    for i in range(0,len(ax.patches)):
        ebar = getEbarYVals(i)
        p = calcP(ymin,ymax,ebar)
        ax.patches[i].set_facecolor(cm(p)) 
    


# In[3]:


# create new figure and primary axes
fig = plt.figure()
ax = plt.axes()

# create a bar plot with data
bars = ax.bar(left=[1,2,3,4], height=m, tick_label=['1992','1993','1994','1995'])
# create a line plot with error bars, since this seemed to provide the easiest way to customize/work with error bars.
# the line is hidden so that only error bars show. 
(eline,ecaps,ebars) = ax.errorbar(x = [1,2,3,4], y = m, yerr = ci, ecolor = 'black',linestyle='None',capsize=3,capthick=1)

# some formatting
ax.set_axis_bgcolor('lightgrey')
ebars[0].set_linewidth(1)

# add the primary axis to the figure
fig.add_axes(ax)

# create color map to be used for coloring bars based on comparison against reference range
cm = plt.cm.get_cmap('coolwarm')

# create a widget for user to select reference range that they want to test against
span = SpanSelector(ax, rangeSelected, 'vertical', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))

# create a horizontal box that will mark the reference region selected by user
hbox = ax.axhspan(ymin=0,ymax=0,xmin=0,xmax=5,color='black',alpha=0.2)

# a color bar will be used as a legend for the color map

# create an axes to contain the ColorBar, with appropriate position and size
cBarAx = fig.add_axes([0.90, 0.2, 0.025, 0.6])    # rect [left, bottom, width, height] 

# create the color bar, passing its parent axes and the color map
cb = ColorbarBase(ax=cBarAx, cmap=cm, orientation='vertical')

# reposition original bar plot axes to allow for better fit of color bar legend next to it
ax.set_position(
    [ax.get_position().bounds[0],ax.get_position().bounds[1],ax.get_position().bounds[2]*0.98,ax.get_position().bounds[3]]
)

# use title to provide some breif instruction.
ax.set_title('Select a Y range with mouse left click and drag.' + '\n' + 
             'Bar colors will reflect comparison of sample mean to selected range.', size=10)


# In[ ]:



