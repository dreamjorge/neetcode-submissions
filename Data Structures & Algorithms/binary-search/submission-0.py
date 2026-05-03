from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # --- STRATEGY: Binary Search ---
        # Because the array is SORTED, we don't need to check every element.
        # We repeatedly cut the search space in HALF by looking at the middle.
        #
        # We track our current search window with two pointers:
        #   left  → the leftmost index we still consider
        #   right → the rightmost index we still consider
        left, right = 0, len(nums) - 1

        while left <= right:
            # --- STEP 1: Find the middle index ---
            #
            # ⚠️  WHY NOT (left + right) // 2 ?
            # If both left and right are very large, left + right can OVERFLOW
            # in languages like C++ or Java. The safe formula below is
            # mathematically identical but never exceeds right.
            #
            # Example:  left=2, right=8  →  2 + (8-2)//2  =  2 + 3  =  5  ✓
            middle = left + ((right - left) // 2)

            if nums[middle] > target:
                # --- CASE A: Middle value is TOO HIGH ---
                # Target must be in the LEFT half.
                # Shrink the window by moving right pointer just before middle.
                right = middle - 1

            elif nums[middle] < target:
                # --- CASE B: Middle value is TOO LOW ---
                # Target must be in the RIGHT half.
                # Shrink the window by moving left pointer just after middle.
                left = middle + 1

            else:
                # --- CASE C: Exact match ---
                # nums[middle] == target → found it, return the index.
                return middle

        # --- NOT FOUND ---
        # The window collapsed (left > right) without a match.
        return -1