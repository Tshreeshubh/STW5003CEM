"""
Smart Energy Grid Optimization - DP & Greedy Hybrid
---------------------------------------------------
Problem: Optimize energy source allocation to meet district demands.
Strategies: 
1. Dynamic Programming (Bounded Knapsack) for exact cost minimization.
2. Greedy Heuristic for efficiency.
3. Approximate Demand Satisfaction (±10% tolerance).
"""

class EnergyGridSolver:
    """
    Simulates a 24-hour Smart Grid Control System.
    """
    def __init__(self):
        # 1. Resource Modeling (Capacity in kWh, Cost in Rs/kWh, Availability)
        self.sources = [
            {'name': 'Solar',  'cap': 50, 'cost': 1.0, 'hrs': range(6, 19)}, # Day only
            {'name': 'Hydro',  'cap': 40, 'cost': 1.5, 'hrs': range(0, 25)}, # 24/7
            {'name': 'Diesel', 'cap': 60, 'cost': 3.0, 'hrs': range(17, 24)} # Peak hours only
        ]
        
        # 2. Demand Modeling (Sample 24h profiles for Districts A, B, C)
        self.profiles = {
            'A': [10, 8, 8, 10, 15, 20, 25, 30, 30, 25, 20, 20, 20, 20, 25, 30, 35, 40, 40, 35, 30, 25, 20, 15],
            'B': [8, 6, 6, 8, 10, 15, 20, 20, 20, 20, 15, 15, 15, 15, 20, 25, 30, 30, 30, 25, 20, 15, 10, 8],
            'C': [5, 5, 5, 5, 8, 10, 15, 15, 15, 15, 10, 10, 10, 10, 15, 20, 25, 25, 25, 20, 15, 10, 8, 5]
        }
        
        # Statistics Tracking
        self.stats = {
            'total_cost': 0.0,
            'total_demand': 0,
            'total_supplied': 0,
            'renewable_usage': 0,
            'diesel_usage': 0
        }

    def solve_hour(self, hour, demand_a, demand_b, demand_c):
        """
        Solves allocation for a specific hour using DP with Tolerance logic.
        """
        total_demand = demand_a + demand_b + demand_c
        
        # Filter available sources for this hour
        active_sources = [s for s in self.sources if hour in s['hrs']]
        
        # Tolerance Logic: ±10% (0.9D to 1.1D)
        # We try to minimize cost within this acceptable range.
        min_target = int(total_demand * 0.9)
        max_target = int(total_demand * 1.1)
        
        # Attempt DP to find cheapest combination in range [min_target, max_target]
        alloc, cost = self._dp_knapsack_range(active_sources, min_target, max_target)
        
        # If DP fails (no valid combination found), fallback to Greedy
        if cost == float('inf'):
            alloc, cost = self._greedy_allocation(active_sources, total_demand)

        # Update Stats
        supplied = sum(alloc.values())
        self.stats['total_cost'] += cost
        self.stats['total_demand'] += total_demand
        self.stats['total_supplied'] += supplied
        self.stats['renewable_usage'] += alloc.get('Solar', 0) + alloc.get('Hydro', 0)
        self.stats['diesel_usage'] += alloc.get('Diesel', 0)
        
        return {
            'Hour': hour,
            'Demand': total_demand,
            'Supplied': supplied,
            'Cost': cost,
            'Allocation': alloc,
            'Met %': (supplied / total_demand * 100) if total_demand > 0 else 100
        }

    def _dp_knapsack_range(self, sources, min_demand, max_demand):
        """
        DP Approach: Bounded Knapsack Problem.
        Finds the minimum cost to achieve a total supply S where min_demand <= S <= max_demand.
        """
        # State: dp[kWh_supply] = min_cost
        # Initialize with 0 cost for 0 supply
        dp = {0: 0.0}
        parent = {0: None} # For reconstructing the solution
        
        for s in sources:
            name, cap, cost = s['name'], s['cap'], s['cost']
            
            # Create a snapshot of current states to ensure we don't reuse the same source unit
            # in the same iteration (Preventing unbounded knapsack behavior)
            current_states = list(dp.items())
            
            for prev_supply, prev_cost in current_states:
                # Try adding this source in increments of 1 unit up to its capacity
                # "Step size optimization" removed to ensure theoretical correctness
                for amount in range(1, cap + 1):
                    new_supply = prev_supply + amount
                    
                    # Optimization: Don't exceed max required range significantly
                    if new_supply > max_demand + 10: 
                        continue
                        
                    new_cost = prev_cost + (amount * cost)
                    
                    if new_supply not in dp or new_cost < dp[new_supply]:
                        dp[new_supply] = new_cost
                        parent[new_supply] = (name, amount, prev_supply)

        # Find the best supply amount within the valid tolerance range [min_demand, max_demand]
        best_supply = -1
        min_total_cost = float('inf')
        
        for s in range(min_demand, max_demand + 1):
            if s in dp:
                if dp[s] < min_total_cost:
                    min_total_cost = dp[s]
                    best_supply = s
                    
        if best_supply != -1:
            return self._reconstruct_path(parent, best_supply, sources), min_total_cost
            
        return {}, float('inf')

    def _reconstruct_path(self, parent, target, sources):
        allocation = {s['name']: 0 for s in sources}
        curr = target
        while curr > 0:
            if curr not in parent or parent[curr] is None: break
            name, amount, prev = parent[curr]
            allocation[name] += amount
            curr = prev
        return allocation

    def _greedy_allocation(self, sources, target):
        """Fallback: Sort by cost and take max possible."""
        sorted_src = sorted(sources, key=lambda x: x['cost'])
        alloc = {s['name']: 0 for s in sources}
        total_cost = 0.0
        rem_needed = target
        
        for s in sorted_src:
            take = min(rem_needed, s['cap'])
            alloc[s['name']] = take
            total_cost += take * s['cost']
            rem_needed -= take
            if rem_needed <= 0: break
            
        return alloc, total_cost

    def simulate_day(self):
        """Runs the simulation for all 24 hours."""
        print(f"{'Hr':<3} | {'Dem A':<5} {'Dem B':<5} {'Dem C':<5} | {'Total':<5} | {'Solar':<5} {'Hydro':<5} {'Diesel':<6} | {'Cost (Rs)':<10} | {'Met %'}")
        print("-" * 85)
        
        for h in range(24):
            da = self.profiles['A'][h]
            db = self.profiles['B'][h]
            dc = self.profiles['C'][h]
            
            res = self.solve_hour(h, da, db, dc)
            a = res['Allocation']
            
            print(f"{h:02d}  | {da:<5} {db:<5} {dc:<5} | {res['Demand']:<5} | "
                  f"{a.get('Solar',0):<5} {a.get('Hydro',0):<5} {a.get('Diesel',0):<6} | "
                  f"{res['Cost']:<10.2f} | {res['Met %']:<5.1f}")
        
        self._print_analysis()

    def _print_analysis(self):
        print("-" * 85)
        print("FINAL ANALYSIS")
        print(f"Total Daily Cost:      Rs. {self.stats['total_cost']:.2f}")
        print(f"Total Demand:          {self.stats['total_demand']} kWh")
        print(f"Total Supplied:        {self.stats['total_supplied']} kWh")
        
        if self.stats['total_supplied'] > 0:
            ren_pct = (self.stats['renewable_usage'] / self.stats['total_supplied']) * 100
            dsl_pct = (self.stats['diesel_usage'] / self.stats['total_supplied']) * 100
            print(f"Renewable Energy Used: {ren_pct:.1f}%")
            print(f"Diesel Fuel Used:      {dsl_pct:.1f}%")

    def get_reflection(self):
        return """Reflection on Smart Grid Optimization:
------------------------------------------
Algorithm: Bounded Knapsack DP with Range Tolerance.
Why: This ensures mathematically minimal cost while satisfying constraints.
Tolerance: The system accepts supply in range [0.9D, 1.1D] to prevent over-provisioning 
costs or minor under-supply issues, adhering to real-world grid flexibility.

Complexity Analysis:
- Time Complexity: O(N * S * C) where N=Sources, S=MaxSupply, C=Capacity.
- Space Complexity: O(S) for the DP table.
Note: While slower than Greedy, DP is optimal for cost minimization."""

# --- VALIDATION BLOCK ---
if __name__ == "__main__":
    print("=== TEST Q4: Smart Grid Full Day Simulation ===")
    sim = EnergyGridSolver()
    sim.simulate_day()