#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 07:51:55 2022

@author: hammr
"""


import problem_class as pc
import solution_class as sc
import heuristic_methods as hm
import random
import statistics as st
import math
import heuristic as inti
import multiprocessing
import pickle  

def simple_random_greedy(problem,max_new_hubs,min_throughput,max_time,accept,optimal):
    #setting parameters and classes
    size=problem.getNODepot()+problem.getNOHubs()+problem.getNOsuppliers()
    problem.setMaxNewHubs(max_new_hubs)
    problem.setMinThroughput(min_throughput)
    problem.setMaxTime(max_time)
    solution=sc.Solution(problem)
    h=hm.heuristic_methods(problem)
    #initialing solution
    solution=inti.initial_solution_greedy_depot_allocation(problem, solution)
    
    #Calculate total costs
    cost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    F=1
    #performing swaps
    L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    T=1500*size
    for i in range(T):
        selected_heuristic = random.choice(L)
        h.ApplyHeuristic(selected_heuristic, solution)  
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        #check whether to keep the swap
        if accept==0:
            if (newcost<=cost):  #IE - Improve or Equal
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==1:
            if (newcost<cost):  #OI - Only Improve
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==2:
            t=0.09/(size**3)

            if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==3:
            if (newcost<=cost) or (newcost<=optimal+F*(1-(i/T))): #GD:Great Deluge
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==4:
            try:
                p=math.exp((cost-newcost)/(F*(1-(i/T))))
            except OverflowError:
                p=-float("inf")
            if (newcost<=cost):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            elif p>random.random():
                cost=newcost
                solution.CopyTo(previous_solution)
            else:
                previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L,F)


def Adaptive_greedy(problem,max_new_hubs,min_throughput,max_time,accept,optimal):
    #setting parameters and classes
    size=problem.getNODepot()+problem.getNOHubs()+problem.getNOsuppliers()
    problem.setMaxNewHubs(max_new_hubs)
    problem.setMinThroughput(min_throughput)
    problem.setMaxTime(max_time)
    solution=sc.Solution(problem)
    h=hm.heuristic_methods(problem)
    #initialing solution
    solution=inti.initial_solution_greedy_depot_allocation(problem, solution)
    #Calculate total costs
    cost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    F=1
    #performing swaps
    L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    T=1500*size
    for i in range(T):
        selected_heuristic = random.choice(L)
        h.ApplyHeuristic(selected_heuristic, solution)  
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        #check whether to keep the swap
        if accept==0:
            if (newcost<=cost):  #IE - Improve or Equal
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic) # a kind of RL
            else:
                previous_solution.CopyTo(solution)
        if accept==1:
            if (newcost<cost):  #OI - Only Improve
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic) # a kind of RL
            else:
                previous_solution.CopyTo(solution)
        if accept==2:
            t=0.09/(size**3)
            if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic) # a kind of RL
            else:
                previous_solution.CopyTo(solution)
        if accept==3:
            if (newcost<=cost) or (newcost<=optimal+F*(1-(i/T))):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==4:
            try:
                p=math.exp((cost-newcost)/(F*(1-(i/T))))
            except OverflowError:
                p=-float("inf")
            if (newcost<=cost):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            elif p>random.random():
                cost=newcost
                solution.CopyTo(previous_solution)
            else:
                previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L)

def Sequences_greedy(problem,max_new_hubs,min_throughput,max_time,accept,optimal):
    #setting parameters and classes
    size=problem.getNODepot()+problem.getNOHubs()+problem.getNOsuppliers()
    problem.setMaxNewHubs(max_new_hubs)
    problem.setMinThroughput(min_throughput)
    problem.setMaxTime(max_time)
    solution=sc.Solution(problem)
    h=hm.heuristic_methods(problem)
    #initialing solution
    solution=inti.initial_solution_greedy_depot_allocation(problem, solution)
    #Calculate total costs
    cost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    F=1
    #performing swaps
    L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    T=1500*size
    for i in range(T):
        selected_heuristic = random.choice(L)
        h.ApplyHeuristic(selected_heuristic, solution)  
        if random.randint(0,2) == 0:
            continue
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        #check whether to keep the swap
        if accept==0:
            if (newcost<=cost):  #IE - Improve or Equal
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==1:
            if (newcost<cost):  #OI - Only Improve
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==2:
            t=0.09/(size**3)
            if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==3:
            if (newcost<=cost) or (newcost<=optimal+F*(1-(i/T))):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==4:
            try:
                p=math.exp((cost-newcost)/(F*(1-(i/T))))
            except OverflowError:
                p=-float("inf")
            if (newcost<=cost):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            elif p>random.random():
                cost=newcost
                solution.CopyTo(previous_solution)
            else:
                previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L)

def ADSH_greedy(problem,max_new_hubs,min_throughput,max_time,accept,optimal):
    #setting parameters and classes
    size=problem.getNODepot()+problem.getNOHubs()+problem.getNOsuppliers()
    problem.setMaxNewHubs(max_new_hubs)
    problem.setMinThroughput(min_throughput)
    problem.setMaxTime(max_time)
    solution=sc.Solution(problem)
    h=hm.heuristic_methods(problem)
    #initialing solution
    solution=inti.initial_solution_greedy_depot_allocation(problem, solution)
    #Calculate total costs
    cost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    F=1
    #performing swaps
    L = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14]]
    T=1500*size
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
        if accept==0:
            if (newcost<=cost):  #IE - Improve or Equal
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==1:
            if (newcost<cost):  #OI - Only Improve
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==2:
            t=0.09/(size**3)
            if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==3:
            if (newcost<=cost) or (newcost<=optimal+F*(1-(j/T))):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==4:
            try:
                p=math.exp((cost-newcost)/(F*(1-(j/T))))
            except OverflowError:
                p=-float("inf")
            if (newcost<=cost):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            elif p>random.random():
                cost=newcost
                solution.CopyTo(previous_solution)
            else:
                previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L)

def simple_random_random(problem,max_new_hubs,min_throughput,max_time,accept,optimal):
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
    F=1
    #performing swaps
    L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    T=1500*size
    for i in range(T):
        selected_heuristic = random.choice(L)
        h.ApplyHeuristic(selected_heuristic, solution)  
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        #check whether to keep the swap
        if accept==0:
            if (newcost<=cost):  #IE - Improve or Equal
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==1:
            if (newcost<cost):  #OI - Only Improve
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==2:
            t=0.09/(size**3)
            if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==3:
            if (newcost<=cost) or (newcost<=optimal+F*(1-(i/T))):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==4:
            try:
                p=math.exp((cost-newcost)/(F*(1-(i/T))))
            except OverflowError:
                p=-float("inf")
            if (newcost<=cost):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            elif p>random.random():
                cost=newcost
                solution.CopyTo(previous_solution)
            else:
                previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L,F)


def Adaptive_random(problem,max_new_hubs,min_throughput,max_time,accept,optimal):
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
    F=1
    #performing swaps
    L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    T=1500*size
    for i in range(T):
        selected_heuristic = random.choice(L)
        h.ApplyHeuristic(selected_heuristic, solution)  
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        #check whether to keep the swap
        if accept==0:
            if (newcost<=cost):  #IE - Improve or Equal
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic) # a kind of RL
            else:
                previous_solution.CopyTo(solution)
        if accept==1:
            if (newcost<cost):  #OI - Only Improve
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic) # a kind of RL
            else:
                previous_solution.CopyTo(solution)
        if accept==2:
            t=0.09/(size**3)
            if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic) # a kind of RL
            else:
                previous_solution.CopyTo(solution)
        if accept==3:
            if (newcost<=cost) or (newcost<=optimal+F*(1-(i/T))):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==4:
            try:
                p=math.exp((cost-newcost)/(F*(1-(i/T))))
            except OverflowError:
                p=-float("inf")
            if (newcost<=cost):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            elif p>random.random():
                cost=newcost
                solution.CopyTo(previous_solution)
            else:
                previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L)

def Sequences_random(problem,max_new_hubs,min_throughput,max_time,accept,optimal):
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
    F=1
    #performing swaps
    L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    T=1500*size
    for i in range(T):
        selected_heuristic = random.choice(L)
        h.ApplyHeuristic(selected_heuristic, solution)  
        if random.randint(0,2) == 0:
            continue
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        #check whether to keep the swap
        if accept==0:
            if (newcost<=cost):  #IE - Improve or Equal
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==1:
            if (newcost<cost):  #OI - Only Improve
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==2:
            t=0.09/(size**3)
            if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==3:
            if (newcost<=cost) or (newcost<=optimal+F*(1-(i/T))):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            else:
                previous_solution.CopyTo(solution)
        if accept==4:
            try:
                p=math.exp((cost-newcost)/(F*(1-(i/T))))
            except OverflowError:
                p=-float("inf")
            if (newcost<=cost):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
            elif p>random.random():
                cost=newcost
                solution.CopyTo(previous_solution)
            else:
                previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L)

def ADSH_random(problem,max_new_hubs,min_throughput,max_time,accept,optimal):
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
    F=1
    #performing swaps
    L = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14]]
    T=1500*size
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
        if accept==0:
            if (newcost<=cost):  #IE - Improve or Equal
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==1:
            if (newcost<cost):  #OI - Only Improve
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==2:
            t=0.09/(size**3)
            if (newcost<=cost) or (newcost<=best_cost + t*best_cost): #RR: Record-to-Record
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==3:
            if (newcost<=cost) or (newcost<=optimal+F*(1-(j/T))):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            else:
                previous_solution.CopyTo(solution)
        if accept==4:
            try:
                p=math.exp((cost-newcost)/(F*(1-(j/T))))
            except OverflowError:
                p=-float("inf")
            if (newcost<=cost):
                cost=newcost
                solution.CopyTo(previous_solution)
                if newcost<best_cost:
                    solution.CopyTo(best_solution)
                    best_cost=cost
                    L.append(selected_heuristic)
            elif p>random.random():
                cost=newcost
                solution.CopyTo(previous_solution)
            else:
                previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L)


def testingmethods_SR_G(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"],optimal=[159.666,103.079,73.66,100]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for a in range(5):
            costs=[]
            #Fs=[]
            for i in range(50):
                random.seed(i)
                sol,obj,L,F=simple_random_greedy(p,max_new_hubs,min_throughput,max_time,a,optimal[j])
                costs.append(obj)
                #Fs.append(F)
            results[j][a]={"mean":st.mean(costs),"std":st.stdev(costs),"min":min(costs),"obj":costs}
    return results

def testingmethods_A_G(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"],optimal=[159.666,103.079,73.66,100]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for a in range(5):
            costs=[]
            for i in range(50):
                random.seed(i)
                sol,obj,L=Adaptive_greedy(p,max_new_hubs,min_throughput,max_time,a,optimal[j])
                costs.append(obj)
            results[j][a]={"mean":st.mean(costs),"std":st.stdev(costs),"min":min(costs),"obj":costs}
    return results
    
def testingmethods_S_G(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"],optimal=[159.666,103.079,73.66,100]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for a in range(5):
            costs=[]
            for i in range(50):
                random.seed(i)
                sol,obj,L=Sequences_greedy(p,max_new_hubs,min_throughput,max_time,a,optimal[j])
                costs.append(obj)
            results[j][a]={"mean":st.mean(costs),"std":st.stdev(costs),"min":min(costs),"obj":costs}
    return results
 
def testingmethods_ADSH_G(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"],optimal=[159.666,103.079,73.66,100]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for a in range(5):
            costs=[]
            for i in range(50):
                random.seed(i)
                sol,obj,L=ADSH_greedy(p,max_new_hubs,min_throughput,max_time,a,optimal[j])
                costs.append(obj)
            results[j][a]={"mean":st.mean(costs),"std":st.stdev(costs),"min":min(costs),"obj":costs}
    return results

def testingmethods_SR_R(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"],optimal=[159.666,103.079,73.66,100]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for a in range(5):
            costs=[]
            #Fs=[]
            for i in range(50):
                random.seed(i)
                sol,obj,L,F=simple_random_random(p,max_new_hubs,min_throughput,max_time,a,optimal[j])
                costs.append(obj)
                #Fs.append(F)
            results[j][a]={"mean":st.mean(costs),"std":st.stdev(costs),"min":min(costs),"obj":costs}
    return results

def testingmethods_A_R(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"],optimal=[159.666,103.079,73.66,100]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for a in range(5):
            costs=[]
            for i in range(50):
                random.seed(i)
                sol,obj,L=Adaptive_random(p,max_new_hubs,min_throughput,max_time,a,optimal[j])
                costs.append(obj)
            results[j][a]={"mean":st.mean(costs),"std":st.stdev(costs),"min":min(costs),"obj":costs}
    return results
    
def testingmethods_S_R(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"],optimal=[159.666,103.079,73.66,100]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for a in range(5):
            costs=[]
            for i in range(50):
                random.seed(i)
                sol,obj,L=Sequences_random(p,max_new_hubs,min_throughput,max_time,a,optimal[j])
                costs.append(obj)
            results[j][a]={"mean":st.mean(costs),"std":st.stdev(costs),"min":min(costs),"obj":costs}
    return results
 
def testingmethods_ADSH_R(max_new_hubs,min_throughput,max_time,instances=["instance0.json","instance1.json","instance.json","instance3.json"],optimal=[159.666,103.079,73.66,100]):
    results={}
    for j in range(len(instances)):
        p=pc.Problem(instances[j])
        p.read_problem_instance()
        results[j]={}
        for a in range(5):
            costs=[]
            for i in range(50):
                random.seed(i)
                sol,obj,L=ADSH_random(p,max_new_hubs,min_throughput,max_time,a,optimal[j])
                costs.append(obj)
            results[j][a]={"mean":st.mean(costs),"std":st.stdev(costs),"min":min(costs),"obj":costs}
    return results




def RunHeuristic(fTuple):
    Result=fTuple[0](fTuple[2][0],fTuple[2][1],fTuple[2][2],fTuple[2][3],fTuple[2][4])
    pickle.dump(Result,open(fTuple[1],"wb"))


def Runall(no_processes,ListOfFunctions):
    pool=multiprocessing.Pool(no_processes)
    pool.map(RunHeuristic,ListOfFunctions)

