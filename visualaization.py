import heapq
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

class PolandRobotSolver:
    def __init__(self):
        # Map (a) Adjacency List: Distances in km
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
        stack = [(start, [start])]
        visited = set()
        nodes_explored = 0
        while stack:
            node, path = stack.pop()
            if node in visited: continue
            visited.add(node)
            nodes_explored += 1
            if node == goal: return path, nodes_explored
            for neighbor in self.graph.get(node, {}):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
        return None, nodes_explored

    def bfs(self, start, goal):
        queue = deque([(start, [start])])
        visited = {start}
        nodes_explored = 0
        while queue:
            node, path = queue.popleft()
            nodes_explored += 1
            if node == goal: return path, nodes_explored
            for neighbor in self.graph.get(node, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None, nodes_explored

    def a_star(self, start, goal):
        pq = [(0 + self.heuristic[start], start, [start])]
        g_score = {start: 0}
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
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f_new = tentative_g + self.heuristic.get(neighbor, 0)
                    heapq.heappush(pq, (f_new, neighbor, path + [neighbor]))
        return None, nodes_explored, float('inf')

def visualize_path(solver, path, title, algorithm_name):
    G = nx.Graph()
    for city, neighbors in solver.graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(city, neighbor, weight=weight)
            
    # Position nodes logically (Spring layout simulates distances)
    pos = nx.spring_layout(G, seed=42) 
    plt.figure(figsize=(10, 7))
    
    # Draw non-path elements
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color='#d1d1d1')
    nx.draw_networkx_labels(G, pos, font_size=9)
    nx.draw_networkx_edges(G, pos, width=1, edge_color='#cccccc', alpha=0.5)
    
    # Draw edge weights (distances)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    
    # Highlight the path
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#FF5733', node_size=700)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='#FF5733')
        
    plt.title(f"{algorithm_name} Search: {title}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    solver = PolandRobotSolver()
    start, end = 'Wroclaw', 'Warsaw'
    
    # 1. Visualize DFS
    p_dfs, n_dfs = solver.dfs(start, end)
    visualize_path(solver, p_dfs, f"Explored {n_dfs} nodes", "DFS")
    
    # 2. Visualize BFS
    p_bfs, n_bfs = solver.bfs(start, end)
    visualize_path(solver, p_bfs, f"Explored {n_bfs} nodes", "BFS")
    
    # 3. Visualize A*
    p_ast, n_ast, cost = solver.a_star(start, end)
    visualize_path(solver, p_ast, f"Explored {n_ast} nodes | Cost: {cost}km", "A-Star")