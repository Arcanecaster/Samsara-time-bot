"""
Travel Time
===========

Handles the travel time part for the everfjord time bot so the main script isn't bloated with a bunch of hard coated graph and alias lookups.
Also throwing the algrothim and validation functions in here
"""

# Imports go here
import heapq
import os
import requests

__author__ = "Arcane"
__version__ = "1.0.0"
__license__ = "Loisence"

# Module code goes here

regions = {
'Bachtalan': ['bachtalan', 'bach', 'talan'],
'Eisenland': ['eisenland', 'cortashar', 'cd', 'eisen'],
'Khrobat': ['khrobat', 'drk', 'dirk', 'khro', 'bat'],
'Kemet': ['srath', 'des', 'empire' 'kemet'],
'Solana': ['solana', 'fl', 'leaf', 'farleaf'],
'Solana Tribes': ['solana tribes', 'solana', 'fw', 'farwing', 'farwing tribes', 'st'],
'Zamwall Tribes': ['zamwall tribes', 'zamwall', 'zt', 'snap', 'femur', 'femursnap'],
'Kingdom of Leonia': ['kingdom of leonia', 'leonia', 'kl', 'everica'],
'Twin Kingdoms of Wildhammers': ['wildhammer', 'twin kingdoms','twin kingdoms of wildhammers', 'gundahn' 'wildhammers'],
'Tungsten State': ['tungsten state', 'kobold', 'kt'],
'Lunan': ['lunan', 'lu'],
'Duronia': ['duronia', 'duro', 'ol', 'orcish', 'orcish legions'],
'Norstraden': ['norstraden', 'meloz', 'meloz tribe'],
'Bihar Hordes': ['bihar hordes', 'bihar', 'bh', 'redhorn'],
'Onyxbridge': ['onyxbridge', 'rustvault'],
'Everfjord': ['everfjord', 'samsara', 'ever'],
'Albalatin Holy State': ['albalatin','albatin holy state', 'skarlian', 'skarlia'],
'Sylviria': ['sylviria', 'silver peninsula', 'tsp', 'silver'],
'Milhelm Council': ['milhelm', 'milhelm council','thornian council', 'thornian', 'mc'],
'Ramchatca': ['ramchatca','thrusk', 'tr'],
'Tiamats Eye': ['tiamats eye', 'tiamat', 'te', 'eye'],
'Etelkoz': ['etelkoz','united hordes of sinios', 'sinios'],
'Amberstone': ['amberstone','venuvia', 'as'],
'Glimmhammer': ['glimmhammer','vurn darul', 'vurn', 'darul'],
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
    'Bachtalan': {'Duronia': 6, 'Tungsten State': 6, 'Zamwall Tribes': 5, 'Kemet': 3},
    'Eisenland': {'Etelkoz': 12, 'Solana': 10, 'Ramchatca': 4, 'Bihar Hordes': 2},
    'Khrobat': {'Kemet': 4, 'Norstraden': 3},
    'Kemet': {'Solana Tribes': 20, 'Tiamats Eye': 10, 'Zamwall Tribes': 5, 'Tungsten State': 5, 'Norstraden': 4, 'Khrobat': 4, 'Bachtalan': 3},
    'Solana': {'Etelkoz': 12, 'Eisenland': 10, 'Glimmhammer': 10, 'Aceria': float('inf')},
    'Solana Tribes': {'Kemet': 20, 'Tungsten State': 15, 'Albalatin Holy State': 12, 'Tiamats Eye': 3},
    'Zamwall Tribes': {'Ramchatca': 13, 'Lunan': 7, 'Kemet': 5, 'Duronia': 5, 'Bachtalan': 5, 'Norstraden': 2},
    'Kingdom of Leonia': {'Sylviria': 5, 'Albalatin Holy State': 1},
    'Twin Kingdoms of Wildhammers': {'Glimmhammer': 7, 'Etelkoz': 6, 'Amberstone': 5, 'Milhelm Council': 4, 'Aceria': float('inf')},
    'Tungsten State': {'Solana Tribes': 15, 'Duronia': 10, 'Bachtalan': 6, 'Kemet': 5, 'Tiamats Eye': 3, 'Albalatin Holy State': 3},
    'Lunan': {'Norstraden': 9, 'Zamwall Tribes': 7, 'Duronia': 6, 'Ramchatca': 5, 'Bihar Hordes': 5},
    'Duronia': {'Etelkoz': 12, 'Everfjord': 11, 'Tungsten State': 10, 'Albalatin Holy State': 10, 'Bihar Hordes': 9, 'Bachtalan': 6, 'Lunan': 6, 'Zamwall Tribes': 5},
    'Norstraden': {'Ramchatca': 15, 'Lunan': 9, 'Kemet': 4, 'Khrobat': 3, 'Zamwall Tribes': 2},
    'Bihar Hordes': {'Duronia': 9, 'Etelkoz': 8, 'Ramchatca': 3, 'Eisenland': 2},
    'Onyxbridge': {'Amberstone': 8, 'Sylviria': 7},
    'Everfjord': {'Duronia': 11, 'Etelkoz': 11, 'Milhelm Council': 2},
    'Albalatin Holy State': {'Solana Tribes': 12, 'Duronia': 10, 'Tiamats Eye': 10, 'Tungsten State': 3, 'Kingdom of Leonia': 1},
    'Sylviria': {'Onyxbridge': 7,'Kingdom of Leonia': 5},
    'Milhelm Council': {'Etelkoz': 6,'Amberstone': 5,'Twin Kingdoms of Wildhammers': 4,'Everfjord': 2},'Ramchatca': {'Norstraden': 15,'Zamwall Tribes': 13,'Lunan': 5,'Eisenland': 4,'Duronia': 3},
    'Tiamats Eye': {'Kemet': 10,'Albalatin Holy State': 10,'Tungsten State': 3,'Solana Tribes': 3},
    'Etelkoz': {'Duronia': 12,'Eisenland': 12,'Solana': 12,'Everfjord': 11,'Bihar Hordes': 8,'Milhelm Council': 6,'Glimmhammer': 4},
    'Amberstone': {'Onyxbridge': 8,'Milhelm Council': 5,'Twin Kingdoms of Wildhammers': 5, 'Aceria': float('inf')},
    'Glimmhammer': {'Solana': 10,'Twin Kingdoms of Wildhammers': 7,'Etelkoz': 4, 'Aceria': float('inf')},
    'Aceria': {'Amberstone': 13, 'Twin Kingdoms of Wildhammers': 8, 'Glimmhammer': 4, 'Solana': 7}
}
region_names = list(graph.keys())

def increment_counter(Auth):
    url = "https://api.avrae.io/customizations/gvars/6145e081-f9d9-4a1e-9b65-fb9be71ee04e"  # Replace with the actual API endpoint URL
    headers = {
        "Authorization": Auth,  # Replace with your actual auth token
        "Content-Type": "application/json"
    }   

    # Load previous value from a file or set it to 0 if the file doesn't exist
    value = 0
    filename = "value.txt"
    print("Checkpoint")
    if os.path.exists("C:/Users/frede/PycharmProjects/DiscordTimeBot/value.txt"):
        with open("C:/Users/frede/PycharmProjects/DiscordTimeBot/value.txt", "r") as file:
            value = int(file.read())
            print(value)
    else:
        print("FUCK")
        exit()

    # Increment the value
    value += 1

    payload = {
        "_id": {"$oid": "64626cb79fa1ec99aa9e563a"},
        "owner": "405057667422486528",
        "key": "6145e081-f9d9-4a1e-9b65-fb9be71ee04e",
        "owner_name": "Arcane The Person#6031",
        "value": str(value),
        "editors": []
    }
    print("Got so far")
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("POST request successful!")
    else:
        print("POST request failed with status code:", response.status_code)
        print("Response content:", response.content.decode())

    # Save the updated value to the file
    with open(filename, "w") as file:
        file.write(str(value))