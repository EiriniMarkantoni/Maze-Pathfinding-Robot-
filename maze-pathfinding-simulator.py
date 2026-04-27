import random
import heapq


class Maze:
    """
    Η κλάση Maze αναπαριστά ολόκληρο τον λαβύρινθο

    Περιέχει:
    - το μέγεθος του λαβυρίνθου
    - τον πίνακα/grid
    - τη θέση του ρομπότ
    - τις εξόδους
    - τα εμπόδια
    - τα διόδια
    - το μονοπάτι που θα βρεθεί
    """

    def __init__(self, size, blocked_percentage, toll_percentage):
        """
        Constructor της κλάσης Maze

        Εκτελείται όταν δημιουργούμε ένα αντικείμενο Maze

        Παράμετροι:
        size: μέγεθος λαβυρίνθου n x n
        blocked_percentage: ποσοστό κελιών που θα είναι εμπόδια
        toll_percentage: ποσοστό κελιών που θα είναι διόδια
        """

        self.size = size
        self.blocked_percentage = blocked_percentage
        self.toll_percentage = toll_percentage

        # Δημιουργούμε έναν πίνακα size x size γεμάτο με "."
        # Το "." σημαίνει ότι το κελί είναι ελεύθερο
        self.grid = [["." for _ in range(size)] for _ in range(size)]

        # Οι έξοδοι βρίσκονται:
        # - πάνω αριστερά
        # - κάτω δεξιά
        self.exits = [(0, 0), (size - 1, size - 1)]

        # Η θέση του ρομπότ θα οριστεί αργότερα
        self.robot = None

        # Εδώ θα αποθηκευτεί το τελικό μονοπάτι
        self.path = []

        # Εδώ θα αποθηκευτεί το συνολικό κόστος του μονοπατιού
        self.total_cost = 0

    def generate(self):
        """
        Δημιουργεί ολόκληρο τον λαβύρινθο

        Η σειρά είναι σημαντική:
        1. Βάζουμε πρώτα τις εξόδους
        2. Βάζουμε το ρομπότ
        3. Βάζουμε τα εμπόδια
        4. Βάζουμε τα διόδια

        Έτσι αποφεύγουμε να μπει εμπόδιο πάνω σε έξοδο ή πάνω στο ρομπότ
        """

        self._place_exits()
        self._place_robot()
        self._place_blocked_cells()
        self._place_toll_cells()

    def _place_exits(self):
        """
        Τοποθετεί τις εξόδους στον λαβύρινθο

        Χρησιμοποιούμε το γράμμα E για Exit
        """

        for row, col in self.exits:
            self.grid[row][col] = "E"

    def _place_robot(self):
        """
        Τοποθετεί το ρομπότ τυχαία σε ένα από τα 4 κεντρικά κελιά

        Επειδή το n είναι ζυγό, δεν υπάρχει ένα μόνο κεντρικό κελί
        Υπάρχουν 4 κεντρικά κελιά
        """

        mid = self.size // 2

        # Τα 4 κεντρικά κελιά ενός ζυγού n x n πίνακα
        possible_positions = [
            (mid - 1, mid - 1),
            (mid - 1, mid),
            (mid, mid - 1),
            (mid, mid)
        ]

        # Επιλέγουμε τυχαία μία από τις 4 θέσεις
        self.robot = random.choice(possible_positions)

        # Βάζουμε το R στο grid για να φαίνεται το ρομπότ
        row, col = self.robot
        self.grid[row][col] = "R"

    def _get_available_cells(self):
        """
        Επιστρέφει όλα τα κελιά στα οποία επιτρέπεται να τοποθετηθούν εμπόδια

        Δεν επιτρέπεται να βάλουμε εμπόδιο:
        - στις εξόδους
        - στη θέση του ρομπότ
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
        Τοποθετεί τυχαία εμπόδια στον λαβύρινθο

        Τα εμπόδια συμβολίζονται με X
        Το ρομπότ δεν μπορεί να περάσει μέσα από αυτά
        """

        available = self._get_available_cells()

        # Υπολογίζουμε πόσα εμπόδια πρέπει να τοποθετηθούν
        total_blocked = int(len(available) * self.blocked_percentage / 100)

        # Επιλέγουμε τυχαία τα κελιά που θα γίνουν εμπόδια
        blocked_cells = random.sample(available, total_blocked)

        for row, col in blocked_cells:
            self.grid[row][col] = "X"

    def _place_toll_cells(self):
        """
        Τοποθετεί τυχαία διόδια στον λαβύρινθο

        Τα διόδια συμβολίζονται με T
        Το ρομπότ μπορεί να περάσει από αυτά,
        αλλά το κόστος μετακίνησης είναι μεγαλύτερο
        """

        available = []

        # Διόδια βάζουμε μόνο σε ελεύθερα κελιά "."
        # Δεν βάζουμε διόδια πάνω σε έξοδο, ρομπότ ή εμπόδιο
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == ".":
                    available.append((row, col))

        # Υπολογίζουμε πόσα διόδια πρέπει να μπουν
        total_tolls = int(len(available) * self.toll_percentage / 100)

        # Επιλέγουμε τυχαία τα κελιά των διοδίων
        toll_cells = random.sample(available, total_tolls)

        for row, col in toll_cells:
            self.grid[row][col] = "T"

    def find_shortest_path(self):
        """
        Βρίσκει το μονοπάτι με το μικρότερο κόστος από το ρομπότ προς μία έξοδο

        Χρησιμοποιούμε τον αλγόριθμο Dijkstra

        Γιατί Dijkstra;
        Επειδή δεν έχουν όλα τα κελιά ίδιο κόστος:
        - απλό κελί: κόστος 1
        - κελί διοδίων: κόστος 2

        Άρα δεν ψάχνουμε απλά το συντομότερο μονοπάτι σε βήματα,
        αλλά το φθηνότερο μονοπάτι σε συνολικό κόστος
        """

        start = self.robot

        # Το distances κρατάει το μικρότερο κόστος που έχουμε βρει
        # για να φτάσουμε σε κάθε κελί
        distances = {start: 0}

        # Το previous κρατάει από ποιο κελί ήρθαμε
        # Χρησιμοποιείται μετά για να ξαναφτιάξουμε το μονοπάτι
        previous = {}

        # Priority queue:
        # κρατάει ζεύγη (κόστος, κελί)
        # πάντα βγάζει πρώτο το κελί με το μικρότερο κόστος
        priority_queue = [(0, start)]

        # Το visited κρατάει τα κελιά που έχουμε ήδη εξετάσει
        visited = set()

        while priority_queue:
            # Παίρνουμε το κελί με το μικρότερο κόστος
            current_cost, current_cell = heapq.heappop(priority_queue)

            # Αν το έχουμε ήδη εξετάσει, το αγνοούμε
            if current_cell in visited:
                continue

            visited.add(current_cell)

            # Αν το τρέχον κελί είναι έξοδος,
            # τότε βρήκαμε το καλύτερο μονοπάτι προς κάποια έξοδο
            if current_cell in self.exits:
                self.total_cost = current_cost
                self.path = self._reconstruct_path(previous, current_cell)
                return True

            # Ελέγχουμε όλους τους γείτονες του τρέχοντος κελιού
            for neighbor in self._get_neighbors(current_cell):
                move_cost = self._get_cell_cost(neighbor)
                new_cost = current_cost + move_cost

                # Αν δεν έχουμε ξαναδεί τον γείτονα
                # ή βρήκαμε καλύτερο κόστος προς αυτόν,
                # ενημερώνουμε τις δομές μας
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_cell
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        # Αν τελειώσει η priority queue χωρίς να βρούμε έξοδο,
        # σημαίνει ότι δεν υπάρχει διαθέσιμο μονοπάτι
        return False

    def _get_neighbors(self, cell):
        """
        Επιστρέφει τους έγκυρους γείτονες ενός κελιού

        Το ρομπότ μπορεί να κινηθεί μόνο:
        - πάνω
        - κάτω
        - αριστερά
        - δεξιά

        Δεν επιτρέπεται διαγώνια κίνηση
        """

        row, col = cell

        directions = [
            (-1, 0),  # πάνω
            (1, 0),   # κάτω
            (0, -1),  # αριστερά
            (0, 1)    # δεξιά
        ]

        neighbors = []

        for d_row, d_col in directions:
            new_row = row + d_row
            new_col = col + d_col

            # Κρατάμε μόνο τα κελιά που είναι μέσα στα όρια
            # και δεν είναι εμπόδια
            if self._is_valid_cell(new_row, new_col):
                neighbors.append((new_row, new_col))

        return neighbors

    def _is_valid_cell(self, row, col):
        """
        Ελέγχει αν ένα κελί είναι έγκυρο

        Ένα κελί είναι έγκυρο αν:
        - βρίσκεται μέσα στα όρια του πίνακα
        - δεν είναι εμπόδιο X
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
        Επιστρέφει το κόστος μετακίνησης προς ένα κελί

        Αν το κελί είναι T, έχει κόστος 2
        Όλα τα υπόλοιπα επιτρεπτά κελιά έχουν κόστος 1
        """

        row, col = cell

        if self.grid[row][col] == "T":
            return 2

        return 1

    def _reconstruct_path(self, previous, end_cell):
        """
        Ξαναφτιάχνει το μονοπάτι από την έξοδο προς το ρομπότ

        Ο Dijkstra αποθηκεύει για κάθε κελί από πού ήρθαμε
        Άρα ξεκινάμε από την έξοδο και πηγαίνουμε προς τα πίσω
        μέχρι να φτάσουμε στο ρομπότ
        """

        path = []
        current = end_cell

        while current in previous:
            path.append(current)
            current = previous[current]

        # Προσθέτουμε και τη θέση του ρομπότ
        path.append(self.robot)

        # Επειδή το μονοπάτι φτιάχτηκε ανάποδα,
        # το αντιστρέφουμε
        path.reverse()

        return path

    def print_maze(self):
        """
        Εκτυπώνει τον λαβύρινθο όπως δημιουργήθηκε
        """

        for row in self.grid:
            print(" ".join(row))

    def print_maze_with_path(self):
        """
        Εκτυπώνει τον λαβύρινθο μαζί με το τελικό μονοπάτι

        Το μονοπάτι εμφανίζεται με "*"
        Δεν αλλάζουμε το R και τα E για να φαίνονται καθαρά
        η αρχή και οι έξοδοι
        """

        # Δημιουργούμε αντίγραφο του grid
        # Δεν θέλουμε να αλλάξουμε τον αρχικό λαβύρινθο
        display_grid = [row[:] for row in self.grid]

        for row, col in self.path:
            if display_grid[row][col] not in ["R", "E"]:
                display_grid[row][col] = "*"

        for row in display_grid:
            print(" ".join(row))
    
    

def read_even_size():
    """
    Διαβάζει από τον χρήστη το μέγεθος του λαβυρίνθου

    Το n πρέπει:
    - να είναι ακέραιος
    - να είναι ζυγός
    - να είναι τουλάχιστον 4
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
    Διαβάζει ένα ποσοστό από τον χρήστη

    Το ποσοστό πρέπει να είναι αριθμός από 0 έως 100
    Χρησιμοποιείται για:
    - ποσοστό εμποδίων
    - ποσοστό διοδίων
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
    Κύρια συνάρτηση του προγράμματος

    Εδώ γίνεται η εκτέλεση του project:
    1. Διαβάζουμε δεδομένα από τον χρήστη
    2. Δημιουργούμε τον λαβύρινθο
    3. Τυπώνουμε τον λαβύρινθο
    4. Βρίσκουμε το καλύτερο μονοπάτι
    5. Τυπώνουμε το αποτέλεσμα
    """

    print("===================================")
    print(" Maze Pathfinding Robot Simulation ")
    print("===================================")
    print("Note: The maze size must be EVEN so the robot can start")
    print("randomly in one of the four central cells.\n")

    size = read_even_size()
    blocked_percentage = read_percentage("Enter blocked cells percentage px (%): ")
    toll_percentage = read_percentage("Enter toll cells percentage pt (%): ")

    # Δημιουργούμε αντικείμενο Maze
    maze = Maze(size, blocked_percentage, toll_percentage)

    # Δημιουργούμε τον λαβύρινθο με βάση τις παραμέτρους που δώσαμε
    maze.generate()

    print("\nGenerated maze:")
    maze.print_maze()

    # Τρέχουμε Dijkstra για να βρούμε το μονοπάτι
    found = maze.find_shortest_path()

    if found:
        print("\nShortest path found:")
        maze.print_maze_with_path()

        print("\nTotal cost:", maze.total_cost)
        print("Path length:", len(maze.path) - 1)
    else:
        print("\nNo path found from robot to an exit.")


# Αυτό σημαίνει ότι η main() θα εκτελεστεί μόνο όταν
# τρέχουμε αυτό το αρχείο απευθείας
if __name__ == "__main__":
    main()