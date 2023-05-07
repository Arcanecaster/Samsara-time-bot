"""
Travel Time
===========

Handles the travel time part for the samsara time bot so the main script isn't bloated with a bunch of hard coated graph and alias lookups.
Also throwing the algrothim and validation functions in here
"""

# Imports go here
import heapq

__author__ = "Arcane"
__version__ = "1.0.0"
__license__ = "Loisence"

# Module code goes here

regions = {
'Bachtalan': ['bachtalan', 'bach', 'talan'],
'Cortashar Dominion': ['cortashar dominion', 'cortashar', 'cd'],
'Dirk': ['dirk', 'drk'],
'Srath': ['divine empire of srath', 'srath', 'des', 'empire'],
'Farleaf': ['farleaf', 'fl', 'leaf'],
'Farwing Tribes': ['farwing tribes', 'farwing', 'fw'],
'Femursnap Tribes': ['femursnap tribes', 'femursnap', 'ft', 'snap', 'femur'],
'Kingdom of Evercia': ['kingdom of evercia', 'evercia', 'ke', 'everica'],
'Kingdom of Gundahn': ['kingdom of gundahn', 'gundahn', 'kg', 'kog'],
'Kobold Tribes': ['kobold tribes', 'kobold', 'kt'],
'Lunan': ['lunan', 'lu'],
'Orcish Legions': ['orcish legions', 'orc', 'ol', 'orcish'],
'Meloz Tribe': ['meloz tribe', 'meloz', 'mt'],
'Redhorn Hordes': ['redhorn hordes', 'redhorn', 'rh'],
'Rustvault': ['rustvault', 'rv', 'vault'],
'Samsara': ['samsara', 'sam'],
'Blue Coast Bay': ['blue coast bay', 'blue coast', 'bcb', 'bay', 'blue', 'coast'],
'Skarlian Holy State': ['skarlian holy state', 'skarlian', 'shs', 'skarlia'],
'The Silver Peninsula': ['the silver peninsula', 'silver peninsula', 'tsp', 'silver', 'peninsula'],
'Thornian Council': ['thornian council', 'thornian', 'tc', 'thornia', 'thorn'],
'Thrusk': ['thrusk', 'tr'],
'Tiamats Eye': ['tiamats eye', 'tiamat', 'te', 'eye'],
'United Hordes of Sinios': ['united hordes of sinios', 'sinios', 'uhs'],
'Venuvia': ['venuvia', 'vn'],
'Vurn Darul': ['vurn darul', 'vurn', 'vd', 'darul'],
'Aceria': ['acerica', 'ac', 'ace', 'aceria']
}
def validate_input(input_str):
    for region, aliases in regions.items():
        if input_str.lower() == region.lower() or input_str.lower() in aliases:
            return region
    return None

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    previous_nodes = {node: None for node in graph}
    while queue:
        (current_distance, current_node) = heapq.heappop(queue)
        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            path.reverse()
            return (distances[end], path)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    return (-1, []) # no path found
graph = {
    'Bachtalan': {'Orcish Legions': 6, 'Kobold Tribes': 6, 'Femursnap Tribes': 5, 'Srath': 3},
    'Cortashar Dominion': {'Sinios': 12, 'Farleaf': 10, 'Thrusk': 4, 'Redhorn Hordes': 2},
    'Dirk': {'Srath': 4, 'Meloz Tribe': 3},
    'Srath': {'Farwing Tribes': 20, 'Tiamats Eye': 10, 'Femursnap Tribes': 5, 'Kobold Tribes': 5, 'Meloz Tribe': 4, 'Dirk': 4, 'Bachtalan': 3},
    'Farleaf': {'Sinios': 12, 'Cortashar Dominion': 10, 'Vurn Darul': 10, 'Aceria': float('inf')},
    'Farwing Tribes': {'Srath': 20, 'Kobold Tribes': 15, 'Skarlian Holy State': 12, 'Tiamats Eye': 3},
    'Femursnap Tribes': {'Thrusk': 13, 'Lunan': 7, 'Srath': 5, 'Orcish Legions': 5, 'Bachtalan': 5, 'Meloz Tribe': 2},
    'Kingdom of Evercia': {'Silver Peninsula': 5, 'Skarlian Holy State': 1},
    'Kingdom of Gundahn': {'Vurn Darul': 7, 'Sinios': 6, 'Venuvia': 5, 'Thornian Council': 4, 'Aceria': float('inf')},
    'Kobold Tribes': {'Farwing Tribes': 15, 'Orcish Legions': 10, 'Bachtalan': 6, 'Srath': 5, 'Tiamats Eye': 3, 'Skarlian Holy State': 3},
    'Lunan': {'Meloz Tribe': 9, 'Femursnap Tribes': 7, 'Orcish Legions': 6, 'Thrusk': 5, 'Redhorn Hordes': 5},
    'Orcish Legions': {'Sinios': 12, 'Samsara': 11, 'Kobold Tribes': 10, 'Skarlian Holy State': 10, 'Redhorn Hordes': 9, 'Bachtalan': 6, 'Lunan': 6, 'Femursnap Tribes': 5},
    'Meloz Tribe': {'Thrusk': 15, 'Lunan': 9, 'Srath': 4, 'Dirk': 3, 'Femursnap Tribes': 2},
    'Redhorn Hordes': {'Orcish Legions': 9, 'Sinios': 8, 'Thrusk': 3, 'Cortashar Dominion': 2},
    'Rustvault': {'Venuvia': 8, 'Silver Peninsula': 7},
    'Samsara': {'Orcish Legions': 11, 'Sinios': 11, 'Thornian Council': 2},
    'Skarlian Holy State': {'Farwing Tribes': 12, 'Orcish Legions': 10, 'Tiamats Eye': 10, 'Kobold Tribes': 3, 'Kingdom of Evercia': 1},
    'Silver Peninsula': {'Rustvault': 7,'Kingdom of Evercia': 5},
    'Thornian Council': {'Sinios': 6,'Venuvia': 5,'Kingdom of Gundahn': 4,'Samsara': 2},'Thrusk': {'Meloz Tribe': 15,'Femursnap Tribes': 13,'Lunan': 5,'Cortashar Dominion': 4,'Redhorn Hordes': 3},
    'Tiamats Eye': {'Srath': 10,'Skarlian Holy State': 10,'Kobold Tribes': 3,'Farwing Tribes': 3},
    'Sinios': {'Orcish Legions': 12,'Cortashar Dominion': 12,'Farleaf': 12,'Samsara': 11,'Redhorn Hordes': 8,'Thornian Council': 6,'Vurn Darul': 4},
    'Venuvia': {'Rustvault': 8,'Thornian Council': 5,'Kingdom of Gundahn': 5, 'Aceria': float('inf')},
    'Vurn Darul': {'Farleaf': 10,'Kingdom of Gundahn': 7,'Sinios': 4, 'Aceria': float('inf')},
    'Aceria': {'Venuvia': 13, 'Kingdom of Gundahn': 8, 'Vurn Darul': 4, 'Farleaf': 7}
}
region_names = list(graph.keys())