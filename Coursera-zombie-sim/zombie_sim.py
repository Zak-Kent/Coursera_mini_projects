"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = [] 
        poc_grid.Grid.clear(self)       
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list: 
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for item in self._human_list: 
            yield item 
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        if entity_type == ZOMBIE: 
            piece_list = self._zombie_list
        elif entity_type == HUMAN: 
            piece_list = self._human_list 
        
        # creates a new grid object of the same size as board, with empty cells 
        visited = poc_grid.Grid(self._grid_height, self._grid_width) 
        
        # creates a list with same dim as visited and sets cell values to 
        # a number larger than any possible direct move from one cell to another  
        dist_cell_val = self.get_grid_width() * self.get_grid_height()
        distance_field = [[ dist_cell_val for dummy_col in range(self._grid_width)] 
                            for dummy_row in range(self._grid_height)]
        
        # creating a queue using provided queue class then iterates through 
        # copy of the zombie list and adds zombies to the queue, sets dist
        # at zombie location to 0, sets visited tile to full
        boundry = poc_queue.Queue()
        piece_copy = piece_list
        for item in piece_copy: 
            boundry.enqueue(item)
            distance_field[item[0]][item[1]] = 0 
            visited.set_full(item[0], item[1]) 
            
        while len(boundry) > 0:  
            # while there is something in the boundry queue, take a cell out
            # use the 4 neighbors method to get the cells to search
            cell = boundry.dequeue()
            neighbors = visited.four_neighbors(cell[0], cell[1])
            
            for nbor in neighbors:
                # if the items in the neighbors list haven't been visited and they're free
                # of obstructions, set item to full, enqueue the item, update distance score 
                if visited.is_empty(nbor[0], nbor[1]) and self.is_empty(nbor[0], nbor[1]):
                    visited.set_full(nbor[0], nbor[1])
                    boundry.enqueue((nbor[0], nbor[1]))
                    distance_field[nbor[0]][nbor[1]] = distance_field[cell[0]][cell[1]] + 1 
                    
        return distance_field 
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        # gets a list of neighbors for each human in human list & add current cell  
        for item in self.humans():
            neighbors = self.eight_neighbors(item[0], item[1])
            neighbors.append(item)
            cell_value = 0 
            possible_moves = []
            
            for cell in neighbors:              
                zom_cell = zombie_distance_field[cell[0]][cell[1]]
                # checks the neighboring cells and creates a list of moves, only 
                # adds cells if neighboring cell is farther from zombie & empty
                if cell_value < zom_cell and self.is_empty(cell[0], cell[1]): 
                    cell_value = zom_cell
                    possible_moves = [cell] 
                elif cell_value == zom_cell:
                    possible_moves.append(cell) 
            # chooses move from list, gets index, changes location in human_list   
            human_move = random.choice(possible_moves) 
            idx = self._human_list.index(item)          
            self._human_list[idx] = human_move              
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        # gets a list of neighbors for each zombie in zombie list
        for item in self.zombies():
            neighbors = self.four_neighbors(item[0], item[1])
            neighbors.append(item)
            cell_value = 1000
            possible_moves = []
            
            for cell in neighbors: 
                hum_cell = human_distance_field[cell[0]][cell[1]] 
                # checks the neighboring cells and creates a list of moves, only 
                # adds cells if cell is closer to human(lower value) & empty
                if cell_value > hum_cell and self.is_empty(cell[0], cell[1]):
                    cell_value = hum_cell
                    possible_moves = [cell]
                elif cell_value == hum_cell:
                    possible_moves.append(cell) 

            # chooses move from list, gets index, changes location in zombie_list   
            zombie_move = random.choice(possible_moves) 
            idx = self._zombie_list.index(item)          
            self._zombie_list[idx] = zombie_move  

    

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Apocalypse(30, 40))

 
