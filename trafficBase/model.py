from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import Car, Traffic_Light, Destination, Obstacle, Road
import json
import requests
import random
from grafo import graph as graph_list
from threading import Thread

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
        self.num_agents = N
        self.running = True


        # Add the first car in a random corner
        start_pos = random.choice([(0, 0), (0, self.height - 1), (self.width - 1, 0), (self.width - 1, self.height - 1)])
        
        self.graph_list = graph_list
        self.graph = self.build_graph(self.graph_list)
        
        
        # Add cars
        added = False

        while not added:
            car = Car(f"car_{self.car_counter}", self)
            self.grid.place_agent(car, start_pos)
            start_id = car.pos[1] * car.model.grid.width + car.pos[0]
            end_id = car.destination[1] * car.model.grid.width + car.destination[0]
            path = car.a_star(start_id, end_id)
            if path != None and len(path) > 0:
                car.path = path
                self.schedule.add(car)
                self.car_counter += 1
                added = True
            else:
                self.grid.remove_agent(car)
        

    def build_graph(self, graph_list):
        graph = {}
        for start, end in graph_list:
            if start not in graph:
                graph[start] = []
            graph[start].append(end)
        return graph

    def count_cars(self):
        car_count = 0
        for agent in self.schedule.agents:
            if isinstance(agent, Car):
                car_count += 2
        return car_count
    
    def step(self):
        self.schedule.step()

        if self.running:
            if self.schedule.steps % 100 == 0:
                Thread(target=self.sendData).start()

    
        

        # print(f"Número actual de carros en la simulación: {agent_count}")


        if self.schedule.steps % 10 == 0:
            for _ in range(4):  # Add three cars
                new_car_id = f"car_{self.car_counter}"
                added = False
                start_pos = random.choice([(0, 0), (0, self.height - 1), (self.width - 1, 0), (self.width - 1, self.height - 1)])

                while not added:
                    car = Car(new_car_id, self)
                    self.grid.place_agent(car, start_pos)
                    start_id = car.pos[1] * self.grid.width + car.pos[0]
                    end_id = car.destination[1] * self.grid.width + car.destination[0]
                    path = car.a_star(start_id, end_id)
                    if path is not None and len(path) > 0:
                        car.path = path
                        self.schedule.add(car)
                        self.car_counter += 2
                        added = True
                    else:
                        self.grid.remove_agent(car)

    def count_agents(self):
        """ Cuenta el número total de agentes tipo Car en el modelo. """
        return len([agent for agent in self.schedule.agents if isinstance(agent, Car)])

    def sendData(self):
        """Sends the total number of cars that have ever been in the simulation to the external API."""
        data = {
            "year": 2023,
            "classroom": 302,
            "name": "Dulce y Paula",
            "num_cars": self.car_counter  # Sending the total number of cars ever added
        }

        print("Sending data...", data)

        headers = {
            "Content-Type": "application/json"
        }

        # Sending the data to the external API
        response = requests.post("http://52.1.3.19:8585/api/attempts", json=data, headers=headers)
        print("Response:", response.text)
