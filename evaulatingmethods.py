#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:31:10 2022

@author: hammr
"""
import problem_class as pc
import solution_class as sc
import heuristic_methods as hm
import random
import tspheuristic as inti
import multiprocessing
import pickle



def bram(problem,max_new_hubs,min_throughput,max_time):
    #setting parameters and classes
    size=problem.getNODepot()+problem.getNOHubs()+problem.getNOsuppliers()
    problem.setMaxNewHubs(max_new_hubs)
    problem.setMinThroughput(min_throughput)
    problem.setMaxTime(max_time)
    solution=sc.Solution(problem)
    h=hm.heuristic_methods(problem)
    #initialing solution
    solution=inti.initial_solution_random(problem, solution)
    #Calculate total costs
    cost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    #performing swaps
    bestpath=[]
    bestinfeas=[]
    path=[]
    infeas=[]
    moments=[]
    L = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14]]
    T=1500*size*10
    for j in range(T):
        selected_heuristic = random.choice(L)
        for i in selected_heuristic:
            h.ApplyHeuristic(i, solution)
        if random.randint(0,2) == 0:
            selected_heuristic2=random.choice(L)
            for i in selected_heuristic2:
                h.ApplyHeuristic(i, solution)
            selected_heuristic=selected_heuristic+selected_heuristic2
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        #check whether to keep the swap
        t=0.09/(size**3)
        if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
            if newcost>cost:
                moments.append(j)
            cost=newcost
            solution.CopyTo(previous_solution)
            if newcost<best_cost:
                solution.CopyTo(best_solution)
                best_cost=cost
                L.append(selected_heuristic)
        else:
            previous_solution.CopyTo(solution)
        bestpath.append(best_solution.getObjectiveFunction())
        bestinfeas.append(best_solution.Feasibility())
        path.append(previous_solution.getObjectiveFunction())
        infeas.append(previous_solution.Feasibility())
    return (best_solution,best_cost,L,path,infeas,moments)

def testingmethods_B(max_new_hubs=2,min_throughput=8,max_time=1500,instances=["instance0.json","instance1.json","instance.json","instance3.json"]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for i in range(10):
            random.seed(i)
            sol,obj,L,path,infe,m=bram(p,2,8,1500)
            results[j][i]={"path":path,"infeasible":infe,"llh":L,"moments":m}
    return results

def ch(problem,max_new_hubs,min_throughput,max_time):
    #setting parameters and classes
    size=problem.getNODepot()+problem.getNOHubs()+problem.getNOsuppliers()
    #+problem.getNOVehicles()
    problem.setMaxNewHubs(max_new_hubs)
    problem.setMinThroughput(min_throughput)
    problem.setMaxTime(max_time)
    solution=sc.Solution(problem)
    h=hm.heuristic_methods(problem)
    #initialing solution
    solution=inti.initial_solution_greedy_depot_allocation(problem,solution)
    #Calculate total costs
    cost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    #performing swaps
    bestpath=[]
    bestinfeas=[]
    path=[]
    infeas=[]
    L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    T=1500*size*10
    llh=[]
    k=[]
    moments=[]
    for i in range(T):
        selected_heuristic = random.choice(L)
        k.append(selected_heuristic)
        h.ApplyHeuristic(selected_heuristic, solution)  
        if random.randint(0,2) == 0:
            continue
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        #check whether to keep the swap
        t=0.09/(size**3)
        if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
            if newcost>cost:
                moments.append(i)
            cost=newcost
            solution.CopyTo(previous_solution)
            if newcost<best_cost:
                solution.CopyTo(best_solution)
                best_cost=cost
                llh.append(k)
        else:
            previous_solution.CopyTo(solution)
        bestpath.append(best_solution.getObjectiveFunction())
        bestinfeas.append(best_solution.Feasibility())
        path.append(previous_solution.getObjectiveFunction())
        infeas.append(previous_solution.Feasibility())
        k=[]
    return (best_solution,best_cost,llh,path,infeas,moments)

def testingmethods_c(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for i in range(10):
            random.seed(i)
            sol,obj,L,path,infe,m=ch(p,max_new_hubs,min_throughput,max_time)
            results[j][i]={"path":path,"infeasible":infe,"llh":L,"moments":m}
    return results





def RunHeuristic(fTuple):
    Result=fTuple[0](fTuple[2][0],fTuple[2][1],fTuple[2][2],fTuple[2][3])
    pickle.dump(Result,open(fTuple[1],"wb"))


def Runall(no_processes,ListOfFunctions=[(testingmethods_B(),"Anaylis_of_random_ADSHRR_ins_0.p",[2,8,1500,["instance0.json"]]),
                 (testingmethods_B(),"Anaylis_of_random_ADSHRR_ins_1.p", [2,8,1500,["instance1.json"]]),
                 (testingmethods_B(),"Anaylis_of_random_ADSHRR_ins_2.p",[2,8,1500,["instance.json"]]),
                 (testingmethods_B(),"Anaylis_of_random_ADSHRR_ins_3.p",[2,8,1500,["instance3.json"]]),
                 (testingmethods_c(),"Anaylis_of_greedy_SHRR_ins_0.p",[2,8,1500,["instance0.json"]]),
                 (testingmethods_c(),"Anaylis_of_greedy_SHRR_ins_1.p",[2,8,1500,["instance1.json"]]),
                 (testingmethods_c(),"Anaylis_of_greedy_SHRR_ins_2.p",[2,8,1500,["instance.json"]]),
                 (testingmethods_c(),"Anaylis_of_greedy_SHRR_ins_3.p",[2,8,1500,["instance3.json"]])]):
    pool=multiprocessing.Pool(no_processes)
    pool.map(RunHeuristic,ListOfFunctions)

 
