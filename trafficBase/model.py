from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import Car, Traffic_Light, Destination, Obstacle, Road
import json
import random
from grafo import graph as graph_list  # Importing the graph

class CityModel(Model):
    def __init__(self, N):
        # Load the map dictionary mapping characters in the map file to corresponding agents
        dataDictionary = json.load(open("city_files/mapDictionary.json"))

        self.traffic_lights = []

        # Load the map file. Each character in the map file represents an agent.
        with open('city_files/2023_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0]) - 1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = RandomActivation(self)

            # Iterate over each character in the map file and create the corresponding agent
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, state=(col != "S"), timeToChange=int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)

        self.map_directions = {
            "Right": [(1, 0)],
            "Left": [(-1, 0)],
            "Up": [(0, -1)],
            "Down": [(0, 1)]
        }

        self.num_agents = N
        self.running = True

        # Initialize a counter for car IDs
        self.car_counter = 0

        # Add the first car in a random corner
        start_pos = random.choice([(0, 0), (0, self.height - 1), (self.width - 1, 0), (self.width - 1, self.height - 1)])
        car = Car(f"car_{self.car_counter}", self)
        self.grid.place_agent(car, start_pos)
        self.schedule.add(car)
        self.car_counter += 1

        # Use the imported graph
        self.graph_list = graph_list
        self.graph = self.build_graph(self.graph_list)

    def build_graph(self, graph_list):
        graph = {}
        for start, end in graph_list:
            if start not in graph:
                graph[start] = []
            graph[start].append(end)
        return graph

    def step(self):
        ''' Advance the model by one step. '''
        self.schedule.step()

        # Add a new car every 15 steps
        if self.schedule.steps % 4 == 0:
            new_car_id = f"car_{self.car_counter}"
            self.car_counter += 1

            new_car = Car(new_car_id, self)
            start_pos = random.choice([(0, 0), (0, self.height - 1), (self.width - 1, 0), (self.width - 1, self.height - 1)])
            self.grid.place_agent(new_car, start_pos)
            self.schedule.add(new_car)

# Rest of your server.py file remains the same
