import pandas as pd
from collections import defaultdict
from queue import PriorityQueue
import time
import sys

from geopy.distance import geodesic

## SearchNode
# A node used to capture information on f, g, and h costs, visited nodes, paths that have been ventured, and the
#   best solution label found at the current time
# @param: city, list of parents, list of visited cities, gcost, hcost, solution label
class SearchNode:
    def __init__(self, city, parents, current_path_cities, gcost = 0, hcost = 0, solution_label = ""):
        self.city = city #city node
        self.parents = parents #parent node list
        self.current_path_cities = current_path_cities #list of visited cities
        self.gcost = gcost #actual distance traveled
        self.hcost = hcost #straight line distance to goal city
        self.fcost = gcost + hcost #f = g + h
        self.solution_label = solution_label

## City
# A class to represent each city in the graph
# @param: name, edges, latitude-longitude pair
class City:
    name = "Nashville"
    #edges dict, keys are city objects, values are tuple, where tuple[0] = edge_label, tuple[1] = edge_cost
    #to get edge_label:   edges[cityobj][0]
    #to get cost:         edges[cityobj][1]
    edges = {}
    latlong = (0,0)

    def __init__(self, name, edges, latlong):
        self.name = name
        self.edges = edges
        self.latlong = latlong

## aStarSearch
# performs the A* anytime search algorithm
# @param: start_city, goal_city, resultFile
def aStarSearch(start_city, goal_city, resultFile):
    frontier = PriorityQueue()
    h = hcost(start_city, goal_city)
    startNode = SearchNode(start_city, [], [start_city.name], gcost=0, hcost=h)
    frontier.put((h, startNode))
    solutions = PriorityQueue()
    allVisited = set()

    elapsed_time = 0
    start_time = time.time()

    cont = "Y"
    numSolutions = 1
    while frontier and cont == "Y":
        cur_node = frontier.get()[1]

        allVisited.add(cur_node.city.name)
        if cur_node.city == goal_city:
            solutions.put((cur_node.gcost, cur_node))
            cur_node.solution_label = "Solution" + str(numSolutions)
            numSolutions+=1
            elapsed_time += time.time() - start_time
            cont = intermediate_output(cur_node.solution_label, cur_node, resultFile)
            start_time = time.time()
        

        for neighbor_city in cur_node.city.edges:
            edge_cost = cur_node.city.edges[neighbor_city][1]
            #Get neighbor g cost
            g = cur_node.gcost + edge_cost
            neighborParents = list(cur_node.parents)
            neighborParents.append(cur_node)
            #Check for loops
            if neighbor_city.name not in cur_node.current_path_cities:
                neighbor_path = list(cur_node.current_path_cities)
                neighbor_path.append(neighbor_city.name)
                neighbor_node = SearchNode(neighbor_city, neighborParents, neighbor_path, g, hcost(neighbor_city, goal_city))
                frontier.put((neighbor_node.fcost, neighbor_node))
            
    final_output(goal_city, solutions, allVisited, len(frontier.queue), elapsed_time, resultFile)

## intermediate_output
# outputs the current solution to screen and result_file
# @param: solution_label, end_nodes, result_file
def intermediate_output(solution_label, end_node, result_file):
    node_list = end_node.parents
    node_list.append(end_node)
    start_node = end_node.parents[0]
    outStr = solution_label + "  " + start_node.city.name + "  " + str(start_node.hcost) + "\n"
    
    node_list_size = len(node_list)
    parent = start_node
    count = 1

    for node in node_list[1:node_list_size]:
        outStr += str(count) + "  " + parent.city.name + "  " + node.city.name + "  "
        outStr += str(node.hcost) + "  " + node.city.edges[parent.city][0] + "  " + str(node.city.edges[parent.city][1]) + "  "
        outStr += str(node.gcost) + "  " + str(node.fcost) + "\n"
        count += 1
        parent = node
    
    outStr += node.city.name + "  " + str(node.gcost) + "\n"
    print(outStr)
    
    f = open(result_file, mode="a")
    f.write(outStr)
    f.close()

    input1 = input("Continue? (Y/N)")
    while (input1 != "Y" and input1 != "N"):
        input1 = input("Invalid input. Continue? (Y/N)")

    return(input1)

## final_output
# Output the final solution to screen and result_file
# @param: goal, solutions, allVisited, frontier_length, elapsedTime, resultFile
def final_output(goal, solutions, allVisited, frontier_length, elapsedTime, resultFile):
    total = 0
    minimum = solutions.queue[0][0]
    maximum = solutions.queue[len(solutions.queue)-1][0]
    for solution in solutions.queue:
        path_sum = solution[0]
        total += path_sum
    mean = total/len(solutions.queue)

    outStr = ""
    outStr += "a) Frontier size: " + str(frontier_length) + "\n"
    outStr += "b) Min cost path: " + str(minimum) + "\t" + "Mean cost path: " + str(mean) + "\t" + "Max cost path: " + str(maximum) + "\n"
    outStr += "c) Solution Label — Min cost path found: " + solutions.queue[0][1].solution_label + "\n"
    outStr += "d) All visited locations:\t" + " ".join(allVisited) + "\n"
    outStr += "e) Instrumented runtime: " + str(elapsedTime) + " seconds\n"
            

    f = open(resultFile, mode="a")
    f.write(outStr)
    f.close()
    print(outStr)

## get_neighbors
# gets the list of surrounding cities connected by roads
# @param: current node
# @returns: list of neighbors
def get_neighbors(current):
    return current.edges   
    
## hcost
# finds the heuristic for the distance between two cities
# @param: city1, city2
# @returns: heuristic distance
def hcost(city1, city2):
    return geodesic(city1.latlong, city2.latlong).miles


## read
# read csv into dfs and construct graph of cities and roads
# @param: edges_path, cities_path
# @returns: list of cities
def read(edges_path, cities_path):
    edges_df = pd.read_csv(edges_path, skiprows=0)
    cities_df = pd.read_csv(cities_path, skiprows=0)
    #dictionary, where keys are city names, and values are corresponding city objects
    city_list = {}


    for index, row in cities_df.iterrows():
        name = row.iloc[0]
        latitude = row.iloc[1]
        longitude = row.iloc[2]
        
        cty = City(name, {}, (latitude, longitude))
        city_list[cty.name] = cty
    
    # dict mapping city to set of lists containing locationB and actualDistance
    for index, row in edges_df.iterrows():
        edge_label = row.iloc[0]
        #get city objects from city_list dict, using locationA label
        city1 = city_list[row.iloc[1]]
        city2 = city_list[row.iloc[2]]
        edge_cost = row.iloc[3]
        
        #put each city in the other city's adjacency list
        city1.edges[city2] = (edge_label, edge_cost)
        city2.edges[city1] = (edge_label, edge_cost)
    return city_list

## RoadTrip
# high-level interface for engaging with A* anytime search algorithm
# @param: startLoc, goalLoc, LocFile, EdgeFile, resultFile
def RoadTrip(startLoc, goalLoc, LocFile, EdgeFile, resultFile):
    city_list = read(EdgeFile, LocFile)
    start_city = city_list[startLoc]
    goal_city = city_list[goalLoc]
    
    aStarSearch(start_city, goal_city, resultFile)


def main():
    # takes inputs from system call
    startLoc = sys.argv[1]
    goalLoc = sys.argv[2]
    LocFile = sys.argv[3]
    EdgeFile = sys.argv[4]
    resultFile = sys.argv[5]

    open(resultFile, "w").close()
    RoadTrip(startLoc, goalLoc, LocFile, EdgeFile, resultFile)

if __name__ == '__main__':
    main()
