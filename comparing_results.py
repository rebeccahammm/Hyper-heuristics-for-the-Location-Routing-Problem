#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:36:14 2022

@author: hammr
"""
import pandas as pd
import scipy.stats as stats
import numpy as np
import json
import statistics as st
srr=pd.read_pickle("SR_R.p")
adr=pd.read_pickle("A_R.p")
sr=pd.read_pickle("S_R.p")
adshr=pd.read_pickle("ADSH_R.p")
srg=pd.read_pickle("SR_G.p")
adg=pd.read_pickle("A_G.p")
sg=pd.read_pickle("S_G.p")
adshg=pd.read_pickle("ADSH_G.p")
def comparasion(methods=[srr,adr,sr,adshr,srg,adg,sg,adshg]):
    results={}
    info={}
    for meth in range(len(methods)):
        for inst in range(len(methods[0])):
            for k in range(5):
                info[(meth,inst,k)]={"mean":0,"std":0,"min":0,"infeasible":0}
    for meth in range(len(methods)):
        for k in range(5):
            realvalues=[]
            info[(meth,inst,k)]["min"]=methods[meth][inst][k]["min"]
            for i in methods[meth][inst][k]["obj"]:
                if i>100000:
                #    print(i,"removed")
                    info[(meth,inst,k)]["infeasible"]+=1
                    #methods[meth][4][k]["obj"].remove(i)
                else:
                    realvalues.append(i)
                    print(i,"stayed")
            print(realvalues)
            #methods[meth][4][k]["obj"]=realvalues
            info[(meth,inst,k)]["mean"]=st.mean(realvalues)
            info[(meth,inst,k)]["std"]=st.stdev(realvalues)
                    
            
    for meth in range(len(methods)):
        for inst in range(len(methods[0])):
            for k in range(5):
                results[(meth,inst,k)]={"sigbetter":0,"better":0,"equal":0,"worse":0,"sigworse":0}
    for m1 in range(len(methods)):
        for m2 in range(m1,len(methods)): 
            if m1==m2:        
                #print(m1,m2)
                for inst in range(len(methods[0])):
                    srinst0=methods[m1][inst]
                    for k in range(5):
                        for l in range(k+1,5):
                            sig=""
                            list1=srinst0[k]["obj"]
                            list2=srinst0[l]["obj"]
                            if min(srinst0[k]["std"],srinst0[l]["std"])==0:
                                if stats.ttest_ind(list1,list2,equal_var=False)[1]<0.05:
                                    sig="sig"
                            elif max(srinst0[k]["std"],srinst0[l]["std"])/min(srinst0[k]["std"],srinst0[l]["std"])<4:
                                if stats.ttest_ind(list1,list2,equal_var=True)[1]<0.05:
                                    sig="sig"
                            else: 
                                if stats.ttest_ind(list1,list2,equal_var=False)[1]<0.05:
                                    sig="sig"
                            list1score=0
                            list2score=0
                            for i in list1:
                                for j in list2:
                                    if i<j:
                                        list1score+=1
                                    if j<i:
                                        list2score+=1
                            if list1score>list2score:
                                results[(m1,inst,k)][sig+"better"]+=1
                                results[(m1,inst,l)][sig+"worse"]+=1
                            elif list2score>list1score:
                                results[(m1,inst,l)][sig+"better"]+=1
                                results[(m1,inst,k)][sig+"worse"]+=1
                            else:
                                results[(m1,inst,k)]["equal"]+=1
                                results[(m1,inst,l)]["equal"]+=1
            else:
                for inst in range(len(methods[0])):
                    srinst0=methods[m1][inst]
                    srinst1=methods[m2][inst]
                    for k in range(5):
                        for l in range(5):
                            #print(k,l)
                            sig=""
                            list1=srinst0[k]["obj"]
                            list2=srinst1[l]["obj"]
                            if min(srinst0[k]["std"],srinst0[l]["std"])==0:
                                if stats.ttest_ind(list1,list2,equal_var=False)[1]<0.05:
                                    sig="sig"
                            elif max(srinst0[k]["std"],srinst0[l]["std"])/min(srinst0[k]["std"],srinst0[l]["std"])<4:
                                if stats.ttest_ind(list1,list2,equal_var=True)[1]<0.05:
                                    sig="sig"
                            else: 
                                if stats.ttest_ind(list1,list2,equal_var=False)[1]<0.05:
                                    sig="sig"
                            list1score=0
                            list2score=0
                            for i in list1:
                                for j in list2:
                                    if i<j:
                                        list1score+=1
                                    if j<i:
                                        list2score+=1
                            if list1score>list2score:
                                results[(m1,inst,k)][sig+"better"]+=1
                                results[(m2,inst,l)][sig+"worse"]+=1
                            elif list2score>list1score:
                                results[(m2,inst,l)][sig+"better"]+=1
                                results[(m1,inst,k)][sig+"worse"]+=1
                            else:
                                results[(m1,inst,k)]["equal"]+=1
                                results[(m2,inst,l)]["equal"]+=1
    return info,results