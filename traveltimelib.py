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
    'Albalatin Holy State': ['albalatin', 'albatin holy state', 'skarlian', 'skarlia'],
    'Amberstone': ['amberstone', 'venuvia', 'as'],
    'Bachtalan': ['bachtalan', 'bach', 'talan'],
    'Bihar Hordes': ['bihar hordes', 'bihar', 'bh', 'redhorn'],
    'Duronia': ['duronia', 'duro', 'ol', 'orcish', 'orcish legions'],
    'Eisenland': ['eisenland', 'cortashar', 'cd', 'eisen'],
    'Etelkoz': ['etelkoz', 'united hordes of sinios', 'sinios'],
    'Everfjord': ['everfjord', 'samsara', 'ever'],
    'Glimmhammer': ['glimmhammer', 'vurn darul', 'vurn', 'darul', 'glimm'],
    'Kemet': ['srath', 'des', 'empire', 'kemet'],
    'Khrobat': ['khrobat', 'drk', 'dirk', 'khro', 'bat'],
    'Kingdom of Leonia': ['kingdom of leonia', 'leonia', 'kl', 'everica'],
    'Satharia': ['satharia','lunan', 'lu'],
    'Milhelm Council': ['milhelm', 'milhelm council', 'thornian council', 'thornian', 'mc'],
    'Norstraden': ['norstraden', 'meloz', 'meloz tribe'],
    'Onyxbridge': ['onyxbridge', 'rustvault'],
    'Ramchatca': ['ramchatca', 'thrusk', 'tr'],
    'Solana': ['solana', 'fl', 'leaf', 'farleaf'],
    'Solana Tribes': ['solana tribes', 'solana', 'fw', 'farwing', 'farwing tribes', 'st'],
    'Sylviria': ['sylviria', 'silver peninsula', 'tsp', 'silver'],
    'Tiamats Eye': ['tiamats eye', 'tiamat', 'te', 'eye'],
    'Tungsten State': ['tungsten state', 'kobold', 'kt'],
    'Twin Kingdoms of Wildhammers': ['wildhammer', 'twin kingdoms', 'twin kingdoms of wildhammers', 'gundahn', 'wildhammers'],
    'Zamwall Tribes': ['zamwall tribes', 'zamwall', 'zt', 'snap', 'femur', 'femursnap'],
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
Timegraph = {
    'Aceria': {'Amberstone': 13, 'Twin Kingdoms of Wildhammers': 8, 'Glimmhammer': 4, 'Solana': 7},
    'Albalatin Holy State': {'Solana Tribes': 12, 'Duronia': 10, 'Tiamats Eye': 10, 'Tungsten State': 3, 'Kingdom of Leonia': 1},
    'Amberstone': {'Onyxbridge': 8, 'Milhelm Council': 5, 'Twin Kingdoms of Wildhammers': 5, 'Aceria': float('inf')},
    'Bachtalan': {'Duronia': 6, 'Tungsten State': 6, 'Zamwall Tribes': 5, 'Kemet': 3},
    'Bihar Hordes': {'Duronia': 9, 'Etelkoz': 8, 'Ramchatca': 3, 'Eisenland': 2},
    'Duronia': {'Etelkoz': 12, 'Everfjord': 11, 'Tungsten State': 10, 'Albalatin Holy State': 10, 'Bihar Hordes': 9, 'Bachtalan': 6, 'Satharia': 6, 'Zamwall Tribes': 5},
    'Eisenland': {'Etelkoz': 12, 'Solana': 10, 'Ramchatca': 4, 'Bihar Hordes': 2},
    'Etelkoz': {'Duronia': 12, 'Eisenland': 12, 'Solana': 12, 'Everfjord': 11, 'Bihar Hordes': 8, 'Milhelm Council': 6, 'Glimmhammer': 4},
    'Everfjord': {'Duronia': 11, 'Etelkoz': 11, 'Milhelm Council': 2},
    'Glimmhammer': {'Solana': 10, 'Twin Kingdoms of Wildhammers': 7, 'Etelkoz': 4, 'Aceria': float('inf')},
    'Kemet': {'Solana Tribes': 20, 'Tiamats Eye': 10, 'Zamwall Tribes': 5, 'Tungsten State': 5, 'Norstraden': 4, 'Khrobat': 4, 'Bachtalan': 3},
    'Khrobat': {'Kemet': 4, 'Norstraden': 3},
    'Kingdom of Leonia': {'Sylviria': 5, 'Albalatin Holy State': 1},
    'Milhelm Council': {'Etelkoz': 6, 'Amberstone': 5, 'Twin Kingdoms of Wildhammers': 4, 'Everfjord': 2},
    'Norstraden': {'Ramchatca': 15, 'Satharia': 9, 'Kemet': 4, 'Khrobat': 3, 'Zamwall Tribes': 2},
    'Onyxbridge': {'Amberstone': 8, 'Sylviria': 7},
    'Ramchatca': {'Norstraden': 15, 'Zamwall Tribes': 13, 'Satharia': 5, 'Eisenland': 4, 'Duronia': 3},
    'Satharia': {'Norstraden': 9, 'Zamwall Tribes': 7, 'Duronia': 6, 'Ramchatca': 5, 'Bihar Hordes': 5},
    'Solana': {'Etelkoz': 12, 'Eisenland': 10, 'Glimmhammer': 10, 'Aceria': float('inf')},
    'Solana Tribes': {'Kemet': 20, 'Tungsten State': 15, 'Albalatin Holy State': 12, 'Tiamats Eye': 3},
    'Sylviria': {'Onyxbridge': 7, 'Kingdom of Leonia': 5},
    'Tiamats Eye': {'Kemet': 10, 'Albalatin Holy State': 10, 'Tungsten State': 3, 'Solana Tribes': 3},
    'Tungsten State': {'Solana Tribes': 15, 'Duronia': 10, 'Bachtalan': 6, 'Kemet': 5, 'Tiamats Eye': 3, 'Albalatin Holy State': 3},
    'Twin Kingdoms of Wildhammers': {'Glimmhammer': 7, 'Etelkoz': 6, 'Amberstone': 5, 'Milhelm Council': 4, 'Aceria': float('inf')},
    'Zamwall Tribes': {'Ramchatca': 13, 'Satharia': 7, 'Kemet': 5, 'Duronia': 5, 'Bachtalan': 5, 'Norstraden': 2}
}

Milesgraph = {
    'Aceria': {'Amberstone': 650, 'Twin Kingdoms of Wildhammers': 400, 'Glimmhammer': 200, 'Solana': 350},
    'Albalatin Holy State': {'Solana Tribes': 600, 'Duronia': 500, 'Tiamats Eye': 500, 'Tungsten State': 150, 'Kingdom of Leonia': 50},
    'Amberstone': {'Onyxbridge': 400, 'Milhelm Council': 250, 'Twin Kingdoms of Wildhammers': 250, 'Aceria': float('inf')},
    'Bachtalan': {'Duronia': 300, 'Tungsten State': 300, 'Zamwall Tribes': 250, 'Kemet': 150},
    'Bihar Hordes': {'Duronia': 450, 'Etelkoz': 400, 'Ramchatca': 150, 'Eisenland': 100},
    'Duronia': {'Etelkoz': 600, 'Everfjord': 550, 'Tungsten State': 500, 'Albalatin Holy State': 500, 'Bihar Hordes': 450, 'Bachtalan': 300, 'Satharia': 300, 'Zamwall Tribes': 250},
    'Eisenland': {'Etelkoz': 600, 'Solana': 500, 'Ramchatca': 200, 'Bihar Hordes': 100},
    'Etelkoz': {'Duronia': 600, 'Eisenland': 600, 'Solana': 600, 'Everfjord': 550, 'Bihar Hordes': 400, 'Milhelm Council': 300, 'Glimmhammer': 200},
    'Everfjord': {'Duronia': 550, 'Etelkoz': 550, 'Milhelm Council': 250},
    'Glimmhammer': {'Solana': 500, 'Twin Kingdoms of Wildhammers': 350, 'Etelkoz': 200, 'Aceria': float('inf')},
    'Kemet': {'Solana Tribes': 1000, 'Tiamats Eye': 500, 'Zamwall Tribes': 250, 'Tungsten State': 250, 'Norstraden': 200, 'Khrobat': 200, 'Bachtalan': 150},
    'Khrobat': {'Kemet': 200, 'Norstraden': 150},
    'Kingdom of Leonia': {'Sylviria': 250, 'Albalatin Holy State': 50},
    'Milhelm Council': {'Etelkoz': 300, 'Amberstone': 250, 'Twin Kingdoms of Wildhammers': 200, 'Everfjord': 250},
    'Norstraden': {'Ramchatca': 750, 'Satharia': 450, 'Kemet': 200, 'Khrobat': 150, 'Zamwall Tribes': 100},
    'Onyxbridge': {'Amberstone': 400, 'Sylviria': 350},
    'Ramchatca': {'Norstraden': 750, 'Zamwall Tribes': 650, 'Satharia': 250, 'Eisenland': 200, 'Duronia': 150},
    'Satharia': {'Norstraden': 450, 'Zamwall Tribes': 350, 'Duronia': 300, 'Ramchatca': 250, 'Bihar Hordes': 250},
    'Solana': {'Etelkoz': 600, 'Eisenland': 500, 'Glimmhammer': 500, 'Aceria': float('inf')},
    'Solana Tribes': {'Kemet': 1000, 'Tungsten State': 750, 'Albalatin Holy State': 600, 'Tiamats Eye': 150},
    'Sylviria': {'Onyxbridge': 350, 'Kingdom of Leonia': 250},
    'Tiamats Eye': {'Kemet': 500, 'Albalatin Holy State': 500, 'Tungsten State': 150, 'Solana Tribes': 150},
    'Tungsten State': {'Solana Tribes': 750, 'Duronia': 500, 'Bachtalan': 300, 'Kemet': 250, 'Tiamats Eye': 150, 'Albalatin Holy State': 150},
    'Twin Kingdoms of Wildhammers': {'Glimmhammer': 350, 'Etelkoz': 300, 'Amberstone': 250, 'Milhelm Council': 200, 'Aceria': float('inf')},
    'Zamwall Tribes': {'Ramchatca': 650, 'Satharia': 350, 'Kemet': 250, 'Duronia': 250, 'Bachtalan': 250, 'Norstraden': 100},
}
region_names = list(Timegraph.keys())

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