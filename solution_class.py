#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 09:45:35 2021

@author: hammr
"""
import problem_class as pc
import sys
import json

#Class for visits to facilities
class Visit():
    def __init__(self, fID="", quantitychange=0):
        self.__ID = fID
        self.__quantitychange = quantitychange
    def getID(self):
        return self.__ID
    def setID(self, fID):
        self.__ID = fID
    def getQUANTITYCHANGE(self):
        return self.__quantitychange
    def setQUANTITYCHANGE(self, quantitychange):
        self.__quantitychange = quantitychange
    def __str__(self):
        return "ID: "+str(self.getID())

#Class for routes through suppliers    
class SupplierRoute():
    def __init__(self, sID="",vID=""):
        self.__ID = sID
        self.__Vehicle_ID=vID
        self.__visits = []
        self.__max_load=0
    def getID(self):
        return self.__ID
    def getVehicleID(self):
        return self.__Vehicle_ID
    def getNOvisits(self):
        return len(self.__visits)
    def getVisits(self):
        visits=[]
        for i in self.__visits:
            visits.append(i.getID())
        return visits
    def getRouteLength(self):
        return len(self.__visits)
    def getVisit(self, vindex) -> Visit:
        if vindex in range(0, self.getRouteLength()):
            return self.__visits[vindex]
        sys.exit(print("Vehicle Solution 2 error",vindex,self.getRouteLength()))
    def setVisit(self, fID, quantitychange=0):
        self.__visits.append(Visit(fID,quantitychange))
    def getVisitINDEX(self, fID):
        return self.__visits_map[fID]    
    def insertVisit(self, position, visit):
        self.__visits.insert(position, visit)
    def swapVisits(self,visitIndex1,visitIndex2):   
        self.__visits[visitIndex1],self.__visits[visitIndex2]=self.__visits[visitIndex2],self.__visits[visitIndex1]
    def removeVisit(self,visit):
        self.__visits.remove(visit)    
    def setMaxLoad(self):
        load=0
        for i in range(self.getNOvisits()):
            load+=self.getVisit(i).getQUANTITYCHANGE()
        self.__max_load=load    
    def getMaxLoad(self):
        return self.__max_load

#Class for routes through depots
class VehicleSolution():
    def __init__(self, sID="",vID=""):
        self.__ID = sID
        self.__Vehicle_ID=vID
        self.__visits = []
        self.__max_load=0
    def getID(self):
        return self.__ID
    def getVehicleID(self):
        return self.__Vehicle_ID
    def getNOvisits(self):
        return len(self.__visits)
    def getVisits(self):
        visits=[]
        for i in self.__visits:
            visits.append(i.getID())
        return visits
    def getRouteLength(self):
        return len(self.__visits)
    def getVisit(self, vindex) -> Visit:
        if vindex in range(0, self.getRouteLength()):
            return self.__visits[vindex]
        sys.exit(print("Vehicle Solution 2 error",vindex,self.getRouteLength()))
    def setVisit(self, fID, quantitychange=0):
        self.__visits.append(Visit(fID,quantitychange))
    def getVisitINDEX(self, fID):
        return self.__visits_map[fID]
    def insertVisit(self, position, visit):
        self.__visits.insert(position, visit)
    def swapVisits(self,visitIndex1,visitIndex2):   
        self.__visits[visitIndex1],self.__visits[visitIndex2]=self.__visits[visitIndex2],self.__visits[visitIndex1]
    def removeVisit(self,visit):
        self.__visits.remove(visit)
    def setMaxLoad(self):
        load=0
        for i in range(1,self.getNOvisits()):
            #print(i)
            load+=self.getVisit(i).getQUANTITYCHANGE()
        self.__max_load=load
    def getMaxLoad(self):
        return self.__max_load

#class for newhubs
class NewHubsSolution():
    def __init__(self, hID="", throughput=0,opened=True):
        self.__ID = hID
        self.__throughput = throughput
        self.__Open=opened
    def getID(self):
        return self.__ID
    def setID(self, hID):
        self.__ID = hID
    def getTHROUGHPUT(self):
        return self.__throughput
    def setTHROUGHPUT(self, throughput):
        self.__throughput = throughput 
    def setOPENED(self,opened):
        self.__Open= opened   
    def getOPENED(self):
        return self.__Open
 
#class for solution as a whole
class Solution():
    def __init__(self, problem):
        self.__vehicles = []
        self.__newhubs = []
        self.__newhubs_map={}
        self.__problem = problem
        self.__supplier_routes=[]
    def getProblem(self) -> pc.Problem:
        return self.__problem
    def getNOVehicleS(self):
        return len(self.__vehicles)
    def getVehicleS(self, vindex) -> VehicleSolution:
        if vindex in range(0, self.getNOVehicleS()):
            return self.__vehicles[vindex]
        sys.exit(print("Vehicle Solution 1 error",vindex,self.getNOVehicleS()))
    def setVehicleS(self, svID,vID):
        self.__vehicles.append(VehicleSolution(svID,vID))  
    def emptyVehicleS(self):
        self.__vehicles.clear()
    def getNOSupplierRoutes(self):
        return len(self.__supplier_routes)
    def getSupplierRoute(self, vindex) -> SupplierRoute:
        if vindex in range(0, self.getNOSupplierRoutes()):
            return self.__supplier_routes[vindex]
        sys.exit(print("Supplier Solution 1 error"))
    def setSupplierRoute(self, svID,vID):
        self.__supplier_routes.append(SupplierRoute(svID,vID))
    def emptySupplierRoute(self):
        self.__supplier_routes.clear()
    def getNOHubs(self):
        return len(self.__newhubs)
    def getNOOpenedHubs(self):
        Newhubs=[]
        for i in range(self.getNOVehicleS()):
            if self.getVehicleS(i).getNOvisits()>0:
                if self.getVehicleS(i).getVisit(0).getID()[1]=="H":
                    if self.__problem.getHub(self.__problem.getHubINDEX(self.getVehicleS(i).getVisit(0).getID())).getExisting()==False:
                        if self.getVehicleS(i).getVisit(0).getID() not in Newhubs:
                            Newhubs.append(self.getVehicleS(i).getVisit(0).getID()) 
        return len(Newhubs)
    def getNewHubs(self, hindex) -> NewHubsSolution:
        if hindex in range(0, self.getNOHubs()):
            return self.__newhubs[hindex]
        sys.exit(print("Hub Solution 1 error"))   
    def setNewHubs(self, hID,vehicle):
        self.__newhubs_map[vehicle]=len(self.__newhubs)
        self.__newhubs.append(NewHubsSolution(hID))
    def getNewHubsINDEX(self, vehicle):
        return self.__newhubs_map[vehicle]
    def setHubVEHICLE(self,oldvehicle,newvehicle):
        self.__newhubs_map[newvehicle]=self.__newhubs_map.pop(oldvehicle)
    def removeHub(self, Hub):
        self.getNewHubs(Hub).setOPENED(False)
    def emptyHubs(self):
        self.__newhubs.clear()
    def ReadFromFile(self,filename):
        with open(str(filename)) as file_name:
            solution=json.load(file_name)
        vehicles_done=[]
        vehiclecount=1
        suproutecount=1
        for i in solution["solution"]["X"]:
            if solution["solution"]["X"][i][2] not in vehicles_done and solution["solution"]["X"][i][0][0]!="D" and solution["solution"]["X"][i][1][0]=="D": 
                vehicles_done.append(solution["solution"]["X"][i][2])
                self.setVehicleS("SV"+str(vehiclecount), solution["solution"]["vehicletype"][i])
                self.getVehicleS(vehiclecount-1).setVisit(solution["solution"]["X"][i][0],solution["solution"]["f"][i])
                self.getVehicleS(vehiclecount-1).setVisit(solution["solution"]["X"][i][1],solution["solution"]["f"][i])
                last=solution["solution"]["X"][i][1]
                for j in solution["solution"]["X"]:
                    if solution["solution"]["X"][i][2]==solution["solution"]["X"][j][2] and last==solution["solution"]["X"][j][0]:
                        if solution["solution"]["X"][j][1]==self.getVehicleS(vehiclecount-1).getVisit(0).getID(): break
                        self.getVehicleS(vehiclecount-1).setVisit(solution["solution"]["X"][j][1],solution["solution"]["f"][j])
                        self.getVehicleS(vehiclecount-1).getVisit(self.getVehicleS(vehiclecount-1).getNOvisits()-1).setQUANTITYCHANGE(self.getVehicleS(vehiclecount-1).getVisit(self.getVehicleS(vehiclecount-1).getNOvisits()-1).getQUANTITYCHANGE()-solution["solution"]["f"][j])
                        last=solution["solution"]["X"][j][1]
                vehiclecount+=1
            if solution["solution"]["X"][i][2] not in vehicles_done and solution["solution"]["X"][i][0][0]=="H" and solution["solution"]["X"][i][1][0]=="S": 
                vehicles_done.append(solution["solution"]["X"][i][2])
                self.setSupplierRoute("SV"+str(suproutecount), solution["solution"]["vehicletype"][i])
                self.getSupplierRoute(suproutecount-1).setVisit(solution["solution"]["X"][i][0],solution["solution"]["f"][i])
                self.getSupplierRoute(suproutecount-1).setVisit(solution["solution"]["X"][i][1],solution["solution"]["f"][i])
                last=solution["solution"]["X"][i][1]
                for j in solution["solution"]["X"]:
                    if solution["solution"]["X"][i][2]==solution["solution"]["X"][j][2] and last==solution["solution"]["X"][j][0]:
                        if solution["solution"]["X"][j][1]==self.getVehicleS(suproutecount-1).getVisit(0): break
                        self.getSupplierRoute(suproutecount-1).setVisit(solution["solution"]["X"][j][1],solution["solution"]["f"][j])
                        self.getSupplierRoute(suproutecount-1).getVisit(self.getSupplierRoute(suproutecount-1).getNOvisits()-1).setQUANTITYCHANGE(self.getSupplierRoute(suproutecount-1).getVisit(self.getSupplierRoute(suproutecount-1).getNOvisits()-1).getQUANTITYCHANGE()+solution["solution"]["f"][j])
                        last=solution["solution"]["X"][j][1]
                suproutecount+=1
    def getDistanceObjective(self):
        total_distance = 0
        for i in range(self.getNOVehicleS()):
            vehicle_distance = 0
            if self.getVehicleS(i).getNOvisits()<=1:
                vehicle_distance=0
            else:
                for j in range(self.getVehicleS(i).getNOvisits()-1):
                    vehicle_distance += self.getProblem().getDistance(self.getVehicleS(i).getVisit(j).getID(),
                                                                  self.getVehicleS(i).getVisit(j+1).getID())
                vehicle_distance += self.getProblem().getDistance(self.getVehicleS(i).getVisit(self.getVehicleS(i).getNOvisits()-1).getID(),
                                                              self.getVehicleS(i).getVisit(0).getID())
            total_distance += vehicle_distance
        for i in range(self.getNOSupplierRoutes()):
            vehicle_distance = 0
            if self.getSupplierRoute(i).getNOvisits()<=1:
                vehicle_distance==0
            else:
                for j in range(self.getSupplierRoute(i).getNOvisits()-1):
                    vehicle_distance += self.getProblem().getDistance(self.getSupplierRoute(i).getVisit(j).getID(),
                                                                  self.getSupplierRoute(i).getVisit(j+1).getID())
                vehicle_distance += self.getProblem().getDistance(self.getSupplierRoute(i).getVisit(self.getSupplierRoute(i).getNOvisits()-1).getID(),
                                                              self.getSupplierRoute(i).getVisit(0).getID())
            total_distance += vehicle_distance
        return total_distance 
    def getObjectiveFunction(self):
        return self.getDistanceObjective()
    def printSolution(self):
        print("Routes collecting products from suppliers:")
        for i in range(self.getNOSupplierRoutes()):
            if self.getSupplierRoute(i).getNOvisits()>=2:
                string=self.getSupplierRoute(i).getID()+": "
                for j in range(self.getSupplierRoute(i).getNOvisits()):
                    string+=self.getSupplierRoute(i).getVisit(j).getID()+"->"
                string+=self.getSupplierRoute(i).getVisit(0).getID()
                print(string)
        print("Routes delivering products to depots:")
        for i in range(self.getNOVehicleS()):
            if self.getVehicleS(i).getNOvisits()>=2:
                string=self.getVehicleS(i).getID()+": "
                for j in range(self.getVehicleS(i).getNOvisits()):
                    string+=self.getVehicleS(i).getVisit(j).getID()+"->"
                string+=self.getVehicleS(i).getVisit(0).getID()        
                print(string)
        Newhubs=[]
        for i in range(self.getNOVehicleS()):
            if self.getVehicleS(i).getNOvisits()>1:
                if self.getVehicleS(i).getVisit(0).getID()[1]=="H":
                    if self.__problem.getHub(self.__problem.getHubINDEX(self.getVehicleS(i).getVisit(0).getID())).getExisting()==False:
                        if self.getVehicleS(i).getVisit(0).getID() not in Newhubs:
                            Newhubs.append(self.getVehicleS(i).getVisit(0).getID()) 
        print("New Hubs Opened:")
        print(Newhubs)
        print("Objective:")
        print("Total Objective Function:", self.getObjectiveFunction())
        print("Distance Objective:", self.getDistanceObjective())
        print("Feasibility:")
        print("Total:", self.Feasibility())
        print("Demand and Supplier capacity violation:", self.demandandsupcap())
        print("Vehicle Capacity Violations:", self.Capacity_Violations_All_SupplierRoutes()+self.Capacity_Violations_All_Vehicles())
        print("Maximum New Hub Violation:", self.Max_New_Hub_Violations())
        print("Minimum throughpput of New Hub violation:", self.Min_Throuhghput_Violations_All_Vehicles())
        print("Maximum journey time violation:", self.time_constraint_all_supplier_route()+self.time_constraint_all_vehicles())
        print("Other", self.Supplier_capacity_and_hub_flow_violations())
    def CopyTo(self,solution):
        if solution.getNOVehicleS()!=0:
            solution.emptyVehicleS()
        if solution.getNOHubs()!=0:
            solution.emptyHubs()
        if solution.getNOSupplierRoutes()!=0:
            solution.emptySupplierRoute()
        for i in range(self.getNOVehicleS()):
            solution.setVehicleS(self.getVehicleS(i).getID(),self.getVehicleS(i).getVehicleID())
            for j in range(self.getVehicleS(i).getRouteLength()):
                solution.getVehicleS(i).setVisit((self.getVehicleS(i).getVisit(j).getID()))
                solution.getVehicleS(i).getVisit(j).setQUANTITYCHANGE(self.getVehicleS(i).getVisit(j).getQUANTITYCHANGE())
        for i in range(self.getNOHubs()):
            solution.setNewHubs(self.getNewHubs(i),list(self.__newhubs_map.keys())[list(self.__newhubs_map.values()).index(i)])
            solution.getNewHubs(i).setTHROUGHPUT(self.getNewHubs(i).getTHROUGHPUT())
            solution.getNewHubs(i).setOPENED(self.getNewHubs(i).getOPENED())
        for i in range(self.getNOSupplierRoutes()):
            solution.setSupplierRoute(self.getSupplierRoute(i).getID(),self.getSupplierRoute(i).getVehicleID())
            for j in range(self.getSupplierRoute(i).getRouteLength()):
                solution.getSupplierRoute(i).setVisit((self.getSupplierRoute(i).getVisit(j).getID()))
                solution.getSupplierRoute(i).getVisit(j).setQUANTITYCHANGE(self.getSupplierRoute(i).getVisit(j).getQUANTITYCHANGE())      
    def getSolution(self):
        routes=[]
        for i in range(self.getNOVehicleS()):
            routi=self.getVehicleS(i).getVisits()
            routes.append(routi)
        for i in range(self.getNOSupplierRoutes()):
            routi=self.getSupplierRoute(i).getVisits()
            routes.append(routi)
        return routes
    def Capacity_Violations_One_Vehicle(self, v_index):
        self.getVehicleS(v_index).setMaxLoad()
        current_load = self.getVehicleS(v_index).getMaxLoad()
        capacity = self.__problem.getVehicle(self.__problem.getVehicleINDEX(self.getVehicleS(v_index).getVehicleID())).getCAPACITY()
        return max(0, current_load-capacity)
    def Capacity_Violations_All_Vehicles(self):
        total = 0
        for i in range(self.getNOVehicleS()):
            total += self.Capacity_Violations_One_Vehicle( i)
        return total
    def Capacity_Violations_One_SupplierRoute(self, v_index):
        self.getSupplierRoute(v_index).setMaxLoad()
        current_load = self.getSupplierRoute(v_index).getMaxLoad()
        capacity = self.__problem.getVehicle(self.__problem.getVehicleINDEX(self.getSupplierRoute(v_index).getVehicleID())).getCAPACITY()
        return max(0, current_load-capacity)
    def Capacity_Violations_All_SupplierRoutes(self):
        total = 0
        for i in range(self.getNOSupplierRoutes()):
            total += self.Capacity_Violations_One_SupplierRoute( i)
        return total
    def Max_New_Hub_Violations(self):
        Newhubs=[]
        for i in range(self.getNOVehicleS()):
            if self.getVehicleS(i).getVisit(0).getID()[1]=="H":
                if self.__problem.getHub(self.__problem.getHubINDEX(self.getVehicleS(i).getVisit(0).getID())).getExisting()==False:
                    if self.getVehicleS(i).getVisit(0).getID() not in Newhubs:
                        Newhubs.append(self.getVehicleS(i).getVisit(0).getID()) 
        return max(0,len(Newhubs)-self.__problem.getMaxNewHubs())
    def Min_Throughput_Violations_One_Vehicle(self,v_index):
        self.getVehicleS(v_index).setMaxLoad()
        current_load = self.getVehicleS(v_index).getMaxLoad()
        min_throughput=self.__problem.getMinThroughput()
        return max(0,min_throughput-current_load)
    def Min_Throuhghput_Violations_All_Vehicles(self):
        Hub_throughput={}
        for i in range(self.getNOVehicleS()):
            if self.getVehicleS(i).getVisit(0).getID()[1]=="H":
                if self.__problem.getHub(self.__problem.getHubINDEX(self.getVehicleS(i).getVisit(0).getID())).getExisting()==False:
                    self.getVehicleS(i).setMaxLoad()
                    if self.getVehicleS(i).getVisit(0).getID() not in Hub_throughput:
                        Hub_throughput[self.getVehicleS(i).getVisit(0).getID()]=self.getVehicleS(i).getMaxLoad()
                    else:
                        Hub_throughput[self.getVehicleS(i).getVisit(0).getID()]+=self.getVehicleS(i).getMaxLoad()
        total=0
        for i in Hub_throughput:
            total+=max(0,self.__problem.getMinThroughput()-Hub_throughput[i])
        return total 
    def Supplier_capacity_and_hub_flow_violations(self):
        hub_info={}
        for i in range(self.getNOVehicleS()):
            if self.getVehicleS(i).getVisit(0).getID() not in hub_info:
                hub_info[self.getVehicleS(i).getVisit(0).getID()]={"depotroutes":[i],"qout":self.getVehicleS(i).getMaxLoad(),"supplierroutes":[],"qin":0}
            else:
                hub_info[self.getVehicleS(i).getVisit(0).getID()]["depotroutes"].append(i)
                hub_info[self.getVehicleS(i).getVisit(0).getID()]["qout"]+=self.getVehicleS(i).getMaxLoad()
        for i in range(self.getNOSupplierRoutes()):
            if self.getSupplierRoute(i).getVisit(0).getID() in hub_info:
                hub_info[self.getSupplierRoute(i).getVisit(0).getID()]["supplierroutes"].append(i)
                hub_info[self.getSupplierRoute(i).getVisit(0).getID()]["qin"]+=self.getSupplierRoute(i).getMaxLoad()
        total=0
        for i in hub_info:
            hub_excess=hub_info[i]["qin"]-hub_info[i]["qout"]
            if hub_excess==0:
                for j in hub_info[i]["supplierroutes"]:
                    for k in range(1,self.getSupplierRoute(j).getNOvisits()):
                        total+=max(0,self.getSupplierRoute(j).getVisit(k).getQUANTITYCHANGE()-self.__problem.getSupplierCapacity(self.__problem.getSupplierCapacityINDEX(self.getSupplierRoute(j).getVisit(k).getID(), "PT1")).getQUANTITY())
            elif hub_excess>0:
                total_cap=0
                if len(hub_info[i]["supplierroutes"])==1:
                    total+=max(1,hub_info[i]["qout"])
                for j in hub_info[i]["supplierroutes"]:
                    for k in range(1,self.getSupplierRoute(j).getNOvisits()): 
                        total_cap+=self.__problem.getSupplierCapacity(self.__problem.getSupplierCapacityINDEX(self.getSupplierRoute(j).getVisit(k).getID(), "PT1")).getQUANTITY()
                total+=max(0,hub_info[i]["qin"]-total_cap)
                for j in hub_info[i]["supplierroutes"]:
                    for k in range(1,self.getSupplierRoute(j).getNOvisits()): 
                        x=min(self.getSupplierRoute(j).getVisit(k).getQUANTITYCHANGE(),hub_excess)
                        self.getSupplierRoute(j).getVisit(k).setQUANTITYCHANGE(self.getSupplierRoute(j).getVisit(k).getQUANTITYCHANGE()-x)
                        hub_excess-=x
                        if hub_excess<=0: break
            elif hub_excess<0:
                total_cap=0
                if len(hub_info[i]["supplierroutes"])==1:
                    total+=max(1,hub_info[i]["qout"])
                for j in hub_info[i]["supplierroutes"]:
                    for k in range(1,self.getSupplierRoute(j).getNOvisits()): 
                        total_cap+=self.__problem.getSupplierCapacity(self.__problem.getSupplierCapacityINDEX(self.getSupplierRoute(j).getVisit(k).getID(), "PT1")).getQUANTITY()
                total+=max(0,hub_info[i]["qin"]-total_cap)
                for j in hub_info[i]["supplierroutes"]:
                    for k in range(1,self.getSupplierRoute(j).getNOvisits()): 
                        capacity=self.__problem.getSupplierCapacity(self.__problem.getSupplierCapacityINDEX(self.getSupplierRoute(j).getVisit(k).getID(), "PT1")).getQUANTITY()
                        x=min(capacity-self.getSupplierRoute(j).getVisit(k).getQUANTITYCHANGE(),hub_excess)
                        self.getSupplierRoute(j).getVisit(k).setQUANTITYCHANGE(self.getSupplierRoute(j).getVisit(k).getQUANTITYCHANGE()+x)
                        hub_excess+=x
                        if hub_excess>=0: break
        return total
    def demandandsupcap(self):
        suppliers=[]
        for i in range(self.__problem.getNOsuppliers()):
            suppliers.append(self.__problem.getSupplierCapacity(self.__problem.getSupplierCapacityINDEX("S"+str(i+1), "PT1")).getQUANTITY())
        depots=[]
        for i in range(self.__problem.getNODepot()):
            depots.append(self.__problem.getDemand(self.__problem.getDemandINDEX("D"+str(i+1), "PT1")).getQUANTITY())
        hubs=[0 for i in range(self.__problem.getNOHubs())]
        for i in range(self.getNOVehicleS()):
            vc=self.__problem.getVehicle(self.__problem.getVehicleINDEX(self.getVehicleS(i).getVehicleID())).getCAPACITY()
            for j in range(1,self.getVehicleS(i).getNOvisits()):
                if depots[self.__problem.getDepotINDEX(self.getVehicleS(i).getVisit(j).getID())]>0:
                    change=min(vc,depots[self.__problem.getDepotINDEX(self.getVehicleS(i).getVisit(j).getID())])
                    depots[self.__problem.getDepotINDEX(self.getVehicleS(i).getVisit(j).getID())]-=change
                    vc-=change
                    if self.getVehicleS(i).getVisit(0).getID()[1]=="H":
                        hubs[self.__problem.getHubINDEX(self.getVehicleS(i).getVisit(0).getID())]+=change
                    if self.getVehicleS(i).getVisit(0).getID()[0]=="S":
                        suppliers[self.__problem.getSupplierINDEX(self.getVehicleS(i).getVisit(0).getID())]-=change
                    self.getVehicleS(i).getVisit(j).setQUANTITYCHANGE(change)
        for i in range(self.getNOSupplierRoutes()):
            vc=self.__problem.getVehicle(self.__problem.getVehicleINDEX(self.getSupplierRoute(i).getVehicleID())).getCAPACITY()
            for j in range(1,self.getSupplierRoute(i).getNOvisits()):
                if suppliers[self.__problem.getSupplierINDEX(self.getSupplierRoute(i).getVisit(j).getID())]>0:
                    change=min(vc,suppliers[self.__problem.getSupplierINDEX(self.getSupplierRoute(i).getVisit(j).getID())],hubs[self.__problem.getHubINDEX(self.getSupplierRoute(i).getVisit(0).getID())])
                    vc-=change
                    hubs[self.__problem.getHubINDEX(self.getSupplierRoute(i).getVisit(0).getID())]-=change
                    self.getSupplierRoute(i).getVisit(j).setQUANTITYCHANGE(change)
                    suppliers[self.__problem.getSupplierINDEX(self.getSupplierRoute(i).getVisit(j).getID())]-=change
        total=0
        for i in depots:
            if i>0:
                total+=i
        for i in hubs:
            if i>0:
                total+=i
        for i in range(len(suppliers)):
            if suppliers[i]<0:
                total-=suppliers[i]
        return total         
    def time_constraint_one_vehicle(self,v_index):
        vehicle_time = 0
        if self.getVehicleS(v_index).getNOvisits()<=1:
            vehicle_time=0
        else:
            for j in range(self.getVehicleS(v_index).getNOvisits()-1):
                vehicle_time += self.getProblem().getTime(self.getVehicleS(v_index).getVisit(j).getID(),
                                                              self.getVehicleS(v_index).getVisit(j+1).getID())
            vehicle_time += self.getProblem().getTime(self.getVehicleS(v_index).getVisit(self.getVehicleS(v_index).getNOvisits()-1).getID(),
                                                          self.getVehicleS(v_index).getVisit(0).getID())
        return vehicle_time
    def time_constraint_all_vehicles(self):
        total = 0
        for i in range(self.getNOVehicleS()):
            if max(0,self.time_constraint_one_vehicle(i)-self.__problem.getMaxTime()) > total:
                total = max(0,self.time_constraint_one_vehicle(i)-self.__problem.getMaxTime())
        return total
    def time_constraint_one_supplier_route(self,v_index):
        vehicle_time = 0
        if self.getSupplierRoute(v_index).getNOvisits()<=1:
            vehicle_time=0
        else:
            for j in range(self.getSupplierRoute(v_index).getNOvisits()-1):
                vehicle_time += self.getProblem().getTime(self.getSupplierRoute(v_index).getVisit(j).getID(),
                                                              self.getSupplierRoute(v_index).getVisit(j+1).getID())
            vehicle_time += self.getProblem().getTime(self.getSupplierRoute(v_index).getVisit(self.getSupplierRoute(v_index).getNOvisits()-1).getID(),
                                                self.getSupplierRoute(v_index).getVisit(0).getID())
        return vehicle_time
    def time_constraint_all_supplier_route(self):
        total = 0
        for i in range(self.getNOSupplierRoutes()):
            total += max(0,self.time_constraint_one_supplier_route(i)-self.__problem.getMaxTime())
        return total
    def Feasibility(self):
        total=10000*self.demandandsupcap()+(self.Capacity_Violations_All_SupplierRoutes()+self.Capacity_Violations_All_Vehicles()+self.Max_New_Hub_Violations()+self.Min_Throuhghput_Violations_All_Vehicles())+self.time_constraint_all_supplier_route()+self.time_constraint_all_vehicles()+10*self.Supplier_capacity_and_hub_flow_violations()
        return total
    def capconstraint(self,vehicle):
        excess_visits=[]
        while self.getVehicleS(vehicle).getMaxLoad()>self.__problem.getVehicle(self.__problem.getVehicleINDEX(self.getVehicleS(vehicle).getVehicleID())).getCAPACITY():
            excess_visits.append(self.getVehicleS(vehicle).getVisit(self.getVehicleS(vehicle).getNOvisits()-1))
            self.getVehicleS(vehicle).removeVisit(self.getVehicleS(vehicle).getVisit(self.getVehicleS(vehicle).getNOvisits()-1))
            self.getVehicleS(vehicle).setMaxLoad()
        while len(excess_visits)>=1:
            self.setVehicleS("SV"+str(self.getNOVehicleS()+1), self.getVehicleS(vehicle).getVehicleID())
            if self.getVehicleS(vehicle).getVisit(0).getID()[1]=="H":
                if self.__problem.getHub(self.__problem.getHubINDEX(self.getVehicleS(vehicle).getVisit(0).getID())).getExisting()==False:
                        self.setNewHubs(self.getVehicleS(vehicle).getVisit(0).getID(), self.getNOVehicleS()-1)
            self.getVehicleS(self.getNOVehicleS()-1).setVisit(self.getVehicleS(vehicle).getVisit(0).getID())
            while self.getVehicleS(self.getNOVehicleS()-1).getMaxLoad()<self.__problem.getVehicle(self.__problem.getVehicleINDEX(self.getVehicleS(self.getNOVehicleS()-1).getVehicleID())).getCAPACITY() and len(excess_visits)!=0:
                self.getVehicleS(self.getNOVehicleS()-1).setVisit(excess_visits[0].getID(),excess_visits[0].getQUANTITYCHANGE())
                excess_visits.remove(excess_visits[0])
                self.getVehicleS(self.getNOVehicleS()-1).setMaxLoad()
            if self.getVehicleS(vehicle).getVisit(0).getID()[1]=="H":
                if self.__problem.getHub(self.__problem.getHubINDEX(self.getVehicleS(vehicle).getVisit(0).getID())).getExisting()==False:
                    self.getNewHubs(self.getNewHubsINDEX(self.getNOVehicleS()-1)).setTHROUGHPUT(self.getVehicleS(self.getNOVehicleS()-1).setMaxLoad())
   