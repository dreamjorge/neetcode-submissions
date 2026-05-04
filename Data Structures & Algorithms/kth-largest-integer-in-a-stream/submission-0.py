from typing import List

class KthLargest:
    # --- STRATEGY: Sorted List with Binary Search Insertion ---
    #
    # Same goal: maintain the K largest elements seen so far.
    # This time without heapq — using a sorted list instead.
    #
    # We keep `top_k` sorted in ASCENDING order at all times.
    # The Kth largest is always at index 0 (the smallest of the top K).
    #
    # On every insertion:
    #   1. Binary Search → find the correct position  O(log k)
    #   2. Shift + insert → place the new value        O(k)
    #   3. Trim → evict index 0 if size exceeds K      O(k)
    #
    # Trade-off vs heapq:
    #   heapq  → O(log k) per add  (more efficient)
    #   this   → O(k)     per add  (simpler to understand, no imports)

    def __init__(self, k: int, nums: List[int]):
        self.k = k

        # Sort the full input first, then keep only the K largest.
        # Sorting ascending → the K largest are at the END → slice [-k:].
        nums.sort()
        self.top_k = nums[-k:] if len(nums) >= k else nums[:]
        # top_k is now a sorted ascending list of at most K elements.

    # ------------------------------------------------------------------
    # Helper: Binary Search for insertion position
    # ------------------------------------------------------------------
    def _find_insertion_position(self, val: int) -> int:
        # Find the leftmost index where top_k[index] >= val.
        # Inserting at that index keeps the list sorted.
        left, right = 0, len(self.top_k)

        while left < right:
            mid = left + (right - left) // 2
            if self.top_k[mid] < val:
                left = mid + 1
            else:
                right = mid

        return left

    # ------------------------------------------------------------------
    # Helper: Insert val into the correct sorted position
    # ------------------------------------------------------------------
    def _sorted_insert(self, val: int) -> None:
        insertion_position = self._find_insertion_position(val)

        # Extend the list by one slot, then shift elements right
        # to open a gap at insertion_position.
        self.top_k.append(0)  # placeholder

        for index in range(len(self.top_k) - 1, insertion_position, -1):
            self.top_k[index] = self.top_k[index - 1]

        self.top_k[insertion_position] = val

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def add(self, val: int) -> int:
        # --- STEP 1: Insert val in sorted order ---
        self._sorted_insert(val)

        # --- STEP 2: Trim to K elements if needed ---
        # The smallest element is always at index 0.
        # If we now have K+1 elements, evict the smallest (index 0).
        if len(self.top_k) > self.k:
            self.top_k.pop(0)

        # --- STEP 3: Return the Kth largest ---
        # With exactly K elements in ascending order, index 0 = Kth largest.
        return self.top_k[0]