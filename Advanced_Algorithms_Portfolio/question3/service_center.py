"""
Service Center Optimization - Binary Tree Vertex Cover
----------------------------------------------------
Problem: Minimize service centers to cover all nodes in a binary tree.
Algorithm: Greedy DFS (Post-order Traversal).
Complexity: O(N) time, O(H) space.
"""

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class ServiceCenterSolver:
    """
    Solves the Service Center placement problem using a Greedy Strategy 
    on a Tree (Vertex Cover).
    """
    def __init__(self):
        self.centers = 0

    def min_service_centers(self, root):
        """
        Calculates the minimum number of service centers required.
        
        Args:
            root (TreeNode): Root of the binary tree.
            
        Returns:
            int: Number of centers.
        """
        self.centers = 0
        
        # Helper function for Depth First Search
        # Returns state of the node:
        # 0: Not covered (needs coverage from parent)
        # 1: Covered (by a child)
        # 2: Has a Service Center (covers self, parent, and children)
        def dfs(node):
            if not node:
                return 1 # Null nodes are implicitly covered
            
            # Post-order traversal (Bottom-Up)
            left_state = dfs(node.left)
            right_state = dfs(node.right)
            
            # STRATEGY:
            # If any child is uncovered (0), we MUST place a center at this node.
            # This is the greedy choice that guarantees optimality.
            if left_state == 0 or right_state == 0:
                self.centers += 1
                return 2
            
            # If any child has a center (2), this node is covered.
            if left_state == 2 or right_state == 2:
                return 1
                
            # If children are covered (1) but don't have centers, 
            # this node is currently uncovered (0).
            return 0

        # Edge Case: If the root itself remains uncovered after checking children
        if dfs(root) == 0:
            self.centers += 1
            
        return self.centers

    def get_reflection(self):
        """Returns reflection text for portfolio."""
        return """Reflection on Service Center Optimization:
----------------------------------------------
Algorithm: Greedy Depth-First Search (Post-order Traversal)
Why: This is a variation of the Minimum Vertex Cover problem. On general graphs, 
Vertex Cover is NP-Hard. However, on Trees, it can be solved in linear time O(N) 
using Dynamic Programming or a Greedy approach.

Logic:
1. We process nodes from bottom-up (post-order).
2. If a leaf is uncovered, placing a camera at the leaf covers only the leaf and parent.
3. Placing a camera at the PARENT covers the parent, the leaf, and other siblings.
4. Therefore, it is always strictly better (or equal) to place the center at the 
   parent of an uncovered node.

Complexity: O(N) time (visiting every node once)."""

# --- VALIDATION BLOCK ---
if __name__ == "__main__":
    print("=== TEST Q3: Service Center Optimization ===")
    
    solver = ServiceCenterSolver()
    
    # Test Case 1: Linear Chain (Depth 3)
    # Structure: 0 -> 0 -> 0
    # Expected: 1 center (at the middle node)
    root_1 = TreeNode(0)
    root_1.left = TreeNode(0)
    root_1.left.left = TreeNode(0)
    
    res_1 = solver.min_service_centers(root_1)
    print(f"\nTest Case 1 (Linear Chain 3):")
    print(f"  > Centers: {res_1} (Expected: 1)")
    if res_1 == 1: print("  > STATUS: PASS")
    else: print("  > STATUS: FAIL")

    # Test Case 2: From PDF Brief
    # Input: {0,0, null, 0, null, 0, null, null, 0}
    # This represents a tree structure that typically requires 2 centers.
    # Constructing a structure: Root -> Left -> Left -> Right -> Right (Depth 5 chain-like)
    root_2 = TreeNode(0)
    root_2.left = TreeNode(0)
    root_2.left.left = TreeNode(0)
    root_2.left.left.right = TreeNode(0)
    root_2.left.left.right.right = TreeNode(0)
    
    res_2 = solver.min_service_centers(root_2)
    print(f"\nTest Case 2 (Complex Tree from PDF):")
    print(f"  > Centers: {res_2} (Expected: 2)")
    if res_2 == 2: print("  > STATUS: PASS")
    else: print("  > STATUS: FAIL")

    print("\nAll validation tests complete.")