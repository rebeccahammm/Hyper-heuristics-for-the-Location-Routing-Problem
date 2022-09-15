# Selection-Hyper-heuristics-for-Solving-the-Location-Routing-Problem-with-Different-Hubs
We provide code for using selection hyperheuristics to solve a 2-echalon Location-Routing problem with different hubs. Please cite the following paper if you used any of these resources:

## simulating_data.py- 

This file is used to simulate instances of this specific Location-routing problem.
    Uses OSM data which can be found here: converted to a pygerc file
    
    instance_generation(seed,osm_file, sup_range,dep_range, oh_range,nh_range, pt_range,vt_range,instype,distype,key="") 
    
generates one instance with given ranges for size.
Instype 
- if equal 1: creates instances where demands are less then supplier capacities and vehicle capcity chosen from 3 options
- if equal 2: creates instances where demands are less then supplier capacities and vehicle capcity chosen from intergers in range
- if equal 3: creates instances where supplier capacities are less then demands and vehicle capcity chosen from intergers in range

Distype 
- if equal 1: calculates distances and times using google directions api. API key needed: url for googlse api
-if equal 2: calculates distances using pandana package. pandana will need to be installed first. Times estimated as factor of time with randomised speed.

Key: API key needed for distype 1. If using distype 2 can be left blank.
    
    generating_multiple(num_of,seed,sup_range,dep_range, oh_range,nh_range, pt_range,vt_range,ins_types,dist_types,osm_file,key="")
generates num_of different instances with same stated characteristics and saves them into json files.

## problem_class.py-
This file defines the Problem class. To read a instance file into a problem class you must run the following code:
   
    prob=Problem(file_name)
    prob.read_problem_instance()

## solution_class.py-
This file defines the Solution class. To read in a solution from a file use the follwing code:

    sol=Solution()
    sol.ReadFromFile(file_name)
    
Once we have a solution (lets say its called sol) we can do the following:
    
    sol.getObjectiveFunction()
This prints the objective function

    sol.Feasibility()
This prints a value indicating the infeasibility of a solution

    sol.printSolution()
This prints the routes taken, hubs opened, Objective Value, Total infeasibility and individual constraint violations of a solution.

## heuristic_methods.py-
 This file contains Low-Level heuristics used within the hyper-heuristics.

## heuristic.py-
This file include both intial solution methods:
    
    initial_solution_random(problem,solution)
    initial_solution_greedy_depot_allocation(problem,solution)
    
As well as a simpler test heuristic I haved used to estimate optimal values:

    heuristic_lrp(problem,max_new_hubs,min_throughtput,max_time)
    
and a way to plot solutions:

    plot(p,s,t,sol)
 
 ## testingmethods.py-
  This file is used to test all methods.
  
    Runall(no_processes,ListofFunctions)
 Runs methods in parellel using no_processes processors. 
 The list of functions should contain tuples with look like:
 
    (function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
Where the function is one of the below without brackets and file is where results will be saved. 
### functions:
    
    testingmethods_SR_G(function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
    
    testingmethods_A_G(function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
    
    testingmethods_S_G(function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
    
    testingmethods_ADSH_G(function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
    
    testingmethods_SR_R(function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
    
    testingmethods_A_R(function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
    
    testingmethods_S_R(function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
    
    testingmethods_ADSH_R(function,file.p,[max_new_hubs,min_throughput,max_time,[instance_files],[estimated_instance_optimal_values])
    
 ## comparing_methods.py
 This file compares results of the different hyperheuristics.
 
 ## evaulatingmethods.py
 This file runs methods on instances but this time only 10 times but with 10 times the number of iterations. This was use to anyalase methods:
 
 ## evaluationgonemethod.py
 This file creates graphs used for analyazing 
