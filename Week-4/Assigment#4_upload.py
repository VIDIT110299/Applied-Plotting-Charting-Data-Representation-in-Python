
# coding: utf-8

# In[67]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

get_ipython().magic(u'matplotlib notebook')
plt.style.use('seaborn-notebook')


# In[205]:

LA_att = pd.read_csv('C:\Users\RWang3\Documents\GitHub\Applied-Plotting-Charting-Data-Representation-in-Python\Week-4\LA Att.csv',delimiter=",",thousands=',')
LA_win = pd.read_csv('C:\Users\RWang3\Documents\GitHub\Applied-Plotting-Charting-Data-Representation-in-Python\Week-4\LA Stats.csv',delimiter=",",thousands=',')
LA_Data = pd.merge(LA_win, LA_att, on=['Seasons', 'Team'], how='left')
LA_Data = LA_Data.rename(columns={'W/L%': 'Win_ratio', 'Serises Win Ratio': 'Serises_Win_Ratio'})
LA_Data.head()


# In[206]:


LA_ravial_Att=LA_Data[['Seasons','Team','Serises_Win_Ratio','Avg']]
LA_ravial_Att.set_index('Seasons',inplace=True)
LA_ravial_Att.index.name = None
LAL = LA_ravial_Att[LA_ravial_Att['Team'] =='LAL']
LAC=LA_ravial_Att[LA_ravial_Att['Team'] =='LAC']

LA_Win_Att=LA_Data[['Seasons','Team','Win_ratio','Avg']]
LA_Win_Att.set_index('Seasons',inplace=True)
LA_Win_Att.index.name = None
LAL_win = LA_Win_Att[LA_Win_Att['Team'] =='LAL']
LAC_win=LA_Win_Att[LA_Win_Att['Team'] =='LAC']

Score_att = LA_Data[['Seasons','Team','ORtg','Avg']]
Score_att.set_index('Seasons',inplace=True)
Score_att.index.name = None
LAL_att = Score_att[Score_att['Team'] =='LAL']
LAC_att = Score_att[Score_att['Team'] =='LAC']


# In[207]:

fig, axes = plt.subplots(nrows=2, ncols=3,figsize=(30, 10))

LAL.Serises_Win_Ratio.plot(ax=axes[0,0],legend=True);
axes[0,0].set_ylabel('Rivalry Game Win Ratio')
axes[0,0].set_title('Lakers Rivalry Game Win Ratio Vs Avg Attendance')
LAL.Avg.plot(secondary_y=True, style='r',ax=axes[0,0],legend=True)
LAC.Serises_Win_Ratio.plot(ax=axes[1,0],legend=True);
axes[1,0].set_ylabel('Rivalry Game Win Ratio')
axes[1,0].set_title('Clippers Rivalry Game Ratio Vs Avg Attendance')
LAC.Avg.plot(secondary_y=True, style='r',ax=axes[1,0],legend=True)


LAL_att.ORtg.plot(ax=axes[0,2],legend=True); 
axes[0,2].set_ylabel('Season Avg Score')
axes[0,2].set_title('Lakers Season Avg Score Vs Avg Attendance')
LAL_att.Avg.plot(secondary_y=True, style='r',ax=axes[0,2],legend=True)
LAC_att.ORtg.plot(ax=axes[1,2],legend=True); 
axes[1,2].set_ylabel('Season Avg Score')
axes[1,2].set_title('Clippers Season Avg Score Vs Avg Attendance')
LAC_att.Avg.plot(secondary_y=True, style='r',ax=axes[1,2],legend=True)

LAL_win.Win_ratio.plot(ax=axes[0,1],legend=True); 
axes[0,1].set_ylabel('Season Win Ratio')
axes[0,1].set_title('Lakers Season Win Ratio Vs Avg Attendance')
LAL_win.Avg.plot(secondary_y=True, style='r',ax=axes[0,1],legend=True)
LAC_win.Win_ratio.plot(ax=axes[1,1],legend=True); 
axes[1,1].set_ylabel('Season Win Ratio')
axes[1,1].set_title('Clippers Season Win Ratio Vs Avg Attendance')
LAC_win.Avg.plot(secondary_y=True, style='r',ax=axes[1,1],legend=True)


# In[ ]:



