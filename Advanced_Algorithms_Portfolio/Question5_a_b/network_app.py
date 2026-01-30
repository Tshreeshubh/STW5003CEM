import tkinter as tk
from tkinter import messagebox, ttk
import math
import heapq

class EmergencyGraph:
    def __init__(self):
        # Weighted edges: (Distance/Time cost)
        self.adj = {
            'HQ': {'HUBA': 10, 'HUBB': 15, 'HUBC': 20},
            'HUBA': {'HQ': 10, 'SUB1': 30, 'SUB2': 10},
            'HUBB': {'HQ': 15, 'SUB2': 15, 'SUB3': 50},
            'HUBC': {'HQ': 20, 'SUB3': 10, 'SUB4': 40},
            'SUB1': {'HUBA': 30, 'END1': 5},
            'SUB2': {'HUBA': 10, 'HUBB': 15, 'END2': 20},
            'SUB3': {'HUBB': 50, 'HUBC': 10, 'END2': 10},
            'SUB4': {'HUBC': 40, 'END3': 5},
            'END1': {'SUB1': 5},
            'END2': {'SUB2': 20, 'SUB3': 10},
            'END3': {'SUB4': 5}
        }
        # Fixed Positions for UI
        self.positions = {
            'HQ': (300, 50),
            'HUBA': (150, 150), 'HUBB': (300, 150), 'HUBC': (450, 150),
            'SUB1': (100, 250), 'SUB2': (200, 250), 'SUB3': (400, 250), 'SUB4': (500, 250),
            'END1': (50, 350), 'END2': (300, 350), 'END3': (550, 350)
        }
        self.disabled_nodes = set()
        # Vulnerable roads (Risk zones) - modeled as sorted tuples
        self.vulnerable_roads = {
            tuple(sorted(('HUBB', 'SUB3'))), 
            tuple(sorted(('HUBC', 'SUB4')))
        }

    def get_active_edges(self):
        edges = []
        seen = set()
        for u in self.adj:
            if u in self.disabled_nodes: continue
            for v, w in self.adj[u].items():
                if v in self.disabled_nodes: continue
                edge_key = tuple(sorted((u, v)))
                if edge_key not in seen:
                    edges.append((u, v, w))
                    seen.add(edge_key)
        return edges

    def kruskal_mst(self):
        """Kruskal's Algorithm for Minimum Spanning Tree."""
        edges = self.get_active_edges()
        edges.sort(key=lambda x: x[2])
        parent = {node: node for node in self.positions if node not in self.disabled_nodes}
        
        def find(i):
            if parent[i] == i: return i
            return find(parent[i])
        
        def union(i, j):
            root_i, root_j = find(i), find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False
            
        return [ (u, v) for u, v, w in edges if union(u, v) ]

    def dijkstra_shortest_path(self, start, end, exclude_edges=None, avoid_risky=False):
        """Dijkstra's Algorithm with constraints."""
        if exclude_edges is None: exclude_edges = set()
        if start in self.disabled_nodes or end in self.disabled_nodes:
            return None, float('inf')
        
        queue = [(0, start, [])]
        min_costs = {start: 0}

        while queue:
            cost, u, path = heapq.heappop(queue)
            
            if cost > min_costs.get(u, float('inf')): continue
            
            curr_path = path + [u]
            if u == end: return curr_path, cost
            
            for v, w in self.adj.get(u, {}).items():
                if v in self.disabled_nodes: continue
                
                edge_sig = tuple(sorted((u, v)))
                if edge_sig in exclude_edges: continue
                
                # Vulnerability Check
                if avoid_risky and edge_sig in self.vulnerable_roads:
                    continue
                    
                new_cost = cost + w
                if new_cost < min_costs.get(v, float('inf')):
                    min_costs[v] = new_cost
                    heapq.heappush(queue, (new_cost, v, curr_path))
        return None, float('inf')

    def greedy_coloring(self):
        """Bonus: Greedy Graph Coloring for Resource Zones."""
        colors = {}
        nodes = sorted(list(self.positions.keys()))
        
        for u in nodes:
            if u in self.disabled_nodes: continue
            neighbor_colors = {colors.get(v) for v in self.adj[u] if v in colors}
            color = 0
            while color in neighbor_colors:
                color += 1
            colors[u] = color
        return colors

class CommandTreeLogic:
    """Logic for the Command Hierarchy (BST)."""
    class TreeNode:
        def __init__(self, val):
            self.val, self.left, self.right = val, None, None

    def __init__(self):
        self.root = self.TreeNode(10)
        curr = self.root
        # Simulate an unbalanced chain (Worst case O(N))
        for val in [20, 30, 40, 50, 60]:
            curr.right = self.TreeNode(val)
            curr = curr.right

    def optimize_hierarchy(self):
        """Rebalances the BST to minimize communication depth (O(log N))."""
        nodes = []
        def in_order(node):
            if not node: return
            in_order(node.left); nodes.append(node); in_order(node.right)
        
        def build_balanced(nodes_list, start, end):
            if start > end: return None
            mid = (start + end) // 2
            node = nodes_list[mid]
            node.left = build_balanced(nodes_list, start, mid - 1)
            node.right = build_balanced(nodes_list, mid + 1, end)
            return node
            
        in_order(self.root)
        self.root = build_balanced(nodes, 0, len(nodes) - 1)

class EmergencyApp:
    def __init__(self, root):
        self.root = root
        if isinstance(self.root, (tk.Tk, tk.Toplevel)):
            self.root.title("Emergency Network Simulator (Student ID: XXXXX)")
            self.root.geometry("1100x800")
        
        self.graph = EmergencyGraph()
        self.tree_logic = CommandTreeLogic()
        
        # UI Styling
        style = ttk.Style()
        style.theme_use('clam')
        
        self.tabs = ttk.Notebook(root)
        self.tab_network = ttk.Frame(self.tabs)
        self.tab_tree = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_network, text="Network Operations")
        self.tabs.add(self.tab_tree, text="Command Hierarchy")
        self.tabs.pack(expand=1, fill="both")
        
        self.setup_network_ui()
        self.setup_tree_ui()
        self.draw_graph()
        self.draw_tree()

    def setup_network_ui(self):
        # Control Panel
        ctrl = tk.LabelFrame(self.tab_network, text="Control Panel", bg="#f0f0f0", pady=5)
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # 1. Start/End Selection (Validation Fix)
        tk.Label(ctrl, text="Start Node:").pack(side=tk.LEFT, padx=5)
        self.cb_start = ttk.Combobox(ctrl, values=list(self.graph.positions.keys()), width=8)
        self.cb_start.set("HQ")
        self.cb_start.pack(side=tk.LEFT, padx=5)
        
        tk.Label(ctrl, text="End Node:").pack(side=tk.LEFT, padx=5)
        self.cb_end = ttk.Combobox(ctrl, values=list(self.graph.positions.keys()), width=8)
        self.cb_end.set("END3")
        self.cb_end.pack(side=tk.LEFT, padx=5)
        
        # 2. Operations
        tk.Button(ctrl, text="Find Route", bg="#90ee90", command=self.find_route).pack(side=tk.LEFT, padx=10)
        
        # 3. Features
        self.var_risk = tk.BooleanVar()
        tk.Checkbutton(ctrl, text="Avoid High Risk Roads", variable=self.var_risk, bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        
        tk.Button(ctrl, text="Generate MST", bg="lightblue", command=self.show_mst).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="Resource Zones (Bonus)", bg="gold", command=self.show_coloring).pack(side=tk.LEFT, padx=5)

        # Legend
        lbl_info = tk.Label(ctrl, text="[Tip: Click nodes to simulate failure]", font=("Arial", 9, "italic"), bg="#f0f0f0")
        lbl_info.pack(side=tk.RIGHT, padx=10)
        
        self.canvas = tk.Canvas(self.tab_network, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_node_click)

    def setup_tree_ui(self):
        ctrl = tk.Frame(self.tab_tree, pady=10)
        ctrl.pack(side=tk.TOP)
        tk.Label(ctrl, text="Command Chain Optimization (BST Rebalancing)", font=("Arial", 12, "bold")).pack()
        tk.Button(ctrl, text="Optimize Hierarchy", bg="orange", command=self.optimize_tree).pack(pady=5)
        self.tree_canvas = tk.Canvas(self.tab_tree, bg="red")
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)

    def draw_graph(self, mst_edges=None, highlighted_paths=None, zone_colors=None):
        self.canvas.delete("all")
        
        # Draw Edges
        for u, v, w in self.graph.get_active_edges():
            p1, p2 = self.graph.positions[u], self.graph.positions[v]
            
            # Default Style
            color, width, dash = "#ccc", 2, None
            edge_sig = tuple(sorted((u, v)))
            
            # Vulnerable Roads Styling
            if edge_sig in self.graph.vulnerable_roads:
                color = "#ffcccc" # Light red
                dash = (4, 4)     # Dashed line
            
            # MST Highlight
            if mst_edges and ((u, v) in mst_edges or (v, u) in mst_edges): 
                color, width, dash = "blue", 4, None
            
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=width, dash=dash)
            self.canvas.create_text((p1[0]+p2[0])/2, (p1[1]+p2[1])/2, text=str(w), font=("Arial", 9))

        # Draw Highlighted Paths
        if highlighted_paths:
            colors = ["red", "purple", "orange"]
            offset = 0
            for idx, (path, cost) in enumerate(highlighted_paths):
                c = colors[idx % len(colors)]
                for i in range(len(path)-1):
                    u, v = path[i], path[i+1]
                    p1, p2 = self.graph.positions[u], self.graph.positions[v]
                    self.canvas.create_line(p1[0]+offset, p1[1]+offset, p2[0]+offset, p2[1]+offset, 
                                          fill=c, width=3)
                offset += 4

        # Draw Nodes
        zone_palette = ["#87cefa", "#98fb98", "#ffb6c1", "#dda0dd", "#f0e68c"]
        for node, pos in self.graph.positions.items():
            fill_col = "#e0e0e0" # Default grey
            
            if node in self.graph.disabled_nodes:
                fill_col = "#696969" # Disabled Dark Grey
            elif zone_colors and node in zone_colors:
                fill_col = zone_palette[zone_colors[node] % len(zone_palette)]
            elif node == "HQ":
                fill_col = "#ffcc00" # HQ Gold
            else:
                fill_col = "#87cefa" # Standard Blue
                
            self.canvas.create_oval(pos[0]-20, pos[1]-20, pos[0]+20, pos[1]+20, fill=fill_col, outline="black")
            self.canvas.create_text(pos[0], pos[1], text=node, font=("Arial", 9, "bold"))

    def on_node_click(self, event):
        for node, pos in self.graph.positions.items():
            if math.dist((event.x, event.y), pos) < 20:
                if node in self.graph.disabled_nodes: self.graph.disabled_nodes.remove(node)
                else: self.graph.disabled_nodes.add(node)
                self.draw_graph()
                break

    def find_route(self):
        start = self.cb_start.get()
        end = self.cb_end.get()
        avoid_risk = self.var_risk.get()
        
        # 1. Primary Shortest Path
        path1, cost1 = self.graph.dijkstra_shortest_path(start, end, avoid_risky=avoid_risk)
        
        if not path1:
            messagebox.showerror("Route Error", f"No path exists from {start} to {end}.\nCheck disabled nodes.")
            return

        # 2. Calculate Secondary Path (Backup) for Analysis
        # We temporarily exclude edges from the first path to find a disjoint backup
        excluded = set()
        for i in range(len(path1) - 1):
            excluded.add(tuple(sorted((path1[i], path1[i+1]))))
            
        path2, cost2 = self.graph.dijkstra_shortest_path(start, end, exclude_edges=excluded, avoid_risky=avoid_risk)
        
        # Display Results
        paths_to_draw = [(path1, cost1)]
        report = f"Primary Route: {' -> '.join(path1)}\nCost: {cost1} mins\n"
        
        if path2:
            paths_to_draw.append((path2, cost2))
            delay = ((cost2 - cost1) / cost1) * 100
            report += f"\nBackup Route: {' -> '.join(path2)}\nCost: {cost2} mins\n"
            report += f"\n⚠ Delay Analysis: Backup is {delay:.1f}% slower."
        else:
            report += "\n⚠ No distinct backup route available."

        self.draw_graph(highlighted_paths=paths_to_draw)
        messagebox.showinfo("Route Analysis", report)

    def show_mst(self):
        mst = self.graph.kruskal_mst()
        self.draw_graph(mst_edges=mst)
        messagebox.showinfo("MST Generated", f"Minimum Spanning Tree connects all active nodes.\nTotal Edges: {len(mst)}")

    def show_coloring(self):
        colors = self.graph.greedy_coloring()
        self.draw_graph(zone_colors=colors)
        messagebox.showinfo("Resource Zones", "Nodes colored by zone (Greedy Graph Coloring).\nNodes with same color share non-conflicting resources.")

    def optimize_tree(self):
        self.tree_logic.optimize_hierarchy()
        self.draw_tree()
        messagebox.showinfo("Optimization Complete", "Command hierarchy rebalanced.\nCommunication depth minimized to O(log N).")

    def draw_tree(self):
        self.tree_canvas.delete("all")
        def _draw(node, x, y, dx):
            if not node: return
            r = 18
            self.tree_canvas.create_oval(x-r, y-r, x+r, y+r, fill="#041104", outline="red")
            self.tree_canvas.create_text(x, y, text=str(node.val))
            if node.left:
                self.tree_canvas.create_line(x, y+r, x-dx, y+60-r)
                _draw(node.left, x-dx, y+60, dx/2)
            if node.right:
                self.tree_canvas.create_line(x, y+r, x+dx, y+60-r)
                _draw(node.right, x+dx, y+60, dx/2)
        _draw(self.tree_logic.root, 550, 50, 250)

class NetworkApp:
    def __init__(self, root):
        self.root = root
        EmergencyApp(root)