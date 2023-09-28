import pandas as pd
from collections import defaultdict
from queue import PriorityQueue


from geopy.distance import geodesic

#cities paired with dictionaries
#sub dictionaries are edge-destination / edge-cost
edges = {"Nashville": {"Kentucky":100, }}

class SearchNode:
    def __init__(self, vertex, parent, path_cost, children, current_path):
        self.city = city
        self.parent = parent
        self.path_cost = path_cost
        self.children = children
        self.current_path = current_path

def search(start_city, end_city):
    
    startNode = SearchNode(start_city, None, 0, start_city.edges.keys, [])
    frontier = PriorityQueue()
    frontier.put(startNode)
    visited = []
    visited_paths = []
    cont = True
    while frontier and cont:
        #pop frontier
        nextNode = frontier.get()
        for cty in nextNode
    


class city:
    name = ""
    edges = {}
    longlat = (0,0)

    def __init__(self, name, edges, longlat):
        self.name = name
        self.edges = edges
        self.longlat = longlat


        Nashville:
        edges = {"Gatlinburg":("Nash to Gat on I-40", 120)}

class solStatus:
    #index
    solutionLabel = 0
    locations = []
    endLoc = city
    hCost = 0
    edgeLable = ""
    edgeCost = 0
    
    
    
    def push(cty):
        solStatus.locations.add(cty.name)
        



def hcost(city1, city2):
    return geodesic(city1.longlat, city2.longlat).miles
    


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