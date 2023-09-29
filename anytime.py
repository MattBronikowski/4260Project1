import pandas as pd
from collections import defaultdict
from queue import PriorityQueue

from geopy.distance import geodesic

#cities paired with dictionaries
#sub dictionaries are edge-destination / edge-cost
edges = {"Nashville": {"Kentucky":100, }}

# class SearchNode:
#     def __init__(self, city, parent, edge_label, edge_cost, hcost, path_sum, current_path_cities):
#         self.city = city #instance of city class, with its own edges and name
#         self.parent = parent #parent searchNode
#         self.edge_label = edge_label #label of edge from parent city to city
#         self.edge_cost = edge_cost #cost of said edge
#         self.hcost = hcost #heuristic cost (from function, gcost + path_sum)
#         self.path_sum = path_sum #cost of path up until now (not including new edge)
#         self.current_path_cities = current_path_cities #list of cities in path (prevent loops)

class SearchNode:
    def __init__(self, city, parents, gcost = 0, hcost = 0):
        self.city = city #city node
        self.parents = parents #parent node list
        self.gcost = gcost #actual distance traveled
        self.hcost = hcost #straight line distance to goal city
        self.fcost = gcost + hcost #f = g + h
        
    def __lt__(self, other):
        return (self.f) < (other.f)


def aStarSearch(start_city, goal_city):

    frontier = PriorityQueue()
    h = hcost(start_city, goal_city)
    startNode = SearchNode(start_city, None, 0, h)
    frontier.put(h, startNode)
    solutions = PriorityQueue()

    while frontier and cont == "Y":
        cur_node = frontier.get()
        if cur_node.city == goal_city:
            path = cur_node.parents.append(cur_node)
            cont = output(path)
            solutions.put(cur_node.gcost, path)
        

        for neighbor_city in get_neighbors(cur_node.city):
            #Get neighbor g cost
            g = cur_node.gcost + neighbor_edge
            neighborParents = cur_node.parents.append(cur_node)
            
            # found = False
            # for node in frontier:
            #     if node.city == neighbor_city and node.gcost <= g:
            #         found = True
            #         break

            # if not found:
            neighbor_node = SearchNode(neighbor_city, neighborParents, g, hcost(neighbor_city, goal_city))
            frontier.put((neighbor_node.fcost, neighbor_node))
        

#Output the best solution on the priority queue and prompt the user to continue
def output(list):
    path = '/results.txt'
    with open(path, "w") as out:
        out.write(str(list))
    print("Continue? (Y/N)")
    input1 = input()
    if (input1 != "Y" or input1 != "N"){
        print("Invalid input. Continue? (Y/N)")
        input1 = input()
    }
    return(input1)

def get_neighbors(current):
    return current.edges   
    

def hcost(city1, city2):
    return geodesic(city1.longlat, city2.longlat).miles

# ## old stuff
# def search(start_city, end_city):
#     startNode = SearchNode(start_city, None, 0, [])
#     frontier = PriorityQueue()
#     frontier.put(startNode)
#     visited = []
#     visited_paths = []
#     cont = True
#     while frontier and cont:
#         #pop frontier
#         node = frontier.get()
#         new_path_sum = node.path_sum + node.edge_cost
#         if node.cty.name == end_city.name:
#             output(node)
#             #pause timer
#             cont = (input('Continue searching? Type "y"\n')=="y")
#             #continue timer
#         else:
#             for cty in node.city.edges:
#                 #find edge to another city
#                 if cty.name not in node.current_path_cities:
#                     edge = node.city.edges[cty]
#                     edge_label = edge[0]
#                     edge_cost = edge[1]
#                     new_cities = list(node.current_path_cities)
#                     new_cities.append(cty.name)
#                     hcost = gcost(node.city, cty) + new_path_sum
#                     #make new node, with 
#                     ctyNode = SearchNode(cty, node, hcost, edge_label, edge_cost, 
#                                          new_path_sum, new_cities)
#                     frontier.put((ctyNode.hcost, ctyNode))
#     #do final output
#     finish()



class city:
    name = "Nashville"
    edges = {"Detroit":("Detroit to Nash on i-40",100)}
    longlat = (0,0)

    def __init__(self, name, edges, longlat):
        self.name = name
        self.edges = edges
        self.longlat = longlat

            


# End of Ryan's stuff
#


## read csv into dicts, one of adjacency list and one with city coordinates
def read(path1, path2, cities):
    edges_df = pd.read_csv(path1)
    cities_df = pd.read_csv(path2)

    for row in cities_df:
        cityName = row['Location Label']
        cityLongLat = row['Longitude', 'Latitude']
        newCity = city(cityName, {}, cityLongLat)
        cities.append(newCity)

    # dict mapping city to set of lists containing locationB and actualDistance
    adj = defaultdict(set)
    for row in edges_df:
        edgeLabel = row['edgeLabel']
        city1 = row['locationA']
        city2 = row['locationB']
        gcost = row['actualDistance']
        
        adj[city1].add([city2, gcost, edgeLabel])
        adj[city2].add([city1, gcost, edgeLabel])

    ## Need to add from adj to edge list for each city node


def main():
    path1 = '\csv files\Road Network - Edges.csv'
    path2 = '\csv files\Road Network - Locations.csv'
    cities = {}
    adj = {}
    read(path1, path2, cities, adj)
    
    # # set of visited cities
    # visited = {}
    # visited_paths = [[]]
    # p_queue = PriorityQueue()
    # goal = input('Enter your goal')
    # cont = 'yes'
    # while(cont  == 'yes'):
    #     city = ""
        
    #     x = traverse(adj, coordinates, visited, 0, city, goal, p_queue, 0, visited_paths)

        
    #     cont = input('Continue finding another solution?')


if __name__ == '__main__':
    main()


#cities paired with dictionaries
#sub dictionaries are edge-destination / edge-cost
#edges = {"Nashville": {"Kentucky":100, }}

# class SearchNode:
#     def __init__(self, city, parent, edge_label, edge_cost, hcost, path_sum, current_path_cities):
#         self.city = city #instance of city class, with its own edges and name
#         self.parent = parent #parent searchNode
#         self.edge_label = edge_label #label of edge from parent city to city
#         self.edge_cost = edge_cost #cost of said edge
#         self.hcost = hcost #heuristic cost (from function, gcost + path_sum)
#         self.path_sum = path_sum #cost of path up until now (not including new edge)
#         self.current_path_cities = current_path_cities #list of cities in path (prevent loops)