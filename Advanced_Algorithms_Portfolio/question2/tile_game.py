"""
Strategic Tile Shatter - Dynamic Programming
--------------------------------------------
Problem: Maximize points by shattering tiles in optimal order.
Algorithm: Interval Dynamic Programming (Matrix Chain Multiplication variant).
Complexity: O(N^3) time, O(N^2) space.
"""

class TileGameSolver:
    """
    Solves the Tile Shatter problem using Dynamic Programming.
    """
    def solve_max_points(self, tile_multipliers):
        """
        Calculates the maximum possible score.
        
        Args:
            tile_multipliers (list): List of tile values.
            
        Returns:
            int: Maximum score achievable.
        """
        if not tile_multipliers:
            return 0
            
        # Requirement: Handle out-of-bounds as 1
        # Pad the array with 1s at both ends
        nums = [1] + tile_multipliers + [1]
        n = len(nums)
        
        # DP Table initialization
        # dp[i][j] stores max points from shattering tiles between index i and j (exclusive)
        dp = [[0] * n for _ in range(n)]
        
        # Iterate by length of the range (gap)
        for gap in range(2, n):
            for left in range(n - gap):
                right = left + gap
                
                # Iterate through all possible last tiles to shatter in this range
                # 'k' is the index of the LAST tile shattered between left and right
                for k in range(left + 1, right):
                    # Points gained from shattering 'k' last:
                    # 1. Points from left sub-problem (left to k)
                    # 2. Points from right sub-problem (k to right)
                    # 3. Points from shattering k itself (nums[left] * nums[k] * nums[right])
                    # Note: When k is shattered last, its neighbors are effectively 'left' and 'right'
                    current_score = (
                        dp[left][k] + 
                        dp[k][right] + 
                        (nums[left] * nums[k] * nums[right])
                    )
                    
                    # Update max score for this range
                    dp[left][right] = max(dp[left][right], current_score)
                    
        # Result is the max points for the full range (0 to n-1)
        return dp[0][n-1]

    def get_reflection(self):
        """Returns reflection text for portfolio."""
        return """Reflection on Strategic Tile Shatter:
-----------------------------------------
Algorithm: Interval Dynamic Programming (Matrix Chain Multiplication Variant)
Why: This problem exhibits 'Optimal Substructure' and 'Overlapping Subproblems'. 
A greedy approach fails because shattering a high-value tile early might remove it 
as a multiplier for an even better adjacent move.

Logic:
1. We define subproblems as finding the max score for a range (i, j).
2. To solve (i, j), we try every possible position 'k' as the LAST tile to shatter.
3. If 'k' is shattered last, it multiplies with the boundaries 'i' and 'j'.
4. We build the solution bottom-up, starting with small ranges (gap=2) and expanding.

Complexity: O(N^3) time due to the three nested loops (gap, left, k)."""

# --- VALIDATION BLOCK ---
if __name__ == "__main__":
    print("=== TEST Q2: Strategic Tile Shatter ===")
    
    solver = TileGameSolver()
    
    # Test Case 1: From Assignment Brief
    # Input: [3, 1, 5, 8] -> Expected: 167
    tiles_1 = [3, 1, 5, 8]
    score_1 = solver.solve_max_points(tiles_1)
    print(f"\nTest Case 1: Input {tiles_1}")
    print(f"  > Max Score: {score_1} (Expected: 167)")
    if score_1 == 167:
        print("  > STATUS: PASS")
    else:
        print("  > STATUS: FAIL")
        
    # Test Case 2: From Assignment Brief
    # Input: [1, 5] -> Expected: 10
    tiles_2 = [1, 5]
    score_2 = solver.solve_max_points(tiles_2)
    print(f"\nTest Case 2: Input {tiles_2}")
    print(f"  > Max Score: {score_2} (Expected: 10)")
    if score_2 == 10:
        print("  > STATUS: PASS")
    else:
        print("  > STATUS: FAIL")
        
    print("\nAll validation tests complete.")