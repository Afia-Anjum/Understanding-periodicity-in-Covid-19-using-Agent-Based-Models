# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 01:51:05 2020

@author: Asus
"""

from model import Schelling
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def smoothTriangle(data, degree):
    triangle=np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1])) # up then down
    smoothed=[]

    for i in range(degree, len(data) - degree * 2):
        point=data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point)/np.sum(triangle))
    # Handle boundaries
    smoothed=[smoothed[0]]*int(degree + degree/2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed

agent_type_pcs=[.99, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0]
agent_age_type_pcs=[0.05,0.4,0.05,0.5]
agent_disease_type_pcs=[0.25,0.07,0.22,0.24,0.08,0.14]
social_distancing=True

#True: there is a barrier
#False: there is a hole in the barrier


infected_list=[]
list_collect=[]
#empty_model = Schelling(40,40,0.1,0.06,0.075,agent_type_pcs,agent_age_type_pcs,agent_disease_type_pcs,social_distancing)
for j in range(100):  #10 different runs/100 different runs
    #j%100
    
    empty_model = Schelling(100,100,0.1,0.01,0.075,agent_type_pcs,agent_age_type_pcs,agent_disease_type_pcs,social_distancing)
    #empty_model = Schelling(40,40,0.1,0.06,0.075,agent_type_pcs,agent_age_type_pcs,agent_disease_type_pcs,social_distancing)
    #while empty_model.running:
    #for i in range(100):
    for i in range(50):  #150~=5 months
        empty_model.step()
        gini = empty_model.datacollector.get_model_vars_dataframe()
    df=gini['newly_infected']
    #print(df)
    gini_list=df.values.tolist()
    for k in range(len(gini_list)):
        infected_list.append(gini_list[k])
    list_collect.append(gini_list)
    
    
    #total number of agents after the agrregation from 10 runs: 10,000
    
    
    #print(infected_list)
#gini.plot()
    
#print(list_collect)

#smooth_data = pd.Series(infected_list).rolling(window=7).mean().plot(style='k')
#plt.show()

#h=[(list_collect[0][j] + list_collect[1][j]+list_collect[2][j] +list_collect[3][j] +list_collect[4][j] +list_collect[5][j] +list_collect[6][j] +list_collect[7][j] +list_collect[8][j] +list_collect[9][j])/10 for j in range(len(list_collect[0]))]
#plt.plot(h,'r-')

p=0
h=[]
for j in range(len(list_collect[0])):
    p=0
    for i in range(len(list_collect)):
        p=p+list_collect[0][j]
    #p=p/100   #avg, and summing with this line in comment
    h.append(p)
    
plt.plot(h,'r-')       

'''

s=pd.Dataframe(list_collect)
df = pd.DataFrame(list_collect)
df.to_csv('reporting_artifacts_100runs_5thJune.csv',index=False)

'''

'''
plt.plot(list_collect[0],'b-')
plt.plot(list_collect[1],'b-')
plt.plot(list_collect[2],'b-')
plt.plot(list_collect[3],'b-')
plt.plot(list_collect[4],'b-')
plt.plot(list_collect[5],'b-')
plt.plot(list_collect[6],'b-')
plt.plot(list_collect[7],'b-')
plt.plot(list_collect[8],'b-')
plt.plot(list_collect[9],'b-')
plt.plot(h,'r-')
plt.show()
'''

'''
import matplotlib.pyplot as plt
import scipy.signal as signal
ts = infected_list[0:]
#Moving average, basically acts as the low pass filter:
N  = 3    # Filter order
Wn = 0.1 # Cutoff frequency
B, A = signal.butter(N, Wn, output='ba')
smooth_data = signal.filtfilt(B,A, infected_list[0:])
plt.plot(ts,'r-')
#plt.plot(smooth_data[0:],'b-')
plt.show()
    
'''
    
    
    
    
    
    