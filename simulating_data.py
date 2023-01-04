# -*- coding: utf-8 -*-


import json
import random
from numpy.random import binomial
from numpy.random import normal
import pandas as pd
import googlemaps
from datetime import datetime
import gmplot
import numpy as np
import requests
import pandana
from joblib import Parallel,delayed
import dill as pickle
from joblib import parallel_backend
#function to makes lists of edges and nodes from osm data
def get_ids_edges(file_name):
    data = pd.read_csv(file_name)
    dat = data[int(data.iloc[6])+8:]
    nodes_data = pd.DataFrame()
    s = dat[list(dat.columns)[0]].apply(lambda x: x.split(' '))
    nodes_data['id1'] = s.apply(lambda x: x[0]).astype("int64")
    nodes_data['id2'] = s.apply(lambda x: x[1]).astype("int64")
    nodes_data['length'] = s.apply(lambda x: x[2]).astype("float32")
    nodes_data['type'] = s.apply(lambda x: x[3])
    nodes_data['speed'] = s.apply(lambda x: x[4])
    nodes_data['bi_directional'] = s.apply(lambda x: x[5])
    # ---------------------
    # extract nodes
    d = data[8:int(data.iloc[6])+8]
    nodes_ids = pd.DataFrame()
    s = d[list(d.columns)[0]].apply(lambda x: x.split(' '))
    nodes_ids['id'] = s.apply(lambda x: x[0]).astype('float64')
    nodes_ids['latitude'] = s.apply(lambda x: x[1]).astype('float64')
    nodes_ids['longitude'] = s.apply(lambda x: x[2]).astype('float64')
    nodes_data['Risk'] = 0.5
    return nodes_ids, nodes_data



#generates locations for suppliers
def supplier_generation(num_suppliers,ids):
    suppliers = [

    ]

    for i in range(num_suppliers):
        x = random.randrange(len(ids))
        suppliers.append({
            "id": "S"+str(i+1),
            "name": "",
            "latitude": ids["latitude"].iloc[x],
            "longitude": ids["longitude"].iloc[x],
            "index": ids["id"].iloc[x]})
    return suppliers

#generates locates for depots
def depot_generation(num_depots,ids):
    depots = [
    ]

    for i in range(num_depots):
        x = random.randrange(len(ids))
        depots.append({
            "id": "D"+str(i+1),
            "name": "",
            "latitude": ids["latitude"].iloc[x],
            "longitude": ids["longitude"].iloc[x],
            "index": ids["id"].iloc[x]})
    return depots

#generates locations for old hubs
def old_hub_generation(num_old_hubs,ids):
    old_hubs = [

    ]

    for i in range(num_old_hubs):
        x = random.randrange(len(ids))
        old_hubs.append({
            "id": "OH"+str(i+1),
            "name": "",
            "latitude": ids["latitude"].iloc[x],
            "longitude": ids["longitude"].iloc[x],
            "index": ids["id"].iloc[x]})
    return old_hubs

#generates locations for new hubs
def new_hub_generation(num_new_hubs,ids):
    new_hubs = [

    ]

    for i in range(num_new_hubs):
        x = random.randrange(len(ids))
        new_hubs.append({
            "id": "NH"+str(i+1),
            "name": "",
            "latitude": ids["latitude"].iloc[x],
            "longitude": ids["longitude"].iloc[x],
            "index": ids["id"].iloc[x]})
    return new_hubs

#generates product types
def product_types_generation(num_product_types):
    product_types = [

    ]
    for i in range(num_product_types):
        product_types.append({
            "id": "PT"+str(i+1),
            "name": ""})
    return product_types

#generates supplier capacity. 
#Type 1: one supplier has enough cap for multiple depots
#Type 2: Depot needs to recieve product from multiple depots
def supplier_capacity_generation_1(num_suppliers, num_product_types, product_types, suppliers):
    supplier_capacity = [

    ]
    index = 0
    for i in range(num_suppliers):
        for j in range(num_product_types):
            index += 1
            supplier_capacity.append({
                "id": "C"+str(index),
                "product": product_types[j]['id'],
                "supplier": suppliers[i]['id'],
                "quantity": max(0,int(normal(100, 5, size=None)*binomial(1, 0.85, size=None)))})
    return supplier_capacity


def supplier_capacity_generation_2(num_suppliers, num_product_types, product_types, suppliers):
    supplier_capacity = [

    ]
    index = 0
    for i in range(num_suppliers):
        for j in range(num_product_types):
            index += 1
            supplier_capacity.append({
                "id": "C"+str(index),
                "product": product_types[j]['id'],
                "supplier": suppliers[i]['id'],
                "quantity": max(0,int(normal(15, 5, size=None)))})
    return supplier_capacity

#generates demand
#Type 1: one supplier has enough cap for multiple depots
#Type 2: Depot needs to recieve product from multiple depots
def demand_generation_1(num_depots, num_product_types, product_types, depots):
    demand = [
    ]
    index = 0
    for i in range(num_depots):
        for j in range(num_product_types):
            index += 1
            demand.append({
                "id": "De"+str(index),
                "product": product_types[j]['id'],
                "depot": depots[i]['id'],
                "quantity": max(0,int(normal(15, 5, size=None)*binomial(1, 0.85, size=None)))})
    return demand

def demand_generation_2(num_depots, num_product_types, product_types, depots):
    demand = [
    ]
    index = 0
    for i in range(num_depots):
        for j in range(num_product_types):
            index += 1
            demand.append({
                "id": "De"+str(index),
                "product": product_types[j]['id'],
                "depot": depots[i]['id'],
                "quantity": max(0,int(normal(45, 5, size=None)))})
    return demand

#generates vehicle types and there capacity
#type 1: capacity is chosen from three options 
#type 2: capacity chosen from a range
def vehicle_types_generation_1(num_vehicle_types):
    vehicle_types = [
    ]
    for i in range(num_vehicle_types):
        vehicle_types.append({
            "id": "V"+str(i+1),
            "name": "",
            "capacity": random.choice([26, 35, 42]),
            "quantity": 100000})
    return vehicle_types

def vehicle_types_generation_2(num_vehicle_types):
    vehicle_types = [
    ]
    for i in range(num_vehicle_types):
        vehicle_types.append({
            "id": "V"+str(i+1),
            "name": "",
            "capacity": random.randint(19, 31),
            "quantity": 100000})
    return vehicle_types

#formulates matrices of distances and times between facilities 
#not distances and time for hub to hub
#type 1: uses google api
#type 2: uses networkx
def distances_time_1(key,suppliers, depots, oldhubs, newhubs):
    print("STOP")
    suppliers_depots_lat = []
    suppliers_depots_lon = []
    all_facilities_lat = []
    all_facilities_lon = []
    for i in suppliers:
        suppliers_depots_lat.append(i["latitude"])
        all_facilities_lat.append(i["latitude"])
        suppliers_depots_lon.append(i["longitude"])
        all_facilities_lon.append(i["longitude"])
    for i in depots:
        suppliers_depots_lat.append(i["latitude"])
        all_facilities_lat.append(i["latitude"])
        suppliers_depots_lon.append(i["longitude"])
        all_facilities_lon.append(i["longitude"])
    for i in oldhubs:
        all_facilities_lat.append(i["latitude"])
        all_facilities_lon.append(i["longitude"])
    for i in newhubs:
        all_facilities_lat.append(i["latitude"])
        all_facilities_lon.append(i["longitude"])
    distances=[]
    times=[]
    apikey=key
    depart= datetime(2022, 7, 13,12,0,0)
    gmaps=googlemaps.Client(key=apikey)
    for i in range(len(all_facilities_lat)):
        disti=[]
        timei=[]
        for j in range(len(all_facilities_lat)):
            origin= (all_facilities_lat[i], all_facilities_lon[i])
            destination = (all_facilities_lat[j], all_facilities_lon[j])
            if origin==destination:
                disti.append(0)
                timei.append(0)
            else:
                directions_result=gmaps.directions(origin, destination, mode="driving", departure_time=depart)
                disti.append((float(directions_result[0]["legs"][0]["distance"]["value"])/1000.0))
                timei.append((float(directions_result[0]["legs"][0]["distance"]["value"])/60.0))
        distances.append(disti)
        times.append(timei)
    return distances, times



def distances_time_2(ids,edges,suppliers, depots, oldhubs, newhubs):
    all_indexes=[]
    sup_and_dept_indexes=[]
    ids.set_index('id', inplace= True)
    p=pandana.network.Network(ids["latitude"], ids["longitude"], edges["id1"], edges["id2"], edges[["length"]]) 
    edges.set_index(["id1","id2"], inplace= True)
    for i in suppliers:
        all_indexes.append(i["index"])
        sup_and_dept_indexes.append(i["index"])
    for i in depots:
        all_indexes.append(i["index"])
        sup_and_dept_indexes.append(i["index"])
    for i in oldhubs:
        all_indexes.append(i["index"])
    for i in newhubs:
        all_indexes.append(i["index"])  
    distances=[]
    for i in all_indexes:
        distances.append(p.shortest_path_lengths([i for x in range(len(all_indexes))],all_indexes))
    times=[]
    for i in range(len(sup_and_dept_indexes)):
        times_row=[]
        for j in range(len(all_indexes)):
            times_row.append(distances[i][j]/random.randint(30, 60))
        times.append(times_row)
    return distances, times


#creates instance
#instype: type 1- demand and sup cap type 1 and vehicle type 1
#         type 2- demand and sup cap type 2 and vehicle type 2
#         type 3- demand and sup cap type 1 and vehicle type 2
#distype: type 1- distance and times using google api
#         type 2- distance and times using networkx
def instance_generation(seed, osm_file, sup_range, dep_range, oh_range, nh_range, pt_range, vt_range,instype,distype,key=""):
    random.seed(seed)
    ids, edges = get_ids_edges(osm_file)
    num_suppliers = random.randrange(sup_range[0], sup_range[1], 1)
    num_depots = random.randrange(dep_range[0], dep_range[1], 1)
    num_old_hubs = random.randrange(oh_range[0], oh_range[1], 1)
    num_new_hubs = random.randrange(nh_range[0], nh_range[1], 1)
    num_product_types = random.randrange(pt_range[0], pt_range[1], 1)
    num_vehicle_types = random.randrange(vt_range[0], vt_range[1], 1)
    product_types = product_types_generation(num_product_types)
    suppliers = supplier_generation(num_suppliers,ids)
    depots = depot_generation(num_depots,ids)
    oldhubs=old_hub_generation(num_old_hubs,ids)
    newhubs=new_hub_generation(num_new_hubs,ids)
    if distype==1:
        dt=distances_time_1(key, suppliers, depots, oldhubs, newhubs)
    if distype==2:
        dt=distances_time_2(ids,edges,suppliers, depots, oldhubs, newhubs)
    if instype==1:
        instance = {
            "instance": [{"suppliers": suppliers,
                         "depots": depots,
                          "old hubs": oldhubs,
                          "new hubs": newhubs,
                          "product types": product_types,
                          "supplier capacity": supplier_capacity_generation_1(num_suppliers, num_product_types, product_types, suppliers),
                          "demand": demand_generation_1(num_depots, num_product_types, product_types, depots),
                          "vehicles": vehicle_types_generation_1(num_vehicle_types),
                          "distances": dt[0],
                          "times": dt[1]
                          }]
                    }
    if instype==2:
        instance = {
            "instance": [{"suppliers": suppliers,
                         "depots": depots,
                          "old hubs": oldhubs,
                          "new hubs": newhubs,
                          "product types": product_types,
                          "supplier capacity": supplier_capacity_generation_2(num_suppliers, num_product_types, product_types, suppliers),
                          "demand": demand_generation_2(num_depots, num_product_types, product_types, depots),
                          "vehicles": vehicle_types_generation_2(num_vehicle_types),
                          "distances": dt[0],
                          "times": dt[1]
                          }]
                    }
    if instype==3:
        instance = {
            "instance": [{"suppliers": suppliers,
                         "depots": depots,
                          "old hubs": oldhubs,
                          "new hubs": newhubs,
                          "product types": product_types,
                          "supplier capacity": supplier_capacity_generation_1(num_suppliers, num_product_types, product_types, suppliers),
                          "demand": demand_generation_1(num_depots, num_product_types, product_types, depots),
                          "vehicles": vehicle_types_generation_2(num_vehicle_types),
                          "distances": dt[0],
                          "times": dt[1]
                          }]
                    }
    return instance


def generating_multiple(num_of, seed,sup_range, dep_range, oh_range, nh_range, pt_range, vt_range,ins_types,dist_types,osm_file,key=""):
    random.seed(seed)
    for i in list(range(num_of)):
        with open("biginstance"+str(i+3)+".json", "w") as write:
            json.dump(instance_generation(random.random()*100,osm_file,
                      [sup_range[0],sup_range[1]], [dep_range[0],dep_range[1]], [oh_range[0], oh_range[1]], [nh_range[0], nh_range[1]], [pt_range[0], pt_range[1]], [vt_range[0], vt_range[1]],ins_types,dist_types), write)
