
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[108]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
get_ipython().magic('matplotlib notebook')
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import MONDAY
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
plt.rcParams['figure.figsize'] = (20.0, 10.0)

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df = df.sort_values('Date')

df['Year'] = df['Date'].str[:4]
df['Day'] = df['Date'].str[5:]
df = df[df['Day']!='02-29']
df_05_14=df[df['Year']!='2015']
df_2015 = df[df['Year']=='2015']

df_05_14['Newdate'] = pd.to_datetime(df_05_14.Day, format="%m-%d", )
df_05_14['date'] = df_05_14['Newdate'].apply(lambda x: x.strftime('%B-%d'))

df_2015['Newdate'] = pd.to_datetime(df_2015.Day, format="%m-%d", )
df_2015['date'] = df_2015['Newdate'].apply(lambda x: x.strftime('%B-%d'))

max_05_14 = df_05_14.groupby(['date'], sort=False)['Data_Value'].max()
min_05_14 = df_05_14.groupby(['date'], sort=False)['Data_Value'].min()

max_15 = df_2015.groupby(['date'], sort=False)['Data_Value'].max()
min_15 = df_2015.groupby(['date'], sort=False)['Data_Value'].min()

max_15_1 = max_15.where(max_15>max_05_14)
max_15_final = max_15_1
min_15_1 = min_15.where(min_15<min_05_14)
min_15_final = min_15_1

max0514 = (max_05_14/10).tolist()
min0514 = (min_05_14/10).tolist()
max15 = (max_15_final/10).tolist()
min15 = (min_15_final/10).tolist()


obseration_date  = np.arange('2015-01-01','2016-01-01',dtype='datetime64[D]')
obseration_date = list(map(pd.to_datetime,obseration_date))


# In[111]:

fig, ax = plt.subplots()
ax.plot_date(obseration_date, max0514, 'r-')
ax.plot_date(obseration_date, min0514, 'b-')
ax.plot(obseration_date, max15, 'gs')
ax.plot(obseration_date, min15, 'kD')

ax.fill_between(obseration_date, max0514, min0514,
                facecolor='yellow', alpha=1, interpolate=True)
months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
monthsFmt = DateFormatter("%b")
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.autoscale_view()
ax.set_xlim(['2015-01-01', '2015-12-31'])
ax.set_ylim(-40,50)
ax.set_xlabel('Date Month')
ax.set_ylabel('Temperature Degree C')
ax.set_title('05-14 High&Low Temp and 15 Record Breaking Temp')


ax2 = ax.twinx()
ax2.set_ylabel('Temperature Degree F')
ax2.set_ylim(-35,122)

ax.legend(['High Tem','Low Tem','2015 Hihg Tem Record Breaking','2015 Low Tem Record Breaking', 'Tem Diff'])


# In[105]:




# In[ ]:



