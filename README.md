# Maze Pathfinding Robot Simulation (Python)

A console-based Python application that generates a random maze and finds the minimum-cost path for a robot to reach an exit using **Dijkstra’s algorithm**.

---

##  Description

This project simulates a robot navigating inside an `n x n` maze. The maze contains obstacles, toll cells, and two exits. The robot must find the **lowest-cost path** to reach one of the exits.

The maze is generated randomly based on user-defined parameters.

---

## Features

- Implementation of **Dijkstra's Algorithm**
- Random maze generation
- Blocked cells (`X`)
- Toll cells (`T`) with higher movement cost
- Robot starting from the center (`R`)
- Two exits (`E`)
- Path cost calculation
- Path length calculation
- Input validation
- Clean object-oriented design

---

## How It Works

The program:

1. Asks the user for:
   - Maze size `n` (even number ≥ 4)
   - Percentage of blocked cells (`X`)
   - Percentage of toll cells (`T`)

2. Generates a random maze

3. Places:
   - `R` → Robot (center area)
   - `E` → Exits (top-left & bottom-right)
   - `X` → Obstacles
   - `T` → Toll cells

4. Uses **Dijkstra's algorithm** to find the minimum-cost path

5. Displays:
   - The generated maze
   - The shortest path using `*`
   - Total cost
   - Path length

---

##  Maze Symbols

| Symbol | Meaning |
|--------|--------|
| `R` | Robot (start position) |
| `E` | Exit |
| `X` | Blocked cell (cannot pass) |
| `T` | Toll cell (cost = 2) |
| `.` | Free cell (cost = 1) |
| `*` | Final path |

---

## Movement Cost

- Moving to a **free cell (`.`)** → cost = **1**
- Moving to a **toll cell (`T`)** → cost = **2**
- Moving through **blocked cells (`X`)** → Not allowed

---

## Input Example
```bash
Enter maze size n (even number ≥ 4): 6
Enter blocked cells percentage px (%): 20
Enter toll cells percentage pt (%): 15
```

---

## Output Example

```bash
Generated maze:
E . X . T .
. X . . . .
. . T R X .
. . . . . .
. T . X . .
. . . . . E

Shortest path found:
E * X . T .
. X * * * .
. . T R X .
. . . . . .
. T . X . .
. . . . . E

Total cost: 6
Path length: 5
```

---

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Dijkstra's Algorithm
- Priority Queue (`heapq`)
- Random Maze Generation (`random` module)

---

## How to Run

1. Make sure you have Python installed (version 3.x)

2. Run the program locally:


```bash
python maze-pathfinding-simulator.py
```

---

## Constraints
- Maze size must be:
   - Even number
   - Greater than or equal to 4
- Percentages must be:
   - Between 0 and 100
---

 ## Future Improvements
- Add graphical interface (GUI)
- Add colored terminal output
- Add animation for robot movement
- Support multiple pathfinding algorithms (BFS, A*)
- Save/load maze from file
-  Performance comparison between algorithms
--- 

## Author
Eirini Markantoni


