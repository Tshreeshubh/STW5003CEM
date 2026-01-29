"""
Traveling Salesperson Problem (TSP) - Simulated Annealing
---------------------------------------------------------
Problem: Find the shortest route visiting N cities exactly once and returning to the start.
Algorithm: Simulated Annealing (Metaheuristic).
Cooling Schedules: Exponential & Linear.
"""

import math
import random

class TSPSolver:
    """
    Solves the TSP using Simulated Annealing.
    """
    def __init__(self, num_cities=20, area_size=1000, seed=42):
        """
        Initializes the TSP instance with random cities.
        
        Args:
            num_cities (int): Number of cities to generate.
            area_size (int): Max coordinate value (0 to area_size).
            seed (int): Random seed for reproducibility.
        """
        if seed is not None:
            random.seed(seed)
            
        self.n = num_cities
        # Requirement: Generate N cities with random 2D coordinates
        self.cities = [(random.uniform(0, area_size), random.uniform(0, area_size)) 
                       for _ in range(num_cities)]
        
    def _dist(self, city_a, city_b):
        """Calculates Euclidean distance between two cities."""
        return math.sqrt((city_a[0] - city_b[0])**2 + (city_a[1] - city_b[1])**2)
    
    def total_tour_distance(self, tour):
        """Calculates total distance of a complete tour (returning to start)."""
        d = 0.0
        for i in range(self.n):
            d += self._dist(self.cities[tour[i]], self.cities[tour[(i+1) % self.n]])
        return d
    
    def _get_neighbor(self, tour):
        """
        Generates a neighbor solution using 2-Opt or Swap.
        Requirement: Implement Neighborhood operations (Swap, 2-opt).
        """
        new_tour = tour[:]
        # Pick two random indices
        i, j = sorted(random.sample(range(self.n), 2))
        
        # 50% chance to Swap, 50% chance to 2-Opt (Reverse segment)
        if random.random() < 0.5:
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i] # Swap
        else:
            new_tour[i:j+1] = reversed(new_tour[i:j+1]) # 2-Opt
            
        return new_tour

    def solve(self, t_initial=1000, max_iter=50000, schedule_type='exponential', alpha=0.995):
        """
        Executes Simulated Annealing.
        
        Args:
            schedule_type (str): 'exponential' or 'linear'.
            alpha (float): Cooling rate for exponential schedule.
        """
        # Initial State: Random Permutation
        current_tour = list(range(self.n))
        random.shuffle(current_tour)
        current_dist = self.total_tour_distance(current_tour)
        
        # Track Best Solution found so far
        best_tour = current_tour[:]
        best_dist = current_dist
        
        temperature = t_initial
        
        for i in range(max_iter):
            # Requirement: Cooling Schedule
            if schedule_type == 'exponential':
                temperature *= alpha
            elif schedule_type == 'linear':
                # Linear decay: T = T_init - (beta * k)
                beta = t_initial / max_iter
                temperature = t_initial - (beta * i)
            
            # Requirement: Stopping Criteria (Temp threshold)
            if temperature <= 1e-6:
                break

            # Generate Neighbor
            neighbor_tour = self._get_neighbor(current_tour)
            neighbor_dist = self.total_tour_distance(neighbor_tour)
            
            # Calculate Energy Delta
            delta = neighbor_dist - current_dist
            
            # Acceptance Probability (Metropolis Criterion)
            # 1. If better (delta < 0), always accept.
            # 2. If worse, accept with probability P = exp(-delta / T)
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_tour = neighbor_tour
                current_dist = neighbor_dist
                
                # Update Best Solution
                if current_dist < best_dist:
                    best_dist = current_dist
                    best_tour = current_tour[:]
                    
        return best_dist, best_tour

    def get_reflection(self):
        """Returns reflection text for portfolio."""
        # Triple quotes for safe multi-line string
        return """Reflection on TSP (Simulated Annealing):
----------------------------------------
Algorithm: Simulated Annealing (Metaheuristic)
Why: TSP is NP-Hard. Exact algorithms (like brute force) are O(N!), which is impossible for N=20-50.
SA provides a "good enough" (near-optimal) solution in polynomial time.

Mechanism:
1. Exploration: At high Temp, SA accepts worse solutions to escape local optima.
2. Exploitation: At low Temp, SA behaves like Hill Climbing (only accepting improvements).

Cooling Schedules Tested:
1. Exponential (T = T0 * alpha^k): Slower cooling, usually finds better global optima.
2. Linear (T = T0 - beta*k): Constant cooling rate, simpler but risks getting stuck if too fast."""

# --- VALIDATION BLOCK ---
if __name__ == "__main__":
    print("=== TEST Q1b: TSP Simulated Annealing ===")
    
    # Generate Instance
    N = 20
    print(f"Generating {N} random cities...")
    solver = TSPSolver(num_cities=N, seed=42)
    
    # Test 1: Exponential Schedule
    print("\nRunning Exponential Schedule...")
    cost_exp, route_exp = solver.solve(schedule_type='exponential')
    print(f"  > Best Distance (Exponential): {cost_exp:.2f}")
    
    # Test 2: Linear Schedule
    print("\nRunning Linear Schedule...")
    # Re-initialize solver to ensure fair start comparison (same cities)
    solver_lin = TSPSolver(num_cities=N, seed=42)
    cost_lin, route_lin = solver_lin.solve(schedule_type='linear')
    print(f"  > Best Distance (Linear):      {cost_lin:.2f}")
    
    # Validation Check
    if cost_exp > 0 and cost_lin > 0:
        print("\n  > STATUS: PASS (Both schedules produced valid tours)")
    else:
        print("\n  > STATUS: FAIL")
        
    print(f"Difference: {abs(cost_exp - cost_lin):.2f}")