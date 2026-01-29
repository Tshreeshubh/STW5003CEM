

📘 ST5003CEM – Artificial Intelligence Portfolio

Module: ST5003CEM – Intelligent Systems
Assessment Type: Algorithm Portfolio & Implementation
Student: [Shreeshubh Thapa]
Student ID: [ 240213 ]
Institution: Softwarica College

⸻

📌 Project Overview

This project is a comprehensive portfolio demonstrating the practical implementation of core Artificial Intelligence algorithms.
Each task focuses on a different problem domain including optimization, graph search, dynamic programming, greedy strategies, multithreading, and GUI-based simulation.

All modules are fully integrated into a centralized Portfolio Runner, allowing the examiner to execute and evaluate each task independently or interactively.



Implemented Tasks
Question 1a – Sensor Hub Optimization

Algorithm: Weiszfeld’s Algorithm
Objective:
Find the geometric median of 2D sensor points to minimize total signal distance.

Concepts Demonstrated:
	•	Iterative optimization
	•	Numerical convergence
	•	Robust handling of singularities
	•	Computational geometry


Question 1b – Traveling Salesperson Problem (TSP)

Algorithm: Simulated Annealing
Objective:
Find a near-optimal tour visiting all cities exactly once.

Concepts Demonstrated:
	•	Metaheuristic optimization
	•	Neighborhood generation (Swap, 2-opt)
	•	Cooling schedules (Exponential, Linear)
	•	Probabilistic acceptance

Question 2 – Strategic Tile Shatter

Algorithm: Interval Dynamic Programming
Objective:
Maximize total points by selecting optimal shattering order.

Concepts Demonstrated:
	•	Optimal substructure
	•	Bottom-up DP
	•	Matrix Chain Multiplication pattern
	•	Time complexity analysis


Question 3 – Service Center Optimization

Algorithm: Greedy DFS on Trees
Objective:
Minimize service centers required to cover all nodes.

Concepts Demonstrated:
	•	Tree traversal
	•	Greedy decision making
	•	Vertex cover logic
	•	Post-order DFS


Question 4 – Smart Energy Grid Optimization

Algorithm: Bounded Knapsack DP + Greedy Hybrid
Objective:
Optimize energy allocation across multiple sources and districts with tolerance.

Concepts Demonstrated:
	•	Resource modeling
	•	Dynamic programming optimization
	•	Approximate constraint handling
	•	Statistical performance tracking


Question 5a – Emergency Network Simulator (GUI)

Algorithms:
	•	Dijkstra Shortest Path
	•	Kruskal Minimum Spanning Tree
	•	Greedy Graph Coloring
	•	Binary Search Tree Rebalancing

Objective:
Visual simulation of emergency routing and command hierarchy optimization.

Features:
	•	Interactive GUI
	•	Node failure simulation
	•	Risk-aware routing
	•	MST visualization
	•	Resource zone coloring



Question 5b – Multithreaded Sorting

Technique: Parallel Sorting with Thread Synchronization
Objective:
Sort an array using concurrent threads.

Concepts Demonstrated:
	•	Thread creation and joining
	•	Shared memory management
	•	Merge logic
	•	Race condition avoidance



Question 6 – Robot Navigation (Graph Search)

Algorithms:
	•	DFS (Depth-First Search)
	•	BFS (Breadth-First Search)
	•	A* Search

Objective:
Navigate between cities efficiently while comparing algorithm performance.

Concepts Demonstrated:
	•	Graph traversal
	•	Heuristic search
	•	Optimality comparison
	•	Performance metrics



🗂 Project Folder Structure

Project Root
│
├── main.py                        # Portfolio Runner
├── README.md                      # Project Documentation
│
├── Question_1_A_B/
│   ├── sensor_optimization.py
│   └── tsp_solver.py
│
├── question2/
│   └── tile_game.py
│
├── question3/
│   └── service_center.py
│
├── Question4_SmartGrid/
│   └── energy_system.py
│
├── Question5_a_b/
│   ├── network_app.py
│   └── multithreaded_sort.py
│
└── Question6solver/
    └── poland_robot.py



▶️ How to Run the Project

🔹 Requirements
	•	Python 3.9+
	•	No external libraries required (Tkinter included with Python)



🔹 Run Portfolio Runner

Open terminal in project root:

python main.py

You will see an interactive menu allowing you to run each question individually.



🔹 GUI Module (Q5a)

Select option:

6. Q5a Network GUI

A window will open for interactive network simulation.

Close the window to return to the menu.



🧪 Validation & Testing

Each module includes:
	•	Internal validation blocks
	•	Output verification
	•	Reflection explanations

The portfolio runner also:
	•	Handles import errors safely
	•	Prevents runtime crashes
	•	Displays algorithm reflections for academic evaluation

⸻

⸻

📊 Learning Outcomes Demonstrated
	•	Algorithm Design & Analysis
	•   Dynamic Programming
	•	Greedy Optimization
	•	Graph Search Algorithms
	•	Metaheuristics
	•	Multithreading
	•	GUI Development
	•	Software Architecture
	•	Defensive Programming
	•	Modular Design

