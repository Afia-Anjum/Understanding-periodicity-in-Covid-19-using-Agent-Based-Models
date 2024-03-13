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
    
    

p=0
h=[]
for j in range(len(list_collect[0])):
    p=0
    for i in range(len(list_collect)):
        p=p+list_collect[0][j]
    #p=p/100   #avg, and summing with this line in comment
    h.append(p)
    
plt.plot(h,'r-')       

    
    
    
    
    
    
