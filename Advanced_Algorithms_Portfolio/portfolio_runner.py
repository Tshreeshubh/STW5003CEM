import sys
import os
import tkinter as tk
from tkinter import ttk

# --- VERIFICATION PRINT ---
print("\n" + "="*50)
print("   SUCCESS! RUNNING THE FINAL PORTFOLIO RUNNER")
print("="*50 + "\n")

# --- PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # --- IMPORT SECTION ---
    
    # Q1: Sensor & TSP (Folder: Question_1_A_B)
    from Question_1_A_B.sensor_optimization import SensorOptimizer
    from Question_1_A_B.tsp_solver import TSPSolver
    
    # Q2: Tile Game (Folder: question2)
    from question2.tile_game import TileGameSolver
    
    # Q3: Service Center (Folder: question3)
    from question3.service_center import ServiceCenterSolver, TreeNode
    
    # Q4: Energy System (Folder: Question4_SmartGrid)
    from Question4_SmartGrid.energy_system import EnergyGridSolver
    
    # Q5: Network & Sorting (Folder: Question5_a_b)
    from Question5_a_b.network_app import NetworkApp
    from Question5_a_b.multithreaded_sort import MultithreadedSorter
    
    # Q6: Robot (Folder: Question6solver)
    from Question6solver.poland_robot import PolandRobotSolver

    print("All modules imported successfully.\n")

except ImportError as e:
    print("\nCRITICAL IMPORT ERROR")
    print(f"Error Detail: {e}")
    sys.exit(1)

# ==========================================
#              RUNNER FUNCTIONS
# ==========================================

def run_q1a():
    print("\n=== Q1a: Sensor Optimization ===")
    opt = SensorOptimizer([[0,1], [1,0], [1,2], [2,1]])
    x, y, dist = opt.optimize_hub_location()
    print(f"Optimal Hub: ({x:.5f}, {y:.5f}) | Distance: {dist:.5f}")
    print("\n--- Reflection ---")
    print(opt.get_reflection())

def run_q1b():
    print("\n=== Q1b: TSP Solver ===")
    # Using the class defaults for random city generation
    solver = TSPSolver(num_cities=10, seed=42)
    cost, route = solver.solve()
    print(f"Optimal Route Cost: {cost:.2f}")
    print("\n--- Reflection ---")
    print(solver.get_reflection())

def run_q2():
    print("\n=== Q2: Tile Game ===")
    solver = TileGameSolver()
    tiles = [3, 1, 5, 8]
    print(f"Input Tiles: {tiles}")
    print(f"Max Score: {solver.solve_max_points(tiles)}")
    print("\n--- Reflection ---")
    print(solver.get_reflection())

def run_q3():
    print("\n=== Q3: Service Center ===")
    # Constructing a sample tree: Root -> Left -> Left
    root = TreeNode(0)
    root.left = TreeNode(0)
    root.left.left = TreeNode(0)
    solver = ServiceCenterSolver()
    print(f"Tree Depth: 3 (Linear Chain)")
    print(f"Centers Needed: {solver.min_service_centers(root)}")
    print("\n--- Reflection ---")
    print(solver.get_reflection())

def run_q4():
    print("\n=== Q4: Smart Grid ===")
    grid = EnergyGridSolver()
    # Using the full day simulation to show the table output
    grid.simulate_day()
    print("\n--- Reflection ---")
    print(grid.get_reflection())

def run_q5_gui():
    print("\n=== Q5a: Network GUI ===")
    print("Launching Window... (Close window to return to menu)")
    root = tk.Tk()
    # Lift window to top
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    
    app = NetworkApp(root)
    root.mainloop()
    print("GUI Closed.")

def run_q5b():
    print("\n=== Q5b: Multithreaded Sorting ===")
    sorter = MultithreadedSorter()
    res = sorter.run()
    print(f"Final Sorted List: {res}")
    print("\n--- Reflection ---")
    print(sorter.get_reflection())

def run_q6():
    print("\n=== Q6: Robot Navigation ===")
    solver = PolandRobotSolver()
    start, end = 'Wroclaw', 'Warsaw'
    print(f"Navigating: {start} -> {end}")
    
    # Run DFS
    p_dfs, n_dfs = solver.dfs(start, end)
    print(f"\n1. DFS Path: {p_dfs}\n   Nodes Explored: {n_dfs}")
    
    # Run BFS
    p_bfs, n_bfs = solver.bfs(start, end)
    print(f"\n2. BFS Path: {p_bfs}\n   Nodes Explored: {n_bfs}")
    
    # Run A*
    p_ast, n_ast, cost = solver.a_star(start, end)
    print(f"\n3. A* Path:  {p_ast}\n   Nodes Explored: {n_ast}\n   Total Cost: {cost} km")
    
    print("\n--- Reflection ---")
    print(solver.get_reflection())

# ==========================================
#              MAIN MENU
# ==========================================
def main_menu():
    while True:
        print("\n" + "="*30)
        print(" ST5003CEM PORTFOLIO MAIN MENU")
        print("="*30)
        print("1. Q1a Sensor Optimization")
        print("2. Q1b TSP Solver")
        print("3. Q2  Strategic Tile Game")
        print("4. Q3  Service Center Tree")
        print("5. Q4  Smart Grid Simulation")
        print("6. Q5a Network GUI (Window)")
        print("7. Q5b Multithreaded Sort")
        print("8. Q6  Robot Navigation (Comparison)")
        print("0. Exit")
        
        c = input("\nSelect Option: ").strip()
        
        if c == '0':
            print("Exiting...")
            break
            
        # Error Handling Wrapper (Robustness)
        try:
            if c == '1': run_q1a()
            elif c == '2': run_q1b()
            elif c == '3': run_q2()
            elif c == '4': run_q3()
            elif c == '5': run_q4()
            elif c == '6': run_q5_gui()
            elif c == '7': run_q5b()
            elif c == '8': run_q6()
            else: print("Invalid selection. Try again.")
            
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred while running Option {c}:")
            print(f"Details: {e}")
            import traceback
            traceback.print_exc()
            print("Returning to menu...")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()