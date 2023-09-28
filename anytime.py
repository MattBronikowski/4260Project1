import pandas as pd
from collections import defaultdict
from queue import PriorityQueue

from geopy.distance import geodesic

#cities paired with dictionaries
#sub dictionaries are edge-destination / edge-cost
edges = {"Nashville": {"Kentucky":100, }}

class SearchNode:
    def __init__(self, city, parent, edge_label, edge_cost, hcost, path_sum, current_path_cities):
        self.city = city
        self.parent = parent
        self.edge_label = edge_label
        self.edge_cost = edge_cost
        self.hcost = hcost
        self.path_sum = path_sum
        # self.children = children
        self.current_path_cities = current_path_cities

def gcost(city1, city2):
    return geodesic(city1.longlat, city2.longlat).miles

#build an output text, and then print / write it to output file
def output(final_search_node, out_file):
    output_text = ""

def finish(pqueue):
    

def search(start_city, end_city):
    
    startNode = SearchNode(start_city, None, 0, [])
    frontier = PriorityQueue()
    frontier.put(startNode)
    visited = []
    visited_paths = []
    cont = True
    while frontier and cont:
        #pop frontier
        node = frontier.get()
        new_path_sum = node.path_sum + node.edge_cost
        if node.cty.name == end_city.name:
            output(node)
            #pause timer
            cont = (input('Continue searching? Type "y"\n')=="y")
            #continue timer
        else:
            for cty in node.city.edges:
                #find edge to another city
                if cty.name not in node.current_path_cities:
                    edge = node.city.edges[cty]
                    edge_label = edge[0]
                    edge_cost = edge[1]
                    new_cities = list(node.current_path_cities)
                    new_cities.append(cty.name)
                    hcost = gcost(node.city, cty) + ctyNode.path_sum
                    #make new node, with 
                    ctyNode = SearchNode(cty, node, hcost, edge_label, edge_cost, 
                                         new_path_sum, new_cities)
                    frontier.put((ctyNode.hcost, ctyNode))
    #do final output
    finish()



class city:
    name = "Nashville"
    edges = {"Detroit":("Detroit to Nash on i-40",100)}
    longlat = (0,0)

    def __init__(self, name, edges, longlat):
        self.name = name
        self.edges = edges
        self.longlat = longlat


        Nashville:
        edges = {"Gatlinburg":("Nash to Gat on I-40", 120)}

            


# End of Ryan's stuff
#

    


## read csv into dicts, one of adjacency list and one with city coordinates
def read(path1, path2, adj, coordinates):
    edges_df = pd.read_csv(path1)
    loc_df = pd.read_csv(path2)

    for loc in loc_df:
        coordinates[loc['Location Label']].append([loc['Latitude'], loc['Longitude']])

    # dict mapping city to set of lists containing locationB and actualDistance
    adj = defaultdict(set)
    for row in edges_df:
        city = row['locationA']
        to = row['locationB']
        gcost = row['actualDistance']
        
        adj[city].add([to, gcost])



## performs the search, returns path_sum
def traverse(adj, coordinates, visited, path_sum, cur_loc, goal, p_queue, count, visited_paths):
    if cur_loc == goal:
        visited_paths.append([])
        return [p_queue.qsize(), path_sum, count+1]
    
    path = visited_paths[visited_paths.size()-1]
    visited_paths[visited_paths.size()-1].append(cur_loc)
    
    visited.add(cur_loc)

    
    # builds priority queue
    cities = adj[cur_loc]
    for city in cities:
        destination = city[0]
        distance = adj[destination][2]
        if destination not in visited and path not in visited_paths:
            city1 = (coordinates[cur_loc], coordinates[cur_loc])
            city2 = (coordinates[destination], coordinates[destination])
            fcost = hcost(city1, city2)
            p_queue.put((fcost, [destination, distance]))
    
    # iterates through priority queue for next traversal
    while p_queue:
        info = p_queue.get()
        destination = info[0]
        traverse(adj, coordinates, visited, path_sum + info[1], destination, goal, p_queue)
    
    return -1



def main():
    path1 = '\csv files\Road Network - Edges.csv'
    path2 = '\csv files\Road Network - Locations.csv'
    adj = {}
    coordinates = {}
    read(path1, path2, adj, coordinates)
    
    # set of visited cities
    visited = {}
    visited_paths = [[]]
    p_queue = PriorityQueue()
    goal = input('Enter your goal')
    cont = 'yes'
    while(cont  == 'yes'):
        city = ""
        
        x = traverse(adj, coordinates, visited, 0, city, goal, p_queue, 0, visited_paths)

        
        cont = input('Continue finding another solution?')


if __name__ == '__main__':
    main()