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
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
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
            self._obstacle_list = obstacle_list
        else:
            self._obstacle_list = []
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
        for human in self._human_list:
            yield human

        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        # Create a new grid visited of the same size as the original grid 
        # and initialize its cells to be empty.
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        for obstacle in self._obstacle_list:
            visited.set_full(obstacle[0], obstacle[1])
        
        # Create a 2D list of the same size as the original grid 
        # and initialize each of its entries to be the product of the height times the width of the grid.
        distance_field = [[self._grid_height * self._grid_width for dummy_c in range(self._grid_width)]
                          for dummy_r in range(self._grid_height)]
        
        # Create a queue boundary that is a copy of either the zombie list or the human list. 
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            list_type = self._zombie_list
        if entity_type == HUMAN:
            list_type = self._human_list
            
        # For cells in the queue, initialize visited to be FULL and distance_field to be zero.
        for item in list_type:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0
        
        # Implement a modified version of the BFS search
        while boundary:
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0], cell[1])
            for resident in neighbors:
                if visited.is_empty(resident[0], resident[1]):
                    distance_field[resident[0]][resident[1]] = min(distance_field[resident[0]][resident[1]],
                                                                   distance_field[cell[0]][cell[1]] + 1)
                    visited.set_full(resident[0], resident[1])
                    boundary.enqueue(resident)                               

        return distance_field      
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        temp_human_list = []
        for human in self.humans():
            neighbors = self.eight_neighbors(human[0], human[1])
            # store current position
            distance = [zombie_distance[human[0]][human[1]]]
            location = [human]
            
            for resident in neighbors:
                if self.is_empty(resident[0], resident[1]):
                    # and store rest of 8 other positions if not occupied
                    distance.append(zombie_distance[resident[0]][resident[1]])
                    location.append(resident)
            # find the current safest location, move there        
            safest = location[distance.index(max(distance))]          
            self.set_empty(human[0], human[1])
            temp_human_list.append(safest)
            
        self._human_list = temp_human_list

    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        temp_zombie_list = []
        #for zombie in self.zombies():
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            # store current position
            distance = [human_distance[zombie[0]][zombie[1]]]
            location = [zombie]
            
            for resident in neighbors:
                if self.is_empty(resident[0], resident[1]):
                    # and store rest of 4 other positions if not occupied
                    distance.append(human_distance[resident[0]][resident[1]])
                    location.append(resident)
            # find the current most closest location, move there  
            closest = location[distance.index(min(distance))]          
            self.set_empty(zombie[0], zombie[1])
            temp_zombie_list.append(closest)
            
        self._zombie_list = temp_zombie_list
        
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))

