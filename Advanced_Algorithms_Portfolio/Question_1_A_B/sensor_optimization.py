"""
Sensor Hub Optimization - Robust Weiszfeld Algorithm
----------------------------------------------------
Problem: Find the Geometric Median of a set of 2D points to minimize 
the sum of Euclidean distances (Signal Attenuation).

Algorithm: Weiszfeld's Iterative Algorithm
Complexity: O(K * N) where K is iterations, N is number of sensors.
"""

import math

class SensorOptimizer:
    """
    Calculates the optimal hub location (Geometric Median) to minimize
    total Euclidean distance to a set of sensors.
    """
    def __init__(self, locations=None):
        # Validate input is a list of lists/tuples
        self.locations = locations if locations else []

    def optimize_hub_location(self, tolerance=1e-7, max_iter=100):
        """
        Executes Weiszfeld's Algorithm.
        
        Args:
            tolerance (float): Stop when hub moves less than this distance.
            max_iter (int): Safety limit for iterations.
            
        Returns:
            tuple: (optimal_x, optimal_y, minimum_total_distance)
        """
        # Edge Case 1: No sensors
        if not self.locations:
            return 0.0, 0.0, 0.0
        
        # Edge Case 2: Single sensor (Hub is on the sensor)
        if len(self.locations) == 1:
            return self.locations[0][0], self.locations[0][1], 0.0
        
        # Step 1: Initialize Hub at Centroid (Mean)
        # The mean is a good starting guess but minimizes squared distance, not Euclidean distance.
        current_x = sum(p[0] for p in self.locations) / len(self.locations)
        current_y = sum(p[1] for p in self.locations) / len(self.locations)
        
        # Step 2: Iterative Refinement
        for iteration in range(max_iter):
            num_x, num_y = 0.0, 0.0
            denom = 0.0
            
            # Calculate weighted sum based on inverse distance
            for px, py in self.locations:
                dist = math.sqrt((current_x - px)**2 + (current_y - py)**2)
                
                # Singularity handling: If hub is exactly on a point, avoid div/0
                dist = max(dist, 1e-10)
                
                weight = 1.0 / dist
                num_x += weight * px
                num_y += weight * py
                denom += weight
            
            # Stop if denominator is zero (should not happen with robustness check)
            if denom == 0:
                break
                
            new_x = num_x / denom
            new_y = num_y / denom
            
            # Step 3: Check Convergence
            shift = math.sqrt((new_x - current_x)**2 + (new_y - current_y)**2)
            current_x, current_y = new_x, new_y
            
            if shift < tolerance:
                break
        
        # Calculate Final Total Distance
        final_dist = sum(math.sqrt((current_x - p[0])**2 + (current_y - p[1])**2) 
                         for p in self.locations)
        
        return current_x, current_y, final_dist

    def get_reflection(self):
        """Returns analysis text for the portfolio reflection."""
        # Using triple quotes to avoid SyntaxErrors with multi-line strings
        return """Sensor Optimization Analysis (Geometric Median):
------------------------------------------------
Algorithm Used: Weiszfeld's Algorithm
Why: The Geometric Median minimizes the sum of Euclidean distances (L1 norm equivalent in 2D space),
whereas the simple Centroid (Mean) minimizes the sum of SQUARED distances.
There is no closed-form solution for Geometric Median, so an iterative approach is required.

Time Complexity: O(K * N) where K is the number of iterations and N is the number of sensors.
Robustness: This method is less sensitive to outliers (far away sensors) compared to the Mean."""

# --- VALIDATION BLOCK ---
if __name__ == "__main__":
    print("=== TEST Q1a: Sensor Optimization ===")
    
    # Test Case 1: Square Configuration (Example from PDF)
    # Expected: 4.0
    sensors_1 = [[0,1], [1,0], [1,2], [2,1]]
    opt_1 = SensorOptimizer(sensors_1)
    x1, y1, d1 = opt_1.optimize_hub_location()
    print(f"\nTest Case 1 (Square): Input {sensors_1}")
    print(f"  > Optimal Hub: ({x1:.5f}, {y1:.5f})")
    print(f"  > Total Distance: {d1:.5f} (Expected: 4.00000)")
    # Using a small epsilon for float comparison
    if abs(d1 - 4.0) < 1e-4:
        print("  > STATUS: PASS")
    else:
        print("  > STATUS: FAIL")

    # Test Case 2: Diagonal Configuration (Example from PDF)
    # Expected: 2.82843
    sensors_2 = [[1,1], [3,3]]
    opt_2 = SensorOptimizer(sensors_2)
    x2, y2, d2 = opt_2.optimize_hub_location()
    print(f"\nTest Case 2 (Diagonal): Input {sensors_2}")
    print(f"  > Optimal Hub: ({x2:.5f}, {y2:.5f})")
    print(f"  > Total Distance: {d2:.5f} (Expected: 2.82843)")
    if abs(d2 - 2.82843) < 1e-4:
        print("  > STATUS: PASS")
    else:
        print("  > STATUS: FAIL")
    
    print("\nAll validation tests complete.")