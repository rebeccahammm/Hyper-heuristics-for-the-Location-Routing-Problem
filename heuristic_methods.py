#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:14:15 2021

@author: hammr
"""
import solution_class as sc
import random
class heuristic_methods():
    def __init__(self,problem):
        self.__problem=problem
    def SwapInsideVehicleHeuristic(self,solution):
        vehicleIndex=random.randint(0, solution.getNOVehicleS()-1)
        if solution.getVehicleS(vehicleIndex).getNOvisits() < 3:
            return
        index_one=random.randint(1,solution.getVehicleS(vehicleIndex).getNOvisits()-1)
        index_two=random.randint(1,solution.getVehicleS(vehicleIndex).getNOvisits()-2)
        if index_one == index_two:
            index_two = solution.getVehicleS(vehicleIndex).getNOvisits()-1
        visit1=solution.getVehicleS(vehicleIndex).getVisit(index_one)
        visit2=solution.getVehicleS(vehicleIndex).getVisit(index_two)
        solution.getVehicleS(vehicleIndex).removeVisit(visit1)
        solution.getVehicleS(vehicleIndex).removeVisit(visit2)
        solution.getVehicleS(vehicleIndex).insertVisit(index_one, visit2)
        solution.getVehicleS(vehicleIndex).insertVisit(index_two, visit1)
    def InsertDepotHeuristic(self,solution):
        vehicleIndex=random.randint(0, solution.getNOVehicleS()-1)
        position=random.randint(1, solution.getVehicleS(vehicleIndex).getNOvisits())
        visitID=self.__problem.getDepot(random.randint(0, self.__problem.getNODepot()-1)).getID()
        solution.getVehicleS(vehicleIndex).insertVisit(position,sc.Visit(visitID,self.__problem.getDemand(self.__problem.getDemandINDEX(visitID, "PT1")).getQUANTITY()))
    def RemoveDepot(self,solution):
        vehicleIndex=random.randint(0, solution.getNOVehicleS()-1)
        if solution.getVehicleS(vehicleIndex).getNOvisits() < 2:
            return
        position=random.randint(1, solution.getVehicleS(vehicleIndex).getNOvisits()-1)
        visit=solution.getVehicleS(vehicleIndex).getVisit(position)
        solution.getVehicleS(vehicleIndex).removeVisit(visit)
    def SwapBetweenVehicles(self,solution):
        vehicleIndex1=random.randint(0, solution.getNOVehicleS()-1)
        vehicleIndex2=random.randint(0, solution.getNOVehicleS()-2)
        if vehicleIndex1 == vehicleIndex2:
            vehicleIndex2 = solution.getNOVehicleS()-1
        if solution.getVehicleS(vehicleIndex1).getNOvisits() < 2:
            return
        if solution.getVehicleS(vehicleIndex2).getNOvisits() < 2:
            return
        index_one=random.randint(1,solution.getVehicleS(vehicleIndex1).getNOvisits()-1)
        index_two=random.randint(1,solution.getVehicleS(vehicleIndex2).getNOvisits()-1)
        visit1=solution.getVehicleS(vehicleIndex1).getVisit(index_one)
        visit2=solution.getVehicleS(vehicleIndex2).getVisit(index_two)
        solution.getVehicleS(vehicleIndex1).removeVisit(visit1)
        solution.getVehicleS(vehicleIndex2).removeVisit(visit2)
        solution.getVehicleS(vehicleIndex1).insertVisit(index_one, visit2)
        solution.getVehicleS(vehicleIndex2).insertVisit(index_two, visit1) 
    def InsertBetweenVehicles(self,solution):
        vehicleIndex1=random.randint(0, solution.getNOVehicleS()-1)
        vehicleIndex2=random.randint(0, solution.getNOVehicleS()-2)
        if vehicleIndex1 == vehicleIndex2:
            vehicleIndex2 = solution.getNOVehicleS()-1
        if solution.getVehicleS(vehicleIndex1).getNOvisits() < 2:
            return
        index_one=random.randint(1,solution.getVehicleS(vehicleIndex1).getNOvisits()-1)
        index_two=random.randint(1,solution.getVehicleS(vehicleIndex2).getNOvisits())
        visit1=solution.getVehicleS(vehicleIndex1).getVisit(index_one)
        solution.getVehicleS(vehicleIndex1).removeVisit(visit1)
        solution.getVehicleS(vehicleIndex2).insertVisit(index_two, visit1)
    def SwapHubs(self,solution):
        vehicleIndex1=random.randint(0, solution.getNOVehicleS()-1)
        vehicleIndex2=random.randint(0, solution.getNOVehicleS()-2)
        if vehicleIndex1 == vehicleIndex2:
            vehicleIndex2 = solution.getNOVehicleS()-1
        visit1=solution.getVehicleS(vehicleIndex1).getVisit(0)
        visit2=solution.getVehicleS(vehicleIndex2).getVisit(0)
        solution.getVehicleS(vehicleIndex1).removeVisit(visit1)
        solution.getVehicleS(vehicleIndex2).removeVisit(visit2)
        solution.getVehicleS(vehicleIndex1).insertVisit(0, visit2)
        solution.getVehicleS(vehicleIndex2).insertVisit(0, visit1)
    def InterchangeHubs(self,solution):
        vehicleIndex1=random.randint(0, solution.getNOVehicleS()-1)
        newhub=self.__problem.getHub(random.randint(0, self.__problem.getNOHubs()-1)).getID()
        visit1=solution.getVehicleS(vehicleIndex1).getVisit(0)
        othervehicles=[]
        for i in range(solution.getNOVehicleS()):
            if solution.getVehicleS(i).getVisit(0).getID()==visit1.getID() and i!=vehicleIndex1:
                othervehicles.append(i)
        suppliervehicles=[]
        for i in range(solution.getNOSupplierRoutes()):
            if solution.getSupplierRoute(i).getVisit(0).getID()==visit1.getID():
                suppliervehicles.append(i)
        solution.getVehicleS(vehicleIndex1).removeVisit(visit1)
        solution.getVehicleS(vehicleIndex1).insertVisit(0, sc.Visit(newhub))
        for i in othervehicles:
            solution.getVehicleS(i).removeVisit(solution.getVehicleS(i).getVisit(0))
            solution.getVehicleS(i).insertVisit(0, sc.Visit(newhub))
        for i in suppliervehicles:
            solution.getSupplierRoute(i).removeVisit(solution.getSupplierRoute(i).getVisit(0))
            solution.getSupplierRoute(i).insertVisit(0,sc.Visit(newhub))
    def DirectDelivery(self,solution):
        vehicleIndex1=random.randint(0, solution.getNOVehicleS()-1)
        newhub=self.__problem.getSupplier(random.randint(0, self.__problem.getNOsuppliers()-1)).getID()
        visit1=solution.getVehicleS(vehicleIndex1).getVisit(0)
        othervehicles=[]
        for i in range(solution.getNOVehicleS()):
            if solution.getVehicleS(i).getVisit(0).getID()==visit1.getID() and i!=vehicleIndex1:
                othervehicles.append(i)
        suppliervehicles=[]
        for i in range(solution.getNOSupplierRoutes()):
            if solution.getSupplierRoute(i).getVisit(0).getID()==visit1.getID():
                suppliervehicles.append(i)
        solution.getVehicleS(vehicleIndex1).removeVisit(visit1)
        solution.getVehicleS(vehicleIndex1).insertVisit(0, sc.Visit(newhub))
        for i in othervehicles:
            solution.getVehicleS(i).removeVisit(solution.getVehicleS(i).getVisit(0))
            solution.getVehicleS(i).insertVisit(0, sc.Visit(newhub))
        for i in suppliervehicles:
            while solution.getSupplierRoute(i).getNOvisits()>1:
                solution.getSupplierRoute(i).removeVisit(solution.getSupplierRoute(i).getVisit(1))
    def SwapInsideSupplierRouteHeuristic(self,solution):
            vehicleIndex=random.randint(0, solution.getNOSupplierRoutes()-1)
            if solution.getSupplierRoute(vehicleIndex).getNOvisits() < 3:
                return
            index_one=random.randint(1,solution.getSupplierRoute(vehicleIndex).getNOvisits()-1)
            index_two=random.randint(1,solution.getSupplierRoute(vehicleIndex).getNOvisits()-2)
            if index_one == index_two:
                index_two = solution.getSuppplierRoute(vehicleIndex).getNOvisits()-1
            visit1=solution.getSupplierRoute(vehicleIndex).getVisit(index_one)
            visit2=solution.getSupplierRoute(vehicleIndex).getVisit(index_two)
            solution.getSupplierRoute(vehicleIndex).removeVisit(visit1)
            solution.getSupplierRoute(vehicleIndex).removeVisit(visit2)
            solution.getSupplierRoute(vehicleIndex).insertVisit(index_one, visit2)
            solution.getSupplierRoute(vehicleIndex).insertVisit(index_two, visit1)
    def SwapSuppliers(self,solution):
        if solution.getNOSupplierRoutes()>1:
            vehicleIndex1=random.randint(0, solution.getNOSupplierRoutes()-1)
            vehicleIndex2=random.randint(0, solution.getNOSupplierRoutes()-2)
            if vehicleIndex1 == vehicleIndex2:
                vehicleIndex2 = solution.getNOSupplierRoutes()-1
            if solution.getSupplierRoute(vehicleIndex1).getNOvisits() < 2:
                return
            if solution.getSupplierRoute(vehicleIndex2).getNOvisits() < 2:
                return
            index_one=random.randint(1,solution.getSupplierRoute(vehicleIndex1).getNOvisits()-1)
            index_two=random.randint(1,solution.getSupplierRoute(vehicleIndex2).getNOvisits()-1)
            visit1=solution.getSupplierRoute(vehicleIndex1).getVisit(index_one)
            visit2=solution.getSupplierRoute(vehicleIndex2).getVisit(index_two)
            solution.getSupplierRoute(vehicleIndex1).removeVisit(visit1)
            solution.getSupplierRoute(vehicleIndex2).removeVisit(visit2)
            solution.getSupplierRoute(vehicleIndex1).insertVisit(index_one, visit2)
            solution.getSupplierRoute(vehicleIndex2).insertVisit(index_two, visit1)
    def InsertSupplier(self,solution):
        if solution.getNOSupplierRoutes()>0:
            vehicleIndex=random.randint(0, solution.getNOSupplierRoutes()-1)
            position=random.randint(1, solution.getSupplierRoute(vehicleIndex).getNOvisits())
            visitID=self.__problem.getSupplier(random.randint(0, self.__problem.getNOsuppliers()-1)).getID()
            solution.getSupplierRoute(vehicleIndex).insertVisit(position,sc.Visit(visitID,self.__problem.getSupplierCapacity(self.__problem.getSupplierCapacityINDEX(visitID, "PT1")).getQUANTITY()))
    def RemoveSupplier(self,solution):
        if solution.getNOSupplierRoutes()>0:
            vehicleIndex=random.randint(0, solution.getNOSupplierRoutes()-1)
            if solution.getSupplierRoute(vehicleIndex).getNOvisits() < 2:
                return
            position=random.randint(1, solution.getSupplierRoute(vehicleIndex).getNOvisits()-1)
            visit=solution.getSupplierRoute(vehicleIndex).getVisit(position)
            solution.getSupplierRoute(vehicleIndex).removeVisit(visit)
    def InsertHub(self,solution):
        vehicleIndex1=random.randint(0, solution.getNOVehicleS()-1)
        newhub=self.__problem.getHub(random.randint(0, self.__problem.getNOHubs()-1)).getID()
        visit1=solution.getVehicleS(vehicleIndex1).getVisit(0)
        othervehicles=[]
        for i in range(solution.getNOVehicleS()):
            if solution.getVehicleS(i).getVisit(0).getID()==visit1.getID() and i!=vehicleIndex1:
                othervehicles.append(i)
        suppliervehicles=[]
        for i in range(solution.getNOSupplierRoutes()):
            if solution.getSupplierRoute(i).getVisit(0).getID()==visit1.getID():
                suppliervehicles.append(i)
        solution.getVehicleS(vehicleIndex1).removeVisit(visit1)
        solution.getVehicleS(vehicleIndex1).insertVisit(0, sc.Visit(newhub))
        if len(othervehicles)>0:
            VID=random.randint(1,self.__problem.getNOVehicles())
            solution.setSupplierRoute("SSV"+str(solution.getNOSupplierRoutes()),"V"+str(VID))
            solution.getSupplierRoute(solution.getNOSupplierRoutes()-1).setVisit(sc.Visit(newhub).getID())
            j=random.randint(0,self.__problem.getNOsuppliers()-1)
            solution.getSupplierRoute(solution.getNOSupplierRoutes()-1).setVisit(sc.Visit(self.__problem.getSupplier(j).getID()).getID())
        elif len(suppliervehicles)>0:
            i=random.choice(suppliervehicles)
            solution.getSupplierRoute(i).removeVisit(solution.getSupplierRoute(i).getVisit(0))
            solution.getSupplierRoute(i).insertVisit(0,sc.Visit(newhub))
        else:
            VID=random.randint(1,self.__problem.getNOVehicles())
            solution.setSupplierRoute("SSV"+str(solution.getNOSupplierRoutes()),"V"+str(VID))
            solution.getSupplierRoute(solution.getNOSupplierRoutes()-1).setVisit(sc.Visit(newhub).getID())
            j=random.randint(0,self.__problem.getNOsuppliers()-1)
            solution.getSupplierRoute(solution.getNOSupplierRoutes()-1).setVisit(sc.Visit(self.__problem.getSupplier(j).getID()).getID())
    def InsertSupplierBetweenVehicles(self,solution):
        if solution.getNOSupplierRoutes()>1:
            vehicleIndex1=random.randint(0, solution.getNOSupplierRoutes()-1)
            vehicleIndex2=random.randint(0, solution.getNOSupplierRoutes()-2)
            if vehicleIndex1 == vehicleIndex2:
                vehicleIndex2 = solution.getNOSupplierRoutes()-1
            if solution.getSupplierRoute(vehicleIndex1).getNOvisits() < 2:
                return
            index_one=random.randint(1,solution.getSupplierRoute(vehicleIndex1).getNOvisits()-1)
            index_two=random.randint(1,solution.getSupplierRoute(vehicleIndex2).getNOvisits())
            visit1=solution.getSupplierRoute(vehicleIndex1).getVisit(index_one)
            solution.getSupplierRoute(vehicleIndex1).removeVisit(visit1)
            solution.getSupplierRoute(vehicleIndex2).insertVisit(index_two, visit1)
    def SwapHubsforSuppliers(self,solution):
        if solution.getNOSupplierRoutes()>1:
            vehicleIndex1=random.randint(0, solution.getNOSupplierRoutes()-1)
            vehicleIndex2=random.randint(0, solution.getNOSupplierRoutes()-2)
            if vehicleIndex1 == vehicleIndex2:
                vehicleIndex2 = solution.getNOSupplierRoutes()-1
            visit1=solution.getSupplierRoute(vehicleIndex1).getVisit(0)
            visit2=solution.getSupplierRoute(vehicleIndex2).getVisit(0)
            solution.getSupplierRoute(vehicleIndex1).removeVisit(visit1)
            solution.getSupplierRoute(vehicleIndex2).removeVisit(visit2)
            solution.getSupplierRoute(vehicleIndex1).insertVisit(0, visit2)
            solution.getSupplierRoute(vehicleIndex2).insertVisit(0, visit1)
    def ApplyHeuristic(self,h,solution):
        if h==0:
            self.SwapInsideVehicleHeuristic(solution)
        if h==1:
            self.InsertDepotHeuristic(solution)
        if h==2:
            self.SwapBetweenVehicles(solution)
        if h==3:
            self.InsertBetweenVehicles(solution)
        if h==4:
            self.SwapHubs(solution)
        if h==5:
            self.InterchangeHubs(solution)
        if h==6:
            self.SwapSuppliers(solution)
        if h==7:
            self.InsertSupplier(solution)
        if h==8:
            self.InsertSupplierBetweenVehicles(solution)
        if h==9:
            self.SwapHubsforSuppliers(solution)
        if h==10:
            self.RemoveDepot(solution)
        if h==11:
            self.RemoveSupplier(solution)
        if h==12:
            self.DirectDelivery(solution)
        if h==13:
            self.InsertHub(solution)
        if h==14:
            self.SwapInsideSupplierRouteHeuristic
            
  
    
        
                                