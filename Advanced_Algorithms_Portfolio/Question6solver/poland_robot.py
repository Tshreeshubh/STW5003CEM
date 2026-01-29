"""
Robot Navigation Solver - DFS, BFS, A*
--------------------------------------
Problem: Navigate a robot through Polish cities using Graph Search.
Algorithms:
1. DFS (Depth-First): Explores deep, not optimal.
2. BFS (Breadth-First): Explores layers, optimal for unweighted graphs.
3. A* (A-Star): Uses heuristics to find the shortest path efficiently.
"""

import heapq
from collections import deque

class PolandRobotSolver:
    def __init__(self):
        # Map (a) Adjacency List
        # Distances between cities in km
        self.graph = {
            'Bydgoszcz': {'Wloclawek': 110, 'Poznan': 140, 'Konin': 108},
            'Wloclawek': {'Bydgoszcz': 110, 'Plock': 55, 'Konin': 102},
            'Plock': {'Wloclawek': 55, 'Warsaw': 130},
            'Warsaw': {'Plock': 130, 'Lodz': 120, 'Radom': 105},
            'Konin': {'Bydgoszcz': 108, 'Wloclawek': 102, 'Poznan': 130, 'Lodz': 95, 'Kalisz': 120},
            'Poznan': {'Bydgoszcz': 140, 'Konin': 130, 'Leszno': 90},
            'Leszno': {'Poznan': 90, 'Wroclaw': 100, 'Kalisz': 140},
            'Kalisz': {'Konin': 120, 'Leszno': 140, 'Wroclaw': 120, 'Lodz': 160},
            'Lodz': {'Warsaw': 120, 'Konin': 95, 'Kalisz': 160, 'Czestochowa': 128, 'Radom': 190},
            'Radom': {'Warsaw': 105, 'Lodz': 190, 'Kielce': 80},
            'Wroclaw': {'Leszno': 100, 'Kalisz': 120, 'Opole': 100, 'Glogow': 140},
            'Glogow': {'Wroclaw': 140},
            'Opole': {'Wroclaw': 100, 'Czestochowa': 118, 'Katowice': 120},
            'Czestochowa': {'Lodz': 128, 'Opole': 118, 'Katowice': 85, 'Kielce': 100},
            'Katowice': {'Opole': 120, 'Czestochowa': 85, 'Krakow': 85},
            'Krakow': {'Katowice': 85, 'Kielce': 120},
            'Kielce': {'Radom': 80, 'Czestochowa': 100, 'Krakow': 120}
        }
        
        # Map (b) Heuristics (Straight line distance to Warsaw)
        self.heuristic = {
            'Bydgoszcz': 240, 'Wloclawek': 140, 'Plock': 95, 'Warsaw': 0,
            'Konin': 190, 'Poznan': 280, 'Leszno': 300, 'Kalisz': 220,
            'Lodz': 120, 'Radom': 100, 'Wroclaw': 320, 'Glogow': 360,
            'Opole': 290, 'Czestochowa': 220, 'Katowice': 280, 'Krakow': 290, 'Kielce': 170
        }

    def dfs(self, start, goal):
        """Depth-First Search (Stack-based)."""
        stack = [(start, [start])]
        visited = set()
        nodes_explored = 0
        
        while stack:
            node, path = stack.pop() # LIFO
            
            if node in visited: continue
            visited.add(node)
            nodes_explored += 1
            
            if node == goal: return path, nodes_explored
            
            # Add neighbors to stack
            for neighbor in self.graph.get(node, {}):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
                    
        return None, nodes_explored

    def bfs(self, start, goal):
        """Breadth-First Search (Queue-based). Optimized with Deque."""
        queue = deque([(start, [start])]) # FIFO
        visited = {start}
        nodes_explored = 0
        
        while queue:
            node, path = queue.popleft() # O(1) operation
            nodes_explored += 1
            
            if node == goal: return path, nodes_explored
            
            for neighbor in self.graph.get(node, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None, nodes_explored

    def a_star(self, start, goal):
        """A* Search (Priority Queue + Heuristic). Includes Closed Set."""
        # Priority Queue: (f_score, current_node, path)
        pq = [(0 + self.heuristic[start], start, [start])]
        
        # Tracks minimum cost found to a node so far
        g_score = {start: 0}
        
        # Closed set to avoid re-processing nodes (Optimization)
        visited = set()
        nodes_explored = 0
        
        while pq:
            f, current, path = heapq.heappop(pq)
            
            if current in visited: continue
            visited.add(current)
            nodes_explored += 1
            
            if current == goal: return path, nodes_explored, g_score[current]
            
            for neighbor, weight in self.graph.get(current, {}).items():
                tentative_g = g_score[current] + weight
                
                # If we found a cheaper path to neighbor
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f_new = tentative_g + self.heuristic.get(neighbor, float('inf'))
                    heapq.heappush(pq, (f_new, neighbor, path + [neighbor]))
                    
        return None, nodes_explored, float('inf')

    def get_reflection(self):
        """Returns analysis text for the portfolio reflection."""
        return """Reflection on Robot Navigation (Graph Search):
----------------------------------------------
1. DFS (Depth-First):
   - Strategy: Go deep immediately. Uses LIFO Stack.
   - Result: Often finds long, inefficient paths first. Not Optimal.
   - Complexity: O(V + E).

2. BFS (Breadth-First):
   - Strategy: Explore layer by layer. Uses FIFO Queue.
   - Result: Guarantees shortest path in unweighted graphs (fewest hops).
   - Optimization: Used 'deque' for O(1) pops.

3. A* (A-Star):
   - Strategy: Best-First Search using f(n) = g(n) + h(n).
   - Heuristic (h): Straight-line distance to Warsaw (Admissible).
   - Result: Finds the shortest weighted path (lowest km cost) efficiently.
   - Optimization: Used a 'Closed Set' to prune revisited nodes."""

if __name__ == "__main__":
    solver = PolandRobotSolver()
    start, end = 'Wroclaw', 'Warsaw'
    
    print(f"--- Question 6: Robot Navigation ({start} -> {end}) ---")
    
    p_dfs, n_dfs = solver.dfs(start, end)
    print(f"\n1. DFS Path: {p_dfs}\n   Nodes Explored: {n_dfs}")
    
    p_bfs, n_bfs = solver.bfs(start, end)
    print(f"\n2. BFS Path: {p_bfs}\n   Nodes Explored: {n_bfs}")
    
    p_ast, n_ast, cost = solver.a_star(start, end)
    print(f"\n3. A* Path:  {p_ast}\n   Nodes Explored: {n_ast}\n   Total Cost: {cost} km")
    
    print("\n--- Comparison ---")
    print(solver.get_reflection())