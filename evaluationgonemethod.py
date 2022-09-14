#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:56:04 2022

@author: hammr
"""
import pandas as pd
import pickle
import solution_class
import matplotlib.pyplot as plt
import numpy as np
import statistics as st

def combining_results():
    ins0method1=pd.read_pickle("Anaylis_of_random_ADSHRR_ins_0.p")
    ins0method2=pd.read_pickle("Anaylis_of_greedy_SHRR_ins_0.p")
    ins1method1=pd.read_pickle("Anaylis_of_random_ADSHRR_ins_1.p")
    ins1method2=pd.read_pickle("Anaylis_of_greedy_SHRR_ins_1.p")
    ins2method1=pd.read_pickle("Anaylis_of_random_ADSHRR_ins_2.p")
    ins2method2=pd.read_pickle("Anaylis_of_greedy_SHRR_ins_2.p")
    ins3method1=pd.read_pickle("Anaylis_of_random_ADSHRR_ins_3.p")
    ins3method2=pd.read_pickle("Anaylis_of_greedy_SHRR_ins_3.p")
    ins4method1=pd.read_pickle("Anaylis_of_random_ADSHRR_ins_4.p")
    ins4method2=pd.read_pickle("Anaylis_of_greedy_SHRR_ins_4.p")
    ins0method1=ins0method1[0]
    ins0method2=ins0method2[0]
    ins1method1=ins1method1[1]
    ins1method2=ins1method2[1]
    ins2method1=ins2method1[2]
    ins2method2=ins2method2[2]
    ins3method1=ins3method1[3]
    ins3method2=ins3method2[3]
    ins4method1=ins4method1[4]
    ins4method2=ins4method2[4]
    return ins0method1,ins2method1,ins3method1,ins4method1,ins0method2,ins2method2,ins3method2,ins4method2
#convert LLH numbers to as in paper
def converting_llh(results):
    newresult=[]
    for i in range(len(results)):
        newresultone=[]
        for j in results[i]["llh"]:
            llh=[]
            for k in j:
                if k==0:
                    llh.append("LLH1")
                if k==1:
                    llh.append("LLH3")
                if k==2:
                    llh.append("LLH7")
                if k==3:
                    llh.append("LLH9")
                if k==4:
                    llh.append("LLH11")
                if k==5:
                    llh.append("LLH13")
                if k==6:
                    llh.append("LLH8")
                if k==7:
                    llh.append("LLH4")
                if k==8:
                    llh.append("LLH10")
                if k==9:
                    llh.append("LLH12")
                if k==10:
                    llh.append("LLH5")
                if k==11:
                    llh.append("LLH6")
                if k==12:
                    llh.append("LLH14")
                if k==13:
                    llh.append("LLH15")
                if k==14:
                    llh.append("LLH2")
            newresultone.append(llh)
        newresult.append(newresultone)
    return newresult
          
#Plot path of objective value and close up of the start
def graph(results,ins):
    pathlength=min([len(results[i]["path"]) for i in range(10)])
    path=[st.mean([results[i]["path"][j]   for i in range(10)]) for j in range(pathlength)]
    fig=plt.figure()
    axes1=fig.add_axes([0.1,0.1,0.8,0.8])
    axes2=fig.add_axes([0.3,0.3,0.6,0.4])
    axes1.plot(range(pathlength),path)
    axes1.set_xlabel("Iteration")
    axes1.set_ylabel("Objective Value")
    axes1.set_title("Instance "+str(ins))
    axes2.plot(range(int(0.005*pathlength)),path[:int(0.005*pathlength)])
    axes2.set_xlabel("Iteration")
    axes2.set_ylabel("Objective Value")
    axes2.set_title("Objective Value for first iter")
    
#plots objective value and infeasibility
def obj_infe_graph(method1,start,pathlength):
    method1infeasible=[st.mean([method1[i]["path"][j]   for i in range(10)]) for j in range(pathlength)]
    method2infeasible=[st.mean([method1[i]["infeasible"][j] for i in range(10)]) for j in range(pathlength)]
    fig,axes=plt.subplots(2,1,figsize=(10,8))
    axes[0].plot(range(start,pathlength),method1infeasible[start:pathlength],label="Adaptive seq")
    axes[0].set_title("Instance 2 Objective Value")
    axes[1].plot(range(start,pathlength),method2infeasible[start:pathlength],label="Adaptive seq")
    axes[1].set_title("Instance 2 infeasbility");

# charts sequence and indiviual all seperate
def llh_each_choice(results,method,ins):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
        method_title="Adaptive Seq"
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]
        method_title=" Seq"
    lcount={}
    for i in l:
        i=str(tuple(i))
        if i in lcount:
            lcount[i]+=1
        else:
            lcount[i]=1
    count=0
    for i in lcount:
        count+=lcount[i]     
    percentage=[]
    for i in lcount:
        percentage.append(lcount[i]/count)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["LLH"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, 1), loc='upper right',ncol=8)
    ax.set_title("Instance "+ str(ins)+" "+ method_title)
    
# charts sequence clumbed
def llh_sequence_combined(results,method,ins):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
        method_title="Adaptive Seq"
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]
        method_title=" Seq"
    lcount={"sequence":0,"(0,)":0,"(1,)":0,"(2,)":0,"(3,)":0,"(4,)":0,"(5,)":0,"(6,)":0,"(7,)":0,"(8,)":0,"(9,)":0,"(10,)":0,"(11,)":0,"(12,)":0,"(13,)":0,"(14,)":0}
    for i in l:
        if len(i)>1:
            lcount["sequence"]+=1
        else:
            i=str(tuple(i))
            if i in lcount:
                lcount[i]+=1
            else:
                lcount[i]=1
    count=0
    for i in lcount:
        count+=lcount[i]     
    percentage=[]
    for i in lcount:
        percentage.append(lcount[i]/count)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["LLH"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, 1), loc='upper right',ncol=8)
    ax.set_title("Instance "+ str(ins)+" "+ method_title)
    
#sequence all instanatnces at once
def llh_sequence_combined_multi_ins(results,method):
    newresults=[]
    for i in range(len(results)):
        newresults.append(converting_llh(results[i]))
    results=newresults
    lcount={"sequence":{0:0,1:0,2:0,3:0,4:0},"LLH1":{0:0,1:0,2:0,3:0,4:0},"LLH2":{0:0,1:0,2:0,3:0,4:0},"LLH3":{0:0,1:0,2:0,3:0,4:0},"LLH4":{0:0,1:0,2:0,3:0,4:0},"LLH5":{0:0,1:0,2:0,3:0,4:0},"LLH6":{0:0,1:0,2:0,3:0,4:0},"LLH7":{0:0,1:0,2:0,3:0,4:0},"LLH8":{0:0,1:0,2:0,3:0,4:0},"LLH9":{0:0,1:0,2:0,3:0,4:0},"LLH10":{0:0,1:0,2:0,3:0,4:0},"LLH11":{0:0,1:0,2:0,3:0,4:0},"LLH12":{0:0,1:0,2:0,3:0,4:0},"LLH13":{0:0,1:0,2:0,3:0,4:0},"LLH14":{0:0,1:0,2:0,3:0,4:0},"LLH15":{0:0,1:0,2:0,3:0,4:0}}
    for ins in range(len(results)):
        if method==1:
            l=[]
            for i in range(10):
                l=l+results[ins][i][15:]
            method_title="Adaptive Seq"
        if method==2:
            l=[]
            for i in range(10):
                l=l+results[ins][i]
            method_title=" Seq"
        
        for i in l:
            if len(i)>1:
                lcount["sequence"][ins]+=1
            else:
                i=i[0]
                if i in lcount:
                    lcount[i][ins]+=1
                else:
                    print(i,ins)
                    lcount[i][ins]=1
    count=[]
    for ins in range(len(results)):
        countins=0
        for i in lcount:
            countins+=lcount[i][ins]
        count.append(countins)
    percentage=[]
    for i in lcount:
        lcountp=[]
        for ins in range(len(results)):
            lcountp.append(lcount[i][ins]/count[ins])
        percentage.append(lcountp)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["Ins 1","Ins 2","Ins 3","Ins 4","Ins 5"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, -0.15), loc='upper right',ncol=8)
    ax.set_title(method_title)    
    
#each indidual llh
def llh_each_individual(results,method,ins):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
        method_title="Adaptive Seq"
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]
        method_title=" Seq"
    lcount={"sequence":0,0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
    for i in l:
        for j in i:
            lcount[j]+=1
    print(lcount)
    count=0
    for i in lcount:
        count+=lcount[i]     
    percentage=[]
    for i in lcount:
        percentage.append(lcount[i]/count)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["LLH"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, 1), loc='upper right',ncol=8)
    ax.set_title("Instance "+ str(ins)+" "+ method_title)
    
#charts sequence and indiviual all seperate Less than percent othered
def llh_each_choice_percent_capped(results,method,ins,percent):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
        method_title="Adaptive Seq"
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]
        method_title=" Seq"
    lcount={}
    for i in l:
        i=str(tuple(i))
        if i in lcount:
            lcount[i]+=1
        else:
            lcount[i]=1
    count=0
    for i in lcount:
        count+=lcount[i]   
    lcount["other"]=0
    x=list(lcount.keys())
    for i in x:
        if lcount[i]/count<percent:
            lcount["other"]+=lcount.pop(i)
    percentage=[]
    for i in lcount:
        percentage.append(lcount[i]/count)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["LLH"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, 1), loc='upper right',ncol=8)
    ax.set_title("Instance "+ str(ins)+" "+ method_title)
    
 #each choice capped multi iins   
def llh_eachchoice_multi_ins(results,method,percent):
    newresults=[]
    for i in range(len(results)):
        newresults.append(converting_llh(results[i]))
    results=newresults
    lcount={"sequence":{0:0,1:0,2:0,3:0,4:0},"LLH1":{0:0,1:0,2:0,3:0,4:0},"LLH2":{0:0,1:0,2:0,3:0,4:0},"LLH3":{0:0,1:0,2:0,3:0,4:0},"LLH4":{0:0,1:0,2:0,3:0,4:0},"LLH5":{0:0,1:0,2:0,3:0,4:0},"LLH6":{0:0,1:0,2:0,3:0,4:0},"LLH7":{0:0,1:0,2:0,3:0,4:0},"LLH8":{0:0,1:0,2:0,3:0,4:0},"LLH9":{0:0,1:0,2:0,3:0,4:0},"LLH10":{0:0,1:0,2:0,3:0,4:0},"LLH11":{0:0,1:0,2:0,3:0,4:0},"LLH12":{0:0,1:0,2:0,3:0,4:0},"LLH13":{0:0,1:0,2:0,3:0,4:0},"LLH14":{0:0,1:0,2:0,3:0,4:0},"LLH15":{0:0,1:0,2:0,3:0,4:0}}
    for ins in range(len(results)):
        #print(ins)
        if method==1:
            l=[]
            for i in range(10):
                l=l+results[ins][i][15:]
            method_title="Adaptive Seq"
        if method==2:
            l=[]
            for i in range(10):
                l=l+results[ins][i]
            method_title=" Seq"
        
        for i in l:
            if len(i)<1:
                lcount[i[0]][ins]+=1
            else:
                i=str(i)
                if i in lcount:
                    lcount[i][ins]+=1
                else:
                    lcount[i]={0:0,1:0,2:0,3:0,4:0}
                    lcount[i][ins]+=1
    count=[]
    for ins in range(len(results)):
        countins=0
        for i in lcount:
            countins+=lcount[i][ins]
        count.append(countins)
    lcount["other"]={0:0,1:0,2:0,3:0,4:0}
    x=list(lcount.keys())
    for i in x:
        for ins in range(len(results)):
            if lcount[i][ins]/count[ins]<percent:
                lcount["other"][ins]+=lcount[i][ins]
                lcount[i][ins]=0
    for i in x:
        c=0
        for ins in range(len(results)):
            if lcount[i][ins]==0:
                c+=1
        if c==5:
            lcount.pop(i) 
    percentage=[]
    for i in lcount:
        lcountp=[]
        for ins in range(len(results)):
            lcountp.append(lcount[i][ins]/count[ins])
        percentage.append(lcountp)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["Ins 1","Ins 2","Ins 3","Ins 4","Ins 5"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.8, -0.15), loc='upper right',ncol=9)
    ax.set_title(method_title)    
    
    
# charts sequence clumbed capped percentage
def llh_sequence_combined_percent_capped(results,method,ins,percent):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
        method_title="Adaptive Seq"
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]
        method_title=" Seq"
    lcount={"sequence":0,"(0,)":0,"(1,)":0,"(2,)":0,"(3,)":0,"(4,)":0,"(5,)":0,"(6,)":0,"(7,)":0,"(8,)":0,"(9,)":0,"(10,)":0,"(11,)":0,"(12,)":0,"(13,)":0,"(14,)":0}
    for i in l:
        if len(i)>1:
            lcount["sequence"]+=1
        else:
            i=str(tuple(i))
            if i in lcount:
                lcount[i]+=1
            else:
                lcount[i]=1
    count=0
    for i in lcount:
        count+=lcount[i]  
    lcount["other"]=0
    x=list(lcount.keys())
    for i in x:
        if lcount[i]/count<percent:
            lcount["other"]+=lcount.pop(i)
            
    percentage=[]
    for i in lcount:
        percentage.append(lcount[i]/count)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["LLH"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, 1), loc='upper right',ncol=8)
    ax.set_title("Instance "+ str(ins)+" "+ method_title)
    
#each indidual llh capped percentage
def llh_each_individual_percent_capped(results,method,ins,percent):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
        method_title="Adaptive Seq"
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]
        method_title=" Seq"
    lcount={"sequence":0,0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
    for i in l:
        if len(i)>1:
            for j in i:
                lcount[j]+=1
    print(lcount)
    count=0
    for i in lcount:
        count+=lcount[i] 
    lcount["other"]=0
    x=list(lcount.keys())
    for i in x:
        if lcount[i]/count<percent:
            lcount["other"]+=lcount.pop(i)
    percentage=[]
    for i in lcount:
        percentage.append(lcount[i]/count)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["LLH"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, 1), loc='upper right',ncol=8)
    ax.set_title("Instance "+ str(ins)+" "+ method_title)
    
#each individual multi ins    
def llh_eachindiv_multi_ins(results,method,percent):
    newresults=[]
    for i in range(len(results)):
        newresults.append(converting_llh(results[i]))
    results=newresults
    lcount={"sequence":{0:0,1:0,2:0,3:0,4:0},"LLH1":{0:0,1:0,2:0,3:0,4:0},"LLH2":{0:0,1:0,2:0,3:0,4:0},"LLH3":{0:0,1:0,2:0,3:0,4:0},"LLH4":{0:0,1:0,2:0,3:0,4:0},"LLH5":{0:0,1:0,2:0,3:0,4:0},"LLH6":{0:0,1:0,2:0,3:0,4:0},"LLH7":{0:0,1:0,2:0,3:0,4:0},"LLH8":{0:0,1:0,2:0,3:0,4:0},"LLH9":{0:0,1:0,2:0,3:0,4:0},"LLH10":{0:0,1:0,2:0,3:0,4:0},"LLH11":{0:0,1:0,2:0,3:0,4:0},"LLH12":{0:0,1:0,2:0,3:0,4:0},"LLH13":{0:0,1:0,2:0,3:0,4:0},"LLH14":{0:0,1:0,2:0,3:0,4:0},"LLH15":{0:0,1:0,2:0,3:0,4:0}}
    for ins in range(len(results)):
        if method==1:
            l=[]
            for i in range(10):
                l=l+results[ins][i][15:]
            method_title="Adaptive Seq"
        if method==2:
            l=[]
            for i in range(10):
                l=l+results[ins][i]
            method_title=" Seq"
        
        for i in l:
            if len(i)>1:
                for j in i:
                    lcount[j][ins]+=1
    count=[]
    for ins in range(len(results)):
        countins=0
        for i in lcount:
            countins+=lcount[i][ins]
        count.append(countins)
    lcount["other"]={0:0,1:0,2:0,3:0,4:0}
    x=list(lcount.keys())
    for i in x:
        for ins in range(len(results)):
            if lcount[i][ins]/count[ins]<percent:
                lcount["other"][ins]+=lcount[i][ins]
                lcount[i][ins]=0
    for i in x:
        c=0
        for ins in range(len(results)):
            if lcount[i][ins]==0:
                c+=1
        if c==5:
            lcount.pop(i) 
    percentage=[]
    for i in lcount:
        lcountp=[]
        for ins in range(len(results)):
            lcountp.append(lcount[i][ins]/count[ins])
        percentage.append(lcountp)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["Ins 1","Ins 2","Ins 3","Ins 4","Ins 5"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, -0.15), loc='upper right',ncol=8)
    ax.set_title(method_title) 
    
#grouped by type
def llh_types(results,method,ins):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
        method_title="Adaptive Seq"
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]
        method_title=" Seq"
    lcount={"swaps inside routes":0,"swaps between vehicles":0,"insert":0,"Insertbetween":0,"changes to hubs":0,"remove":0,"direct or not":0}
    for i in l:
        for j in i:
            if j==0 or j==14:
                lcount["swaps inside routes"]+=1
            elif j==2 or j==6:
                lcount["swaps between vehicles"]+=1
            elif j==1 or j==7:
                lcount["insert"]+=1
            elif j==3 or j==8:
                lcount["Insertbetween"]+=1
            elif j==4 or j==9 or j==5:
                lcount["changes to hubs"]+=1
            elif j==10 or j==11:
                lcount["remove"]+=1
            elif j==12 or j==13:
                lcount["direct or not"]+=1
    count=0
    for i in lcount:
        count+=lcount[i]     
    percentage=[]
    for i in lcount:
        percentage.append(lcount[i]/count)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["LLH"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, 1), loc='upper right',ncol=4)
    ax.set_title("Instance "+ str(ins)+" "+ method_title)
    
#grouped by facilities
def llh_facilities(results,method,ins):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
        method_title="Adaptive Seq"
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]
        method_title=" Seq"
    lcount={"Depots":0,"Hubs":0,"Suppliers":0,"Mixed":0}
    for i in l:
        for j in i:
            if j==0 or j==1 or j==2 or j==10:
                lcount["Depots"]+=1
            elif j==4 or j==5:
                lcount["Hubs"]+=1
            elif j==6 or j==7 or j==8 or j==11 or j==14:
                lcount["Suppliers"]+=1
            elif j==12 or j==13:
                lcount["Mixed"]+=1
    count=0
    for i in lcount:
        count+=lcount[i]     
    percentage=[]
    for i in lcount:
        percentage.append(lcount[i]/count)
    percentage=np.array(percentage)
    percents=pd.DataFrame(percentage,index=lcount,columns=["LLH"])
    ax = percents.T.plot(kind='barh', stacked=True)
    ax.legend(bbox_to_anchor=(1.4, 1), loc='upper right',ncol=8)
    ax.set_title("Instance "+ str(ins)+" "+ method_title)
    
def llh_stats(results,method):
    if method==1:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"][15:]
    if method==2:
        l=[]
        for i in range(10):
            l=l+results[i]["llh"]    
    minl=1000
    maxl=0
    suml=0
    for i in l:
        if len(i)<minl:
            minl=len(i)
        if len(i)>maxl:
            maxl=len(i)
        suml+=len(i)
    mean=suml/len(l)
    return ("mean:",mean,"min:",minl,"max:",maxl)
    
def objandinfe(results):
    objandinfe=[]
    for i in range(10):
        path=[]
        for j in range(len(results[i]["path"])):
            path.append(results[i]["path"][j])

        objandinfe.append(path)
    return objandinfe
 