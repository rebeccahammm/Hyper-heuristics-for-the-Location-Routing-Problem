# Selection-Hyper-heuristics-for-Solving-the-Location-Routing-Problem-with-Different-Hubs
We provide code for using selection hyperheuristics to solve a 2-echalon Location-Routing problem with different hubs. Please cite the following paper if you used any of these resources:

## simulating_data.py- 

This file is used to simulate instances of this specific Location-routing problem.
    Uses OSM data which can be found here: https://download.geofabrik.de/ and convert to a pygerc file using https://github.com/AndGem/OsmToRoadGraph. To generate instances we can use the following functions:
    
    
    
    instance_generation(seed,osm_file, sup_range,dep_range, oh_range,nh_range, pt_range,vt_range,instype,distype,key="") 
    
generates one instance with given ranges for size. Ranges are given in list format. 
-sup_range= number of supplier range
-dep_range= number of depot range
-oh_range= number of old hub range
-nh_range= number of new hub range
-pt_range= number of product type range
-vt_range= number of vehicle type range
Instype 
- if equal 1: creates instances where demands are less then supplier capacities and vehicle capcity chosen from 3 options
- if equal 2: creates instances where demands are less then supplier capacities and vehicle capcity chosen from intergers in range
- if equal 3: creates instances where supplier capacities are less then demands and vehicle capcity chosen from intergers in range

Distype 
- if equal 1: calculates distances and times using google directions api. API key needed: (https://developers.google.com/maps/documentation/directions) 
- if equal 2: calculates distances using pandana package. pandana will need to be installed first. Times estimated as factor of time with randomised speed.

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
This prints the routes taken, hubs opened, objective value, total infeasibility and individual constraint violations of a solution.

## heuristic_methods.py-
 This file contains Low-Level heuristics used within the hyper-heuristics.

## heuristic.py-
This file includes both intial solution methods:
    
    initial_solution_random(problem,solution)
produces a random initial solution

    initial_solution_greedy_depot_allocation(problem,solution)
produces a greedy initial solution
    
As well as a simpler test heuristic I haved used to estimate optimal values:

    heuristic_lrp(problem,max_new_hubs,min_throughtput,max_time)
    
and a way to plot solutions:

    plot(p,s,t,sol)
    
where 
-p is the problem class
-s is routes
-t is the title of the plot
-sol is the solution class
 
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
 
    comparison(methods)
    
 given a list of results from different methods this function returns results from comparing results. For each method it states how many functions it is significantly better than, better than, equal to, worse than, significantly worse than.
 
 ## evaulatingmethods.py
 This file runs methods on instances but this time only 10 times but with 10 times the number of iterations on two selected methods. This was use to anyalase methods:
    
    Runall(no_processes,ListOfFunctions)
    
 Runs functions in parellel.
 example of use:
 
    List=[(testingmethods_B,"Anaylis_of_random_ADSHRR_ins_5.p",[2,8,28800,["biginstance3.json"]]),(testingmethods_c,"Anaylis_of_greedy_SHRR_ins_5.p",[2,8,28800,["biginstance3.json"]])]
    Runall(len(List),List)
    
 ## evaluationgonemethod.py
 This file creates graphs used for analyazing LLH used and process of finding a solution for algorithmims. To use functions may have to redefine dictionary of results. For example Instance 0 results maybe saved in [0] of the dictionary so we redefine dictionary the following way:
    
    ins0method1=insomethod[0]
      
                                    
    graph(results,ins)
 creates a graph from results of one method and instance that shows the average objective function of the 10 runs at each iteration. ins provided is just the instance number to use for the title.

    obj_infe_graph(method1,start, pathlength)
creates two graphs one showing average objective value at each iteration and one showing the average infeasibility at each iteration. method1 is the results we are using. The graph shows interations _start_ to _pathlength_.

    llh_sequence_combined_multi_ins(results,method)
 create a graph showing percentage of LLH use for all instances with sequence of instances combined in one catergory. results is a list of results for the instances and method is the method used 1 is ADSH and 2 is SH
 
    llh_eachchoice_multi_ins(results,method,percent)
creates a graph showing percentage of LLH use for all instances. results is a list of results for the instances, method is the method used 1 is ADSH and 2 is SH and percent is the threshold for which if LLHs are under they and combined together in a other catergory

    llh_eachindiv_multi_ins(results,method,percent)
creates a graph showing percentage of LLH use within sequences for all instances. results is a list of results for the instances, method is the method used 1 is ADSH and 2 is SH and percent is the threshold for which if LLHs are under they and combined together in a other catergory

