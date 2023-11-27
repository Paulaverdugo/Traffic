from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.graph import Graph
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.node import Node
import heapq
from mesa import Agent
import random


class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.destination = self.choose_random_destination()
        


    def move(self):
        start_id = self.pos[1] * self.model.grid.width + self.pos[0]
        end_id = self.destination[1] * self.model.grid.width + self.destination[0]
        print(f"Moving from {start_id} to {end_id}")

        path = self.a_star(start_id, end_id)
        print(f"Car {self.unique_id} path: {path}")  # Imprimir camino encontrado

        if path and len(path) > 1:
            next_node_id = path[1]
            next_position = (next_node_id % self.model.grid.width, next_node_id // self.model.grid.width)
            
            # Comprobar si hay un semáforo en la próxima posición
            next_contents = self.model.grid.get_cell_list_contents(next_position)
            traffic_light = next((agent for agent in next_contents if isinstance(agent, Traffic_Light)), None)
            
            # Detenerse si hay un semáforo en rojo
            if traffic_light and not traffic_light.state:
                return

            # Mover el agente a la siguiente posición si no hay semáforo o está en verde
            self.model.grid.move_agent(self, next_position)




    def a_star(self, start, goal):
        print(f"Starting A* from {start} to {goal}")
        def heuristic(node, goal):
            x1, y1 = divmod(node, self.model.grid.width)
            x2, y2 = divmod(goal, self.model.grid.width)
            return abs(x1 - x2) + abs(y1 - y2)  # Distancia Manhattan

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        
        while open_set:
            
            current = heapq.heappop(open_set)[1]
            print(f"Current node: {current}")

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                    print(f"Path found: {path[::-1]}")
                return path[::-1]

            for neighbor in self.model.graph.get(current, []):
                print(f"Checking neighbor: {neighbor}")
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
        print("No path found")
        return None
    
    # def print_grid_identifiers(self):
    #     for y in range(self.model.grid.height):
    #         for x in range(self.model.grid.width):
    #             cell_id = y * self.model.grid.width + x
    #             print(f"Cell ({x}, {y}) has ID: {cell_id}", end='  ')
    #         print()  # Nueva línea después de cada fila


    def choose_random_destination(self):
        destinations = [agent.pos for agent in self.model.schedule.agents if isinstance(agent, Destination)]
        chosen_destination = random.choice(destinations) if destinations else None
        print("Destino elegido:", chosen_destination)  # Imprimir destino elegido
        return chosen_destination

    
    def step(self):
        self.move()
        if self.pos == self.destination:
            self.model.grid.remove_agent(self)  # Elimina el agente
            self.model.schedule.remove(self)    # Elimina el agente del schedule



class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

        # coom este pero para los coches

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
