# Selection-Hyper-heuristics-for-Solving-the-Location-Routing-Problem-with-Different-Hubs
We provide code for using selection hyperheuristics to solve a 2-echalon Location-Routing problem with different hubs. Please cite the following papers if you used any of these resources:

##simulating_data.py- 
This file is used to simulate instances of this specific Location-routing problem.
    Uses OSM data which can be found here: converted to a pygerc file
    
    instance_generation(seed,osm_file, sup_range,dep_range, oh_range,nh_range, pt_range,vt_range,instype,distype,key="") 
    
gerenates one instance with given ranges for size.
Instype 
- if equal 1: creates instances where demands are less then supplier capacities and vehicle capcity chosen from 3 options
- if equal 2: creates instances where demands are less then supplier capacities and vehicle capcity chosen from intergers in range
- if equal 3: creates instances where supplier capacities are less then demands and vehicle capcity chosen from intergers in range
Distype 
- if equal 1: calculates distances and times using google directions api. API key needed: url for googlse api
-if equal 2: calculates distances using pandana package. pandana will need to be installed first. Times estimated as factor of time with randomised speed.
Key: API key needed for distype 1. If using distype 2 can be left blank.
    
    generating
