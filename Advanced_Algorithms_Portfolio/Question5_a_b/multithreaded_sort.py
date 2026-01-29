"""
Multithreaded Sorting Application
---------------------------------
Problem: Sort a list using two separate threads for halves, 
and a third thread to merge them.
"""

import threading
import time

# Shared Global Arrays (Simulating shared memory)
# We use a wrapper class to avoid global variable issues during import
class SharedData:
    original_list = [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
    sorted_list = [0] * len(original_list)

def sorting_worker(start_index, end_index, result_array, thread_name):
    """
    Sorting Thread: Sorts a slice of the original list.
    """
    print(f"[{thread_name}] Started sorting indices {start_index} to {end_index}...")
    
    # Extract sublist
    sublist = SharedData.original_list[start_index:end_index]
    sublist.sort() # Local sort
    
    # Simulate work
    time.sleep(0.1) 
    
    # Write back to shared array
    for i, val in enumerate(sublist):
        result_array[start_index + i] = val
        
    print(f"[{thread_name}] Finished.")

def merging_worker(mid_point):
    """
    Merging Thread: Merges the two sorted halves.
    """
    print("[Merge Thread] Started merging...")
    
    left_half = SharedData.sorted_list[:mid_point]
    right_half = SharedData.sorted_list[mid_point:]
    
    i = j = k = 0
    final_merge = [0] * len(SharedData.sorted_list)
    
    # Standard Merge Sort Logic
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            final_merge[k] = left_half[i]
            i += 1
        else:
            final_merge[k] = right_half[j]
            j += 1
        k += 1
        
    while i < len(left_half):
        final_merge[k] = left_half[i]; i += 1; k += 1
        
    while j < len(right_half):
        final_merge[k] = right_half[j]; j += 1; k += 1
        
    # Update the global result
    SharedData.sorted_list = final_merge
    print("[Merge Thread] Finished merging.")

class MultithreadedSorter:
    def run(self):
        # Reset for fresh run
        SharedData.original_list = [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
        SharedData.sorted_list = [0] * len(SharedData.original_list)
        
        n = len(SharedData.original_list)
        mid = n // 2
        
        print(f"Original List: {SharedData.original_list}\n")
        
        # 1. Create Sorting Threads
        t1 = threading.Thread(target=sorting_worker, args=(0, mid, SharedData.sorted_list, "Thread-1"))
        t2 = threading.Thread(target=sorting_worker, args=(mid, n, SharedData.sorted_list, "Thread-2"))
        
        # 2. Start and Wait (Join)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        print(f"\nIntermediate State: {SharedData.sorted_list}")
        
        # 3. Create Merging Thread
        t_merge = threading.Thread(target=merging_worker, args=(mid,))
        t_merge.start()
        t_merge.join()
        
        return SharedData.sorted_list

    def get_reflection(self):
        return """Reflection on Multithreaded Sorting:
--------------------------------------
Concurrency Logic:
1. Divide: The list is split into two halves.
2. Parallel Execution: Two threads sort these halves simultaneously.
3. Synchronization: The main program uses .join() to wait for sorting to finish.
4. Merge: A third thread merges the sorted sub-lists.

Why no locks? 
We write to disjoint (non-overlapping) sections of the array [0..mid] and [mid..end],
so there is no Race Condition during the sorting phase."""

# --- VALIDATION BLOCK ---
if __name__ == "__main__":
    print("=== TEST Q5b: Multithreaded Sort ===")
    sorter = MultithreadedSorter()
    result = sorter.run()
    
    print(f"\nFinal Result:   {result}")
    expected = sorted([7, 12, 19, 3, 18, 4, 2, 6, 15, 8])
    print(f"Expected:       {expected}")
    
    if result == expected:
        print("STATUS: PASS")
    else:
        print("STATUS: FAIL")