#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 13:53:04 2021

@author: hammr
"""
import json
import sys
import numpy as np

#Class for suppliers
class Supplier():
    def __init__(self,ID="",name="",latitude=0.0,longitude=0.0,index=0):
        self.__id=ID
        self.__name=name
        self.__latitude=latitude
        self.__longitude=longitude
        self.__index=index
    def getID(self):
        return self.__id
    def setID(self,ID):
        self.__id=ID
    def getNAME(self):
        return self.__name
    def setNAME(self,name):
        self.__name=name
    def getLATITUDE(self):
        return self.__latitude
    def setLATITUDE(self,latitude):
        self.__latitude=latitude
    def getLONGITUDE(self):
        return self.__longitude
    def setLONGITUDE(self,longitude):
        self.__longitude=longitude
    def getINDEX(self):
        return self.__index
    def setINDEX(self,index):
        self.__index=index
    def __str__(self):
        return "ID: "+str(self.getID())
  
#class for depots
class Depot():
    def __init__(self,ID="",name="",latitude=0.0,longitude=0.0,index=0):
        self.__id=ID
        self.__name=name
        self.__latitude=latitude
        self.__longitude=longitude
        self.__index=index
    def getID(self):
        return self.__id
    def setID(self,ID):
        self.__id=ID
    def getNAME(self):
        return self.__name
    def setNAME(self,name):
        self.__name=name
    def getLATITUDE(self):
        return self.__latitude
    def setLATITUDE(self,latitude):
        self.__latitude=latitude
    def getLONGITUDE(self):
        return self.__longitude
    def setLONGITUDE(self,longitude):
        self.__longitude=longitude
    def getINDEX(self):
        return self.__index
    def setINDEX(self,index):
        self.__index=index
    def __str__(self):
        return "ID: "+str(self.getID())

#class for all hubs 
class Hub():
    def __init__(self,ID="",name="",latitude=0.0,longitude=0.0,index=0,
                 exists=True):
        self.__id=ID
        self.__name=name
        self.__latitude=latitude
        self.__longitude=longitude
        self.__index=index
        self.__exists=exists
    def getID(self):
        return self.__id
    def setID(self,ID):
        self.__id=ID
    def getNAME(self):
        return self.__name
    def setNAME(self,name):
        self.__name=name
    def getLATITUDE(self):
        return self.__latitude
    def setLATITUDE(self,latitude):
        self.__latitude=latitude
    def getLONGITUDE(self):
        return self.__longitude
    def setLONGITUDE(self,longitude):
        self.__longitude=longitude
    def getINDEX(self):
        return self.__index
    def setINDEX(self,index):
        self.__index=index
    def getExisting(self):
        return self.__exists
    def setExsisting(self,exists):
        self.__exists=exists
    def __str__(self):
        return "ID: "+str(self.getID())
    
#Class for products types
class ProductType():
    def __init__(self,ID="",name=""):
        self.__id=ID
        self.__name=name
    def getID(self):
        return self.__id
    def setID(self,ID):
        self.__ID=ID
    def getNAME(self):
        return self.__name
    def setNAME(self,name):
        self.__name=name
    def __str__(self):
        return "ID"+str(self.getID())

#Class for supplier capacities
class SupplierCapacity():
    def __init__(self,ID="",product="",supplier="",quantity=0):
        self.__ID=ID
        self.__product=product
        self.__supplier=supplier
        self.__quantity=quantity
    def getID(self):
        return self.__ID
    def setID(self,ID):
        self.__ID=ID
    def getPRODUCT(self):
        return self.__product
    def setPRODUCT(self,product):
        self.__product=product
    def getSUPPLIER(self):
        return self.__supplier
    def setSUPPLIER(self,supplier):
        self.__supplier=supplier
    def getQUANTITY(self):
        return self.__quantity
    def setQUANTITY(self,quantity):
        self.__quantity=quantity
    def __str__(self):
        return "ID"+str(self.getID())

#Class for demands
class Demand():
    def __init__(self,ID="",product="",depot="",quantity=""):
        self.__id=ID
        self.__product=product
        self.__depot=depot
        self.__quantity=quantity
    def getID(self):
        return self.__id
    def setID(self,ID):
        self.__id=ID
    def getPRODUCT(self):
        return self.__product 
    def setPRODUCT(self,product):
        self.__product=product
    def getDEPOT(self):
        return self.__depot
    def setDEPOT(self,depot):
        self.__depot=depot
    def getQUANTITY(self):
        return self.__quantity
    def setQUANTITY(self,quantity):
        self.__quantity=quantity
    def __str__(self):
        return "ID"+str(self.getID())

#Class for vehicle types
class Vehicle():
    def __init__(self,ID="",name="",capacity=0.0,quantity=0):
        self.__id=ID
        self.__name=name
        self.__capacity=capacity
        self.__quantity=quantity
    def getID(self):
        return self.__id
    def setID(self,ID):
        self.__id=ID
    def getNAME(self):
        return self.__name
    def setNAME(self,name):
        self.__name=name
    def getCAPACITY(self):
        return self.__capacity
    def setCAPACITY(self,capacity):
        self.__capacity=capacity
    def getQUANTITY(self):
        return self.__quantity
    def setQUANTITY(self,quantity):
        self.__quantity=quantity
    def __str__(self):
        return "ID: "+str(self.getID())
 
#Class for whole problem
class Problem():
    def __init__(self,instance_file="instance.json"):
        self.__file_name=instance_file
        self.__suppliers=[]
        self.__suppliers_map={}
        self.__depots=[]
        self.__depots_map={}
        self.__hubs=[]
        self.__hubs_map={}
        self.__producttypes=[]
        self.__producttypes_map={}
        self.__suppliercapacities_map={}
        self.__suppliercapacities=[]
        self.__demands=[]
        self.__demands_map={}
        self.__vehicles=[]
        self.__vehicles_map={}
        self.__distances=[]
        self.__times=[]
        self.__max_new_hubs=0
        self.__min_throughput=0
        self.__max_time=0
    def getMaxNewHubs(self):
        return self.__max_new_hubs
    def setMaxNewHubs(self,Max_value):
        self.__max_new_hubs=Max_value
    def getMaxTime(self):
        return self.__max_time
    def setMaxTime(self,mt):
        self.__max_time=mt
    def getMinThroughput(self):
        return self.__min_throughput
    def setMinThroughput(self, min_throughput):
        self.__min_throughput=min_throughput
    def getVehicle(self,vindex)->Vehicle:
        if vindex in range(0,self.getNOVehicles()):
            return self.__vehicles[vindex]
        sys.exit(print("Vechicle 1 Error"))
    def setVehicle(self,vID):
        self.__vehicles_map[vID]=len(self.__vehicles)
        self.__vehicles.append(Vehicle(vID))
    def getVehicleINDEX(self,vID):
        return self.__vehicles_map[vID]
    def getFile_name(self):
        return self.__file_name
    def getNOsuppliers(self):
        return len(self.__suppliers)
    def getSupplier(self,sindex)->Supplier:
        if sindex in range(0,self.getNOsuppliers()):
            return self.__suppliers[sindex]
        sys.exit(print("Supplier 1 error"))
    def setSupplier(self,sID):
        self.__suppliers_map[sID]=len(self.__suppliers)
        self.__suppliers.append(Supplier(sID))
    def getSupplierINDEX(self,sID):
        return self.__suppliers_map[sID]
    def getNODepot(self):
        return len(self.__depots)
    def getDepot(self,dindex)->Depot:
        if dindex in range(0,self.getNODepot()):
            return self.__depots[dindex]
        sys.exit(print("Depot 1 error"))
    def setDepot(self,dID):
        self.__depots_map[dID]=len(self.__depots)
        self.__depots.append(Depot(dID))
    def getDepotINDEX(self,dID):
        return self.__depots_map[dID]
    def getNOHubs(self):
        return len(self.__hubs)
    def getHub(self,hindex)->Hub:
        if hindex in range(0,self.getNOHubs()):
            return self.__hubs[hindex]
        sys.exit(print("Hub 1 error"))
    def setHub(self,hID):
        self.__hubs_map[hID]=len(self.__hubs)
        self.__hubs.append(Hub(hID))
    def getHubINDEX(self,hID):
        return self.__hubs_map[hID]
    def getNOProductTypes(self):
        return len(self.__producttypes)
    def getProductType(self,pindex)->ProductType:
        if pindex in range(0,self.getNOProductTypes()):
            return self.__producttypes[pindex]
        sys.exit(print("Product 1 error"))
    def setProductType(self,pID):
        self.__producttypes_map[pID]=len(self.__producttypes)
        self.__producttypes.append(ProductType(pID))
    def getProductTypeINDEX(self,pID):
        return self.__producttypes_map[pID]
    def getNOSupplierCapacities(self):
        return len(self.__suppliercapacities)
    def getSupplierCapacity(self,scindex)->SupplierCapacity:
        if scindex in range(0,self.getNOSupplierCapacities()):
            return self.__suppliercapacities[scindex]
        sys.exit(print("Supplier Capacity 1 error"))
    def setSupplierCapacity(self,scID,sID="",pID=""):
        if pID=="PT1":
            self.__suppliercapacities_map[sID]={pID:len(self.__suppliercapacities)}
        else:
            self.__suppliercapacities_map[sID][pID]=len(self.__suppliercapacities)
        self.__suppliercapacities.append(SupplierCapacity(scID))
    def getSupplierCapacityINDEX(self,sID,pID):
        return self.__suppliercapacities_map[sID][pID]
    def getNODemand(self):
        return len(self.__demands)
    def getDemand(self,dindex)->Demand:
        if dindex in range(0,self.getNODemand()):
            return self.__demands[dindex]
        sys.exit(print("Demand 1 error"))
    def setDemand(self,dID,deID="",pID=""):
        if pID=="PT1":
            self.__demands_map[deID]={pID:len(self.__demands)}
        else:
            self.__demands_map[deID][pID]=len(self.__demands)
        self.__demands.append(Demand(dID))
    def getDemandINDEX(self,deID,pID):
        return self.__demands_map[deID][pID]
    def getNOVehicles(self):
        return len(self.__vehicles)
    def getDistanceMatrix(self):
        return self.__distances
    def getDistance(self,facilityID1,facilityID2):
        if facilityID1[1]=="H" and facilityID2[1]=="H":
            sys.exit(print("Hub 2 error",facilityID1,facilityID2))
        if facilityID1[1]=="H":
            ID1=self.getHubINDEX(facilityID1)+self.getNOsuppliers()+self.getNODepot()
        if facilityID1[0]=="S":
            ID1=self.getSupplierINDEX(facilityID1)
        if facilityID1[0]=="D":
            ID1=self.getDepotINDEX(facilityID1)+self.getNOsuppliers()
        if facilityID2[0]=="S":
            ID2=self.getSupplierINDEX(facilityID2)
        if facilityID2[0]=="D":
            ID2=self.getDepotINDEX(facilityID2)+self.getNOsuppliers()
        if facilityID2[1]=="H":
            ID2=self.getHubINDEX(facilityID2)+self.getNOsuppliers()+self.getNODepot()
        return self.__distances[ID1,ID2]
    def getTimeMatrix(self):
        return self.__times
    def getTime(self,facilityID1,facilityID2):
        if facilityID1[1]=="H" and facilityID2[1]=="H":
            sys.exit(print("Hub 3 error"))
        if facilityID1[1]=="H":
            ID1=self.getHubINDEX(facilityID1)+self.getNOsuppliers()+self.getNODepot()
        if facilityID1[0]=="S":
            ID1=self.getSupplierINDEX(facilityID1)
        if facilityID1[0]=="D":
            ID1=self.getDepotINDEX(facilityID1)+self.getNOsuppliers()
        if facilityID2[0]=="S":
            ID2=self.getSupplierINDEX(facilityID2)
        if facilityID2[0]=="D":
            ID2=self.getDepotINDEX(facilityID2)+self.getNOsuppliers()
        if facilityID2[1]=="H":
            ID2=self.getHubINDEX(facilityID2)+self.getNOsuppliers()+self.getNODepot()
        return self.__times[ID1,ID2]
    def read_problem_instance(self):
        with open(str(self.__file_name)) as file_name:
            problem=json.load(file_name)
        instance=problem["instance"][0]
        for i in instance["suppliers"]:
            self.setSupplier(i["id"])
            self.getSupplier(self.getSupplierINDEX(i["id"])).setNAME(i["name"])
            self.getSupplier(self.getSupplierINDEX(i["id"])).setLATITUDE(i["latitude"])
            self.getSupplier(self.getSupplierINDEX(i["id"])).setLONGITUDE(i["longitude"])
            self.getSupplier(self.getSupplierINDEX(i["id"])).setINDEX(i["index"])
        for i in instance["depots"]:
            self.setDepot(i["id"])
            self.getDepot(self.getDepotINDEX(i["id"])).setNAME(i["name"])
            self.getDepot(self.getDepotINDEX(i["id"])).setLATITUDE(i["latitude"])
            self.getDepot(self.getDepotINDEX(i["id"])).setLONGITUDE(i["longitude"])
            self.getDepot(self.getDepotINDEX(i["id"])).setINDEX(i["index"])
        for i in instance["old hubs"]:
            self.setHub(i["id"])
            self.getHub(self.getHubINDEX(i["id"])).setNAME(i["name"])
            self.getHub(self.getHubINDEX(i["id"])).setLATITUDE(i["latitude"])
            self.getHub(self.getHubINDEX(i["id"])).setLONGITUDE(i["longitude"])
            self.getHub(self.getHubINDEX(i["id"])).setINDEX(i["index"])
            self.getHub(self.getHubINDEX(i["id"])).setExsisting(True)
        for i in instance["new hubs"]:
            self.setHub(i["id"])
            self.getHub(self.getHubINDEX(i["id"])).setNAME(i["name"])
            self.getHub(self.getHubINDEX(i["id"])).setLATITUDE(i["latitude"])
            self.getHub(self.getHubINDEX(i["id"])).setLONGITUDE(i["longitude"])
            self.getHub(self.getHubINDEX(i["id"])).setINDEX(i["index"])
            self.getHub(self.getHubINDEX(i["id"])).setExsisting(False)
        for i in instance["product types"]:
            self.setProductType(i["id"])
            self.getProductType(self.getProductTypeINDEX(i["id"])).setNAME(i["name"])
        for i in instance["supplier capacity"]:
            self.setSupplierCapacity(i["id"],i["supplier"],i["product"])
            self.getSupplierCapacity(self.getSupplierCapacityINDEX(i["supplier"],i["product"])).setPRODUCT(i["product"])
            self.getSupplierCapacity(self.getSupplierCapacityINDEX(i["supplier"],i["product"])).setSUPPLIER(i["supplier"])
            self.getSupplierCapacity(self.getSupplierCapacityINDEX(i["supplier"],i["product"])).setQUANTITY(i["quantity"])
        for i in instance["demand"]:
            self.setDemand(i["id"],i["depot"],i["product"])
            self.getDemand(self.getDemandINDEX(i["depot"],i["product"])).setPRODUCT(i["product"])
            self.getDemand(self.getDemandINDEX(i["depot"],i["product"])).setDEPOT(i["depot"])
            self.getDemand(self.getDemandINDEX(i["depot"],i["product"])).setQUANTITY(i["quantity"])
        for i in instance["vehicles"]:
            self.setVehicle(i["id"])
            self.getVehicle(self.getVehicleINDEX(i["id"])).setNAME(i["name"])
            self.getVehicle(self.getVehicleINDEX(i["id"])).setCAPACITY(i["capacity"])
            self.getVehicle(self.getVehicleINDEX(i["id"])).setQUANTITY(i["quantity"])
        self.__max_new_hubs=self.getNOHubs()
        distances=instance["distances"]
        times=instance["times"]
        self.__distances=np.array(distances)
        self.__times=np.array(times)


