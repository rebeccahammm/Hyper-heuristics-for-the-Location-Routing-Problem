
#Instance 73.66
#Instance0 159.66
#Instance1 103.08


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 14:16:52 2021

@author: hammr
"""
import matplotlib.pyplot as plt
import problem_class as pc
import solution_class as sc
import heuristic_methods as hm
import random


def heuristic(problem):
    # Generating first purmuataion and its cost function
    cities=[]
    for i in range(problem.getNODepot()):
        cities.append(problem.getDepot(i).getID())
    random.shuffle(cities)
    solution=sc.Solution(problem)
    solution.setVehicleS("SV1","V1")
    h=hm.heuristic_methods(problem)
    for x in range(len(cities))                                                                                     :
        solution.getVehicleS(0).setVisit(problem.getDepot(problem.getDepotINDEX(cities[x])).getID(),problem.getDemand(problem.getDemandINDEX(problem.getDepot(problem.getDepotINDEX(cities[x])).getID(),"P1").getQUANTITY()))
    cost=solution.getObjectiveFunction()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    for i in range(5):
        # Generating a swap
        print("before swap",solution.getVehicleS(0).getVisits(),cost)
        h.ApplyHeuristic(0, solution)
        newcost=solution.getObjectiveFunction()
        print("after swap",solution.getVehicleS(0).getVisits(),newcost)
        if newcost<=cost:
            cost=newcost
            solution.CopyTo(previous_solution)
            if newcost<best_cost:
                solution.CopyTo(best_solution)
                best_cost=cost
        else:
            previous_solution.CopyTo(solution)
    return best_solution.getVehicleS(0).getVisits()

#assigns each city a vehicle
def allocating_cites(solution,problem):
    allocation=[]
    for i in range(problem.getNODepot()):
        allocation.append(random.randint(0,solution.getNOVehicleS()-1))
    return allocation
def heuristic_vrp(problem):
    # Generating first purmuataion and its cost function
    solution=sc.Solution(problem)
    h=hm.heuristic_methods(problem)
    for i in range(problem.getNODepot()):
        VID=random.randint(0,problem.getNOVehicles())
        solution.setVehicleS("SV"+str(i+1),"V"+str(VID))
    allocationofcities=allocating_cites(problem.getNODepot(),solution.getNOVehicleS())
    cost=0
    #sorting assignment into routes
    for i in range(solution.getNOVehicleS()):
        solution.getVehicleS(i).setVisit(problem.getHub(0).getID())
    for i in range(len(allocationofcities)):
        solution.getVehicleS(allocationofcities[i]).setVisit(problem.getDepot(i).getID())
    #Calculate total costs of routes
    cost=solution.getObjectiveFunction()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    for i in range(5):
        #Generating a swap
        print("before swap",solution.ShowSolution(),cost)
        h.ApplyHeuristic(3, solution)
        newcost=solution.getObjectiveFunction()
        print("after swap",solution.ShowSolution(),newcost)
        #check whether to keep the swap
        if newcost<cost:
            cost=newcost
            solution.CopyTo(previous_solution)
            if newcost<best_cost:
                solution.CopyTo(best_solution)
                best_cost=cost
        else:
            previous_solution.CopyTo(solution)
    return (solution.ShowSolution(),best_cost)
def greedy_allocation(solution,problem):
    allocation=[]
    for i in range(problem.getNODepot()):
        distances=[problem.getDistance(problem.getDepot(i).getID(),solution.getVehicleS(j).getVisit(solution.getVehicleS(j).getNOvisits()-1).getID())for j in range(solution.getNOVehicleS())]
        min_dist=min(distances)
        allocation.append(distances.index(min_dist))
    return allocation  
def random_supplier_allocation(problem,solution):
    Hub_throughput={}
    for i in range(solution.getNOVehicleS()):
        if solution.getVehicleS(i).getVisit(0).getID()[1]=="H":
            if solution.getVehicleS(i).getVisit(0).getID() not in Hub_throughput:
                Hub_throughput[solution.getVehicleS(i).getVisit(0).getID()]=solution.getVehicleS(i).getMaxLoad()
            else:
                Hub_throughput[solution.getVehicleS(i).getVisit(0).getID()]+=solution.getVehicleS(i).getMaxLoad()
    count=1
    for i in Hub_throughput:
        throughput_left=Hub_throughput[i]
        while throughput_left>0:
            VID=random.randint(1,problem.getNOVehicles())
            solution.setSupplierRoute("SSV"+str(count),"V"+str(VID))
            solution.getSupplierRoute(count-1).insertVisit(0,sc.Visit(i))
            capacity=problem.getVehicle(problem.getVehicleINDEX("V"+str(VID))).getCAPACITY()
            while capacity>0:
                j=random.randint(0,problem.getNOsuppliers()-1)
                quanitychange=min(throughput_left,problem.getSupplierCapacity(problem.getSupplierCapacityINDEX(problem.getSupplier(j).getID(),"PT1")).getQUANTITY(),capacity)
                solution.getSupplierRoute(count-1).insertVisit(solution.getSupplierRoute(count-1).getNOvisits(),sc.Visit(problem.getSupplier(j).getID()))
                solution.getSupplierRoute(count-1).getVisit(solution.getSupplierRoute(count-1).getNOvisits()-1).setQUANTITYCHANGE(quanitychange)
                throughput_left-=quanitychange
                capacity-=quanitychange
                if throughput_left<=0:break
            count+=1
    while solution.getNOVehicleS()-solution.getNOSupplierRoutes()>0:
        VID=random.randint(1,problem.getNOVehicles())
        solution.setSupplierRoute("SSV"+str(solution.getNOSupplierRoutes()),"V"+str(VID))
        j=random.randint(0,problem.getNOHubs()-1)
        solution.getSupplierRoute(solution.getNOSupplierRoutes()-1).setVisit(problem.getHub(j).getID())
    return solution
def initial_solution_random(problem,solution):
    for i in range(problem.getNODepot()):
        VID=random.randint(1,problem.getNOVehicles())
        solution.setVehicleS("SV"+str(i+1),"V"+str(VID))
    #sorting assignment into routes
    vehiclecount=0
    while vehiclecount<solution.getNOVehicleS():
        f=random.choice(["H","S"])
        if f=="H":
            j=random.randint(0,problem.getNOHubs()-1)
            if problem.getHub(j).getExisting()==False:
                if solution.getNOOpenedHubs()<problem.getMaxNewHubs():
                    solution.setNewHubs(problem.getHub(j).getID(),vehiclecount)
                    solution.getVehicleS(vehiclecount).setVisit(problem.getHub(j).getID())
                    vehiclecount+=1
            else:
                solution.getVehicleS(vehiclecount).setVisit(problem.getHub(j).getID())
                vehiclecount+=1
        if f=="S":
            j=random.randint(0, problem.getNOsuppliers()-1)
            solution.getVehicleS(vehiclecount).setVisit(problem.getSupplier(j).getID())
            vehiclecount+=1
    allocationofcities=allocating_cites( solution,problem)
    for i in range(len(allocationofcities)):
        solution.getVehicleS(allocationofcities[i]).setVisit(problem.getDepot(i).getID(),problem.getDemand(problem.getDemandINDEX(problem.getDepot(i).getID(),"PT1")).getQUANTITY())
    #Checking vehicle capacity constraints
    for i in range(solution.getNOVehicleS()):
        solution.getVehicleS(i).setMaxLoad()
        if solution.getVehicleS(i).getVisit(0).getID()[1]=="H":
            if problem.getHub(problem.getHubINDEX(solution.getVehicleS(i).getVisit(0).getID())).getExisting()==False:
                solution.getNewHubs(solution.getNewHubsINDEX(i)).setTHROUGHPUT(solution.getVehicleS(i).getMaxLoad())
                if solution.getVehicleS(i).getMaxLoad()<problem.getMinThroughput():
                    possibl_hubs=[]
                    for j in range(problem.getNOHubs()):
                        if problem.getHub(j).getExisting()==True:
                            possibl_hubs.append(j)
                    newhub=problem.getHub(random.choice(possibl_hubs)).getID()
                    visit1=solution.getVehicleS(i).getVisit(0)
                    solution.getVehicleS(i).removeVisit(visit1)
                    solution.removeHub(solution.getNewHubsINDEX(i))
                    solution.getVehicleS(i).insertVisit(0, sc.Visit(newhub))
        solution.capconstraint(i)
    #adding supplier routes
    solution=random_supplier_allocation(problem, solution)
    
    return solution
def greedy_supplier_allocation(solution,problem):
    Hub_throughput={}
    for i in range(solution.getNOVehicleS()):
        if solution.getVehicleS(i).getVisit(0).getID()[1]=="H":
            if solution.getVehicleS(i).getVisit(0).getID() not in Hub_throughput:
                Hub_throughput[solution.getVehicleS(i).getVisit(0).getID()]=solution.getVehicleS(i).getMaxLoad()
            else:
                Hub_throughput[solution.getVehicleS(i).getVisit(0).getID()]+=solution.getVehicleS(i).getMaxLoad()
    count=1
    for i in Hub_throughput:
        throughput_left=Hub_throughput[i]
        distances=[problem.getDistance(problem.getSupplier(j).getID(),i)for j in range(problem.getNOsuppliers())]
        while throughput_left>0:
            VID=random.randint(1,problem.getNOVehicles())
            solution.setSupplierRoute("SSV"+str(count),"V"+str(VID))
            solution.getSupplierRoute(count-1).insertVisit(0,sc.Visit(i))
            capacity=problem.getVehicle(problem.getVehicleINDEX("V"+str(VID))).getCAPACITY()
            while capacity>0:
                min_dist=min(distances)
                j=distances.index(min_dist)
                quanitychange=min(throughput_left,problem.getSupplierCapacity(problem.getSupplierCapacityINDEX(problem.getSupplier(j).getID(),"PT1")).getQUANTITY(),capacity)
                capacity-=quanitychange
                solution.getSupplierRoute(count-1).insertVisit(solution.getSupplierRoute(count-1).getNOvisits(),sc.Visit(problem.getSupplier(j).getID()))
                solution.getSupplierRoute(count-1).getVisit(solution.getSupplierRoute(count-1).getNOvisits()-1).setQUANTITYCHANGE(quanitychange)
                throughput_left-=quanitychange
                if throughput_left<=0: break
                distances[j]=100000
            count+=1  
    while solution.getNOVehicleS()-solution.getNOSupplierRoutes()>0:
        VID=random.randint(1,problem.getNOVehicles())
        solution.setSupplierRoute("SSV"+str(solution.getNOSupplierRoutes()),"V"+str(VID))
        j=random.randint(0,problem.getNOHubs()-1)
        solution.getSupplierRoute(solution.getNOSupplierRoutes()-1).setVisit(problem.getHub(j).getID())
    return solution
def initial_solution_greedy_depot_allocation(problem,solution):
    for i in range(problem.getNODepot()):
        VID=random.randint(1,problem.getNOVehicles())
        solution.setVehicleS("SV"+str(i+1),"V"+str(VID))
    #sorting assignment into routes
    vehiclecount=0
    while vehiclecount<solution.getNOVehicleS():
        f=random.choice(["H","S"])
        if f=="H":
            j=random.randint(0,problem.getNOHubs()-1)
            if problem.getHub(j).getExisting()==False:
                if solution.getNOOpenedHubs()<problem.getMaxNewHubs():
                    solution.setNewHubs(problem.getHub(j).getID(),vehiclecount)
                    solution.getVehicleS(vehiclecount).setVisit(problem.getHub(j).getID())
                    vehiclecount+=1
            else:
                solution.getVehicleS(vehiclecount).setVisit(problem.getHub(j).getID())
                vehiclecount+=1
        if f=="S":
            j=random.randint(0, problem.getNOsuppliers()-1)
            solution.getVehicleS(vehiclecount).setVisit(problem.getSupplier(j).getID())
            vehiclecount+=1
    allocationofcities=greedy_allocation(solution, problem)
    for i in range(len(allocationofcities)):
        solution.getVehicleS(allocationofcities[i]).setVisit(problem.getDepot(i).getID(),problem.getDemand(problem.getDemandINDEX(problem.getDepot(i).getID(),"PT1")).getQUANTITY())
    #Checking vehicle capacity constraints
    for i in range(solution.getNOVehicleS()):
        solution.getVehicleS(i).setMaxLoad()
        if solution.getVehicleS(i).getVisit(0).getID()[1]=="H":
            if problem.getHub(problem.getHubINDEX(solution.getVehicleS(i).getVisit(0).getID())).getExisting()==False:
                solution.getNewHubs(solution.getNewHubsINDEX(i)).setTHROUGHPUT(solution.getVehicleS(i).getMaxLoad())
                if solution.getVehicleS(i).getMaxLoad()<problem.getMinThroughput():
                    possibl_hubs=[]
                    for j in range(problem.getNOHubs()):
                        if problem.getHub(j).getExisting()==True:
                            possibl_hubs.append(j)
                    newhub=problem.getHub(random.choice(possibl_hubs)).getID()
                    visit1=solution.getVehicleS(i).getVisit(0)
                    solution.getVehicleS(i).removeVisit(visit1)
                    solution.removeHub(solution.getNewHubsINDEX(i))
                    solution.getVehicleS(i).insertVisit(0, sc.Visit(newhub))
        solution.capconstraint(i)
    solution=greedy_supplier_allocation(solution, problem)
    return solution
def EvaluateSolution(FileName,problem):
    solution=sc.Solution(problem)
    solution.ReadFromFile(FileName)
    solution.printSolution()
def heuristic_lrp(problem,max_new_hubs,min_throughput,max_time):
    #setting parameters and classes
    problem.setMaxNewHubs(max_new_hubs)
    problem.setMinThroughput(min_throughput)
    problem.setMaxTime(max_time)
    solution=sc.Solution(problem)
    h=hm.heuristic_methods(problem)
    #initialing solution
    solution=initial_solution_greedy_depot_allocation(problem, solution)
    #Calculate total costs
    cost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
    previous_solution=sc.Solution(problem)
    solution.CopyTo(previous_solution)
    best_solution=sc.Solution(problem)
    solution.CopyTo(best_solution)
    best_cost=cost
    #performing swaps
    L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    T=1500*1000
    for i in range(T):
        selected_heuristic = random.choice(L)
        print("before operator",selected_heuristic,solution.getSolution(),cost)
        h.ApplyHeuristic(selected_heuristic, solution)
        newcost=solution.getObjectiveFunction() + 100000*solution.Feasibility()
        print("after operator",solution.getSolution(),newcost)
        #check whether to keep the swap
        if (newcost<=cost) or (newcost<=best_cost + 0.009*best_cost):
            cost=newcost
            solution.CopyTo(previous_solution)
            if newcost<best_cost:
                solution.CopyTo(best_solution)
                best_cost=cost
        else:
            previous_solution.CopyTo(solution)
    return (best_solution,best_cost,L)




def plot(p,s,t,sol):
    facilities=[]
    for i in range(p.getNODepot()):
        facilities.append(p.getDepot(i))
    lats=[]
    longs=[]
    for i in range(len(facilities)):
        lats.append(facilities[i].getLATITUDE())
        longs.append(facilities[i].getLONGITUDE())
    facilities1=[]
    facilities2=[]
    for i in range(p.getNOHubs()):
        if p.getHub(i).getExisting()==True:
            facilities1.append(p.getHub(i))
        else:
            facilities2.append(p.getHub(i))
    lats1=[]
    longs1=[]
    lats2=[]
    longs2=[]
    facilities3=[]
    for i in range(p.getNOsuppliers()):
        facilities3.append(p.getSupplier(i))
    lats3=[]
    longs3=[]
    for i in range(len(facilities3)):
        lats3.append(facilities3[i].getLATITUDE())
        longs3.append(facilities3[i].getLONGITUDE())
    for i in range(len(facilities1)):
        lats1.append(facilities1[i].getLATITUDE())
        longs1.append(facilities1[i].getLONGITUDE())
    for i in range(len(facilities2)):
        lats2.append(facilities2[i].getLATITUDE())
        longs2.append(facilities2[i].getLONGITUDE())
    plt.scatter(lats,longs,c="#ffb7c5",marker="s")
    plt.scatter(lats1,longs1,c="#967bb6")
    plt.scatter(lats2, longs2, c="#663399")
    plt.scatter(lats3, longs3, c="#9bddff",marker="d")
    for i in range(sol.getNOVehicleS()):
        lats2=[]
        long2=[]
        if s[i][0][1]=="H":
            lats2.append(p.getHub(p.getHubINDEX(s[i][0])).getLATITUDE())
            long2.append(p.getHub(p.getHubINDEX(s[i][0])).getLONGITUDE())
        if s[i][0][0]=="S":
            lats2.append(p.getSupplier(p.getSupplierINDEX(s[i][0])).getLATITUDE())
            long2.append(p.getSupplier(p.getSupplierINDEX(s[i][0])).getLONGITUDE())
        for j in s[i][1:]:
            lats2.append(p.getDepot(p.getDepotINDEX(j)).getLATITUDE())
            long2.append(p.getDepot(p.getDepotINDEX(j)).getLONGITUDE())
        if s[i][0][1]=="H":
            lats2.append(p.getHub(p.getHubINDEX(s[i][0])).getLATITUDE())
            long2.append(p.getHub(p.getHubINDEX(s[i][0])).getLONGITUDE())
        if s[i][0][0]=="S":
            lats2.append(p.getSupplier(p.getSupplierINDEX(s[i][0])).getLATITUDE())
            long2.append(p.getSupplier(p.getSupplierINDEX(s[i][0])).getLONGITUDE())
        plt.plot(lats2, long2)
    for i in range(sol.getNOVehicleS(),sol.getNOVehicleS()+sol.getNOSupplierRoutes()):
        lats2=[]
        long2=[]
        lats2.append(p.getHub(p.getHubINDEX(s[i][0])).getLATITUDE())
        long2.append(p.getHub(p.getHubINDEX(s[i][0])).getLONGITUDE())
        for j in s[i][1:]:
            lats2.append(p.getSupplier(p.getSupplierINDEX(j)).getLATITUDE())
            long2.append(p.getSupplier(p.getSupplierINDEX(j)).getLONGITUDE())
        lats2.append(p.getHub(p.getHubINDEX(s[i][0])).getLATITUDE())
        long2.append(p.getHub(p.getHubINDEX(s[i][0])).getLONGITUDE())
        plt.plot(lats2, long2,ls=":")
    plt.title(t)
 