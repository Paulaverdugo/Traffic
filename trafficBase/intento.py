# Map data

traffic_light_moves= [
    # From > to s
    [28,29],
    # From s/S to >
    [29,30],

    [4,5], [5,6],

    [35,36], [36,37],

    [11,12], [12,13],

    [78,54], [54,30],

    [79,55], [55,31],

    [85,61], [61,37],

    [86,62], [62,38],

    [166,190], [190,214],

    [167,191], [191,215],

    [212,213], [213,214],

    [236,237], [237,238],

    [291,290], [290,289],

    [267,266], [266,265],

    [336,312], [312,288],

    [337,313], [313,289],

    [366,390], [390,414],

    [367,391], [391,415],

    [441,440], [440,439],

    [417,416], [416,415],

    [520,544], [544,568],

    [521,545], [545,569],

    [595,594], [594,593],

    [571,570], [570,569]
]


get_to_Destination = [
    # From > to D
    [102,101], [109,108], [43,67], [142,141], [202,178], [361,362], [373,372], [353,354], [435,459], [493,492], [497, 498], [550, 549], [555,531]
]

# Map data
map_data = [
    "v<<<<<<<<<<<<<<<<<s<<<<<",
    "v<<<<<<<<<<<<<<<<<s<<<<^",
    "vv#D#########vv#SS###D^^",
    "vv###########vv#^^####^^",
    "vv##########Dvv#^^D###^^",
    "vv#D#########vv#^^####^^",
    "vv<<<<<<s<<<<vv#^^####^^",
    "vv<<<<<<s<<<<vv#^^####^^",
    "vv####SS#####vv#^^####^^",
    "vvD##D^^####Dvv#^^####^^",
    "vv####^^#####vv#^^D###^^",
    "SS####^^#####vv#^^####^^",
    "vvs<<<<<<<<<<<<<<<<<<<<<",
    "vvs<<<<<<<<<<<<<<<<<<<<<",
    "vv##########vv###^^###^^",
    "vv>>>>>>>>>>>>>>>>>>>s^^",
    "vv>>>>>>>>>>>>>>>>>>>s^^",
    "vv####vv##D##vv#^^####SS",
    "vv####vv#####vv#^^####^^",
    "vv####vv#####vv#^^###D^^",
    "vv###Dvv####Dvv#^^####^^",
    "vv####vv#####vv#^^####^^",
    "vv####SS#####SS#^^#D##^^",
    "v>>>>s>>>>>>s>>>>>>>>>>^",
    ">>>>>s>>>>>>s>>>>>>>>>>^"
]

# Dictionary to interpret symbols
symbol_interpretation = {
    ">": "Right",
    "<": "Left",
    "S": 15,
    "s": 7,
    "#": "Obstacle",
    "v": "Down",
    "^": "Up",
    "D": "Destination"
}

# Helper function to get the neighbor of a cell based on the direction
def get_neighbor(row, col, direction):
    neighbors = []
    if direction in ["Right", "Left", "Down", "Up"]:
        single_direction = {"Right": (0, 1), "Left": (0, -1), "Down": (1, 0), "Up": (-1, 0)}
        dr, dc = single_direction[direction]
        neighbors.append((row + dr, col + dc))
    if direction in ["Right", "Down"]:
        neighbors.append((row + 1, col + 1))  # Diagonal down-right
    if direction in ["Left", "Down"]:
        neighbors.append((row + 1, col - 1))  # Diagonal down-left
    if direction in ["Right", "Up"]:
        neighbors.append((row - 1, col + 1))  # Diagonal up-right
    if direction in ["Left", "Up"]:
        neighbors.append((row - 1, col - 1))  # Diagonal up-left
    return neighbors

# ... [Previous parts of the script] ...

# Creating the graph
graph = []
for row in range(len(map_data)):
    row2 = 24 - row  # Invert the row index
    for col in range(len(map_data[row])):
        cell = map_data[row][col]
        if cell not in ['#', 'D']:  # Skip obstacles and destinations
            node_id = row2 * len(map_data[row]) + col  # Unique ID for each cell

            # Determine the allowed direction and the neighbors
            if cell in ['>', '<', 'v', '^']:
                direction = symbol_interpretation[cell]
                neighbors = get_neighbor(row, col, direction)
                for neighbor in neighbors:
                    if 0 <= neighbor[0] < len(map_data) and 0 <= neighbor[1] < len(map_data[row]):
                        neighbor_cell = map_data[neighbor[0]][neighbor[1]]
                        if neighbor_cell not in ['#', 'D']:  # If not an obstacle or a destination
                            neighbor_id = (24-neighbor[0]) * len(map_data[row]) + neighbor[1]
                            graph.append([node_id, neighbor_id])

# Adding traffic light moves and get to destination moves to the graph
graph.extend(traffic_light_moves)
graph.extend(get_to_Destination)

# Removing duplicates from the graph and converting to lists
graph = list(set(tuple(edge) for edge in graph))
graph_as_lists = [list(edge) for edge in graph]

# Printing the graph
print("graph =", sorted(graph_as_lists))
