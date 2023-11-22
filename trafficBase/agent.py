from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from mesa import Agent
import random

class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.destination = self.choose_random_destination()  


    def move(self):
        

        # Convertir la cuadrícula de Mesa a una cuadrícula para A*
        grid_matrix = []
        for y in range(self.model.grid.height):
            row = []
            for x in range(self.model.grid.width):
                cell_contents = self.model.grid.get_cell_list_contents((x, y))
                obstacle = any(isinstance(agent, Obstacle) for agent in cell_contents)
                row.append(0 if obstacle else 1)
            grid_matrix.append(row)

    
        grid = Grid(matrix=grid_matrix)  # Crear el objeto Grid

        # print("Matriz del Grid:")
        # for row in grid_matrix:
        #     print(' '.join(str(cell) for cell in row))


        # Iniciar y destino fijo
        start = grid.node(*self.pos)
        end = grid.node(self.destination[0],self.destination[1])


        # print("Coche esta en:")
        # print(self.pos[1])
        # print(self.pos[0])
        # print("Destino esta en:")
        # print(self.destination[1])
        # print(self.destination[0])


         # Asegúrate de que tanto start como end no estén en obstáculos
        # if grid_matrix[self.pos[1]][self.pos[0]] == 0:
        #     print("El inicio está en un obstáculo")
        # if grid_matrix[self.destination[1]][self.destination[0]] == 0:
        #     print("El destino está en un obstáculo")
        #     return



        # A* Finder
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, _ = finder.find_path(start, end, grid)
 
        for node in path:
            print(f"{node.x} , {node.y}", end=" - ")


        # Imprimir la ruta generada
        print("Ruta generada por A*:", path)
        print(grid.grid_str(path=path, start=start, end=end))


        # Mover a la siguiente posición en el camino
        if path and len(path) > 1:
            next_position = path[1]  # El segundo elemento es el siguiente paso
            self.model.grid.move_agent(self, next_position)




    def choose_random_destination(self):
        destinations = [agent.pos for agent in self.model.schedule.agents 
                        if isinstance(agent, Destination)]
        # print("Destinos disponibles:", destinations)  # Para depuración
        chosen_destination = random.choice(destinations) if destinations else None
        print("Destino elegido:", chosen_destination)  # Nueva línea de depuración
        return chosen_destination



    def step(self):
        self.move()
        if self.pos == self.destination:
            self.model.running = False  # Detiene la simulación



            

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
