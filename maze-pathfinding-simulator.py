import random
import heapq


class Maze:
    """
    The Maze class represents the entire maze

    Contains:
    - the size of the maze
    - the grid/table
    - the robot's position
    - the exits
    - the obstacles
    - the toll cells
    - the path that will be found
    """

    def __init__(self, size, blocked_percentage, toll_percentage):
        """
        Constructor of the Maze class

        Executed when we create a Maze object

        Parameters:
        size: maze size n x n
        blocked_percentage: percentage of cells that will be obstacles
        toll_percentage: percentage of cells that will be toll cells
        """

        self.size = size
        self.blocked_percentage = blocked_percentage
        self.toll_percentage = toll_percentage

        # We create a size x size grid filled with "."
        # The "." means the cell is free
        self.grid = [["." for _ in range(size)] for _ in range(size)]

        # The exits are located:
        # - top left
        # - bottom right
        self.exits = [(0, 0), (size - 1, size - 1)]

        # The robot's position will be set later
        self.robot = None

        # The final path will be stored here
        self.path = []

        # The total cost of the path will be stored here
        self.total_cost = 0

    def generate(self):
        """
        Creates the entire maze

        The order is important:
        1. First we place the exits
        2. We place the robot
        3. We place the obstacles
        4. We place the toll cells

        This way we avoid placing an obstacle on top of an exit or the robot
        """

        self._place_exits()
        self._place_robot()
        self._place_blocked_cells()
        self._place_toll_cells()

    def _place_exits(self):
        """
        Places the exits in the maze

        We use the letter E for Exit
        """

        for row, col in self.exits:
            self.grid[row][col] = "E"

    def _place_robot(self):
        """
        Places the robot randomly in one of the 4 central cells

        Because n is even, there is no single central cell
        There are 4 central cells
        """

        mid = self.size // 2

        # The 4 central cells of an even n x n grid
        possible_positions = [
            (mid - 1, mid - 1),
            (mid - 1, mid),
            (mid, mid - 1),
            (mid, mid)
        ]

        # We randomly choose one of the 4 positions
        self.robot = random.choice(possible_positions)

        # We place R in the grid so the robot is visible
        row, col = self.robot
        self.grid[row][col] = "R"

    def _get_available_cells(self):
        """
        Returns all cells where obstacles are allowed to be placed

        We are not allowed to place an obstacle:
        - on the exits
        - on the robot's position
        """

        unavailable = set(self.exits)
        unavailable.add(self.robot)

        available = []

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in unavailable:
                    available.append((row, col))

        return available

    def _place_blocked_cells(self):
        """
        Randomly places obstacles in the maze

        Obstacles are represented with X
        The robot cannot pass through them
        """

        available = self._get_available_cells()

        # We calculate how many obstacles need to be placed
        total_blocked = int(len(available) * self.blocked_percentage / 100)

        # We randomly choose the cells that will become obstacles
        blocked_cells = random.sample(available, total_blocked)

        for row, col in blocked_cells:
            self.grid[row][col] = "X"

    def _place_toll_cells(self):
        """
        Randomly places toll cells in the maze

        Toll cells are represented with T
        The robot can pass through them,
        but the movement cost is higher
        """

        available = []

        # We place toll cells only on free "." cells
        # We do not place toll cells on exits, the robot, or obstacles
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == ".":
                    available.append((row, col))

        # We calculate how many toll cells need to be placed
        total_tolls = int(len(available) * self.toll_percentage / 100)

        # We randomly choose the toll cell positions
        toll_cells = random.sample(available, total_tolls)

        for row, col in toll_cells:
            self.grid[row][col] = "T"

    def find_shortest_path(self):
        """
        Finds the path with the lowest cost from the robot to an exit

        We use the Dijkstra algorithm

        Why Dijkstra?
        Because not all cells have the same cost:
        - plain cell: cost 1
        - toll cell: cost 2

        So we are not simply looking for the shortest path in steps,
        but the cheapest path in total cost
        """

        start = self.robot

        # distances keeps the smallest cost we have found
        # to reach each cell
        distances = {start: 0}

        # previous keeps track of which cell we came from
        # Used later to reconstruct the path
        previous = {}

        # Priority queue:
        # keeps pairs (cost, cell)
        # always pops the cell with the smallest cost first
        priority_queue = [(0, start)]

        # visited keeps the cells we have already examined
        visited = set()

        while priority_queue:
            # We get the cell with the smallest cost
            current_cost, current_cell = heapq.heappop(priority_queue)

            # If we have already examined it, we ignore it
            if current_cell in visited:
                continue

            visited.add(current_cell)

            # If the current cell is an exit,
            # then we have found the best path to some exit
            if current_cell in self.exits:
                self.total_cost = current_cost
                self.path = self._reconstruct_path(previous, current_cell)
                return True

            # We check all neighbors of the current cell
            for neighbor in self._get_neighbors(current_cell):
                move_cost = self._get_cell_cost(neighbor)
                new_cost = current_cost + move_cost

                # If we have not seen the neighbor before
                # or we found a better cost to reach it,
                # we update our data structures
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_cell
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        # If the priority queue ends without finding an exit,
        # it means there is no available path
        return False

    def _get_neighbors(self, cell):
        """
        Returns the valid neighbors of a cell

        The robot can only move:
        - up
        - down
        - left
        - right

        Diagonal movement is not allowed
        """

        row, col = cell

        directions = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1)    # right
        ]

        neighbors = []

        for d_row, d_col in directions:
            new_row = row + d_row
            new_col = col + d_col

            # We keep only the cells that are within bounds
            # and are not obstacles
            if self._is_valid_cell(new_row, new_col):
                neighbors.append((new_row, new_col))

        return neighbors

    def _is_valid_cell(self, row, col):
        """
        Checks if a cell is valid

        A cell is valid if:
        - it is within the bounds of the grid
        - it is not an obstacle X
        """

        if row < 0 or row >= self.size:
            return False

        if col < 0 or col >= self.size:
            return False

        if self.grid[row][col] == "X":
            return False

        return True

    def _get_cell_cost(self, cell):
        """
        Returns the movement cost to a cell

        If the cell is T, it has cost 2
        All other allowed cells have cost 1
        """

        row, col = cell

        if self.grid[row][col] == "T":
            return 2

        return 1

    def _reconstruct_path(self, previous, end_cell):
        """
        Reconstructs the path from the exit back to the robot

        Dijkstra stores for each cell where we came from
        So we start from the exit and go backwards
        until we reach the robot
        """

        path = []
        current = end_cell

        while current in previous:
            path.append(current)
            current = previous[current]

        # We also add the robot's position
        path.append(self.robot)

        # Because the path was built in reverse,
        # we reverse it
        path.reverse()

        return path

    def print_maze(self):
        """
        Prints the maze as it was generated
        """

        for row in self.grid:
            print(" ".join(row))

    def print_maze_with_path(self):
        """
        Prints the maze along with the final path

        The path is displayed with "*"
        We do not change R and E so that the start
        and exits are clearly visible
        """

        # We create a copy of the grid
        # We do not want to modify the original maze
        display_grid = [row[:] for row in self.grid]

        for row, col in self.path:
            if display_grid[row][col] not in ["R", "E"]:
                display_grid[row][col] = "*"

        for row in display_grid:
            print(" ".join(row))
    
    

def read_even_size():
    """
    Reads the maze size from the user

    n must:
    - be an integer
    - be even
    - be at least 4
    """

    while True:
        try:
            size = int(input("Enter maze size n (even number ≥ 4, e.g. 6, 8, 10): "))

            if size >= 4 and size % 2 == 0:
                return size

            print("Invalid input. Please enter an EVEN number ≥ 4.")

        except ValueError:
            print("Invalid input. Please enter an integer.")


def read_percentage(message):
    """
    Reads a percentage from the user

    The percentage must be a number from 0 to 100
    Used for:
    - obstacle percentage
    - toll cell percentage
    """

    while True:
        try:
            percentage = float(input(message))

            if 0 <= percentage <= 100:
                return percentage

            print("Invalid percentage. Please enter a value from 0 to 100.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """
    Main function of the program

    Here the project execution takes place:
    1. We read data from the user
    2. We create the maze
    3. We print the maze
    4. We find the best path
    5. We print the result
    """

    print("===================================")
    print(" Maze Pathfinding Robot Simulation ")
    print("===================================")
    print("Note: The maze size must be EVEN so the robot can start")
    print("randomly in one of the four central cells.\n")

    size = read_even_size()
    blocked_percentage = read_percentage("Enter blocked cells percentage px (%): ")
    toll_percentage = read_percentage("Enter toll cells percentage pt (%): ")

    # We create a Maze object
    maze = Maze(size, blocked_percentage, toll_percentage)

    # We generate the maze based on the parameters we provided
    maze.generate()

    print("\nGenerated maze:")
    maze.print_maze()

    # We run Dijkstra to find the path
    found = maze.find_shortest_path()

    if found:
        print("\nShortest path found:")
        maze.print_maze_with_path()

        print("\nTotal cost:", maze.total_cost)
        print("Path length:", len(maze.path) - 1)
    else:
        print("\nNo path found from robot to an exit.")


# This means that main() will only be executed when
# we run this file directly
if __name__ == "__main__":
    main()
