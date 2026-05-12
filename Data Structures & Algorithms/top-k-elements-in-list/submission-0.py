from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # --- STRATEGY: Bucket Sort by Frequency ---
        #
        # Naive approach: count frequencies, then sort by count → O(n log n)
        # Better approach: use the frequency itself as an array INDEX → O(n)
        #
        # Key insight: if we have n numbers, no single number can appear
        # more than n times. So frequencies always fall in the range [1, n].
        # That means we can use frequency as a direct index into an array!
        #
        # We call this array of lists a "bucket array":
        #   bucket[f] = list of all numbers that appear exactly f times
        #
        # Example: nums = [1, 1, 1, 2, 2, 3],  k = 2
        #
        #   Step 1 — count frequencies:
        #     frequency_count = {1:3, 2:2, 3:1}
        #
        #   Step 2 — place each number in its bucket:
        #     buckets index:  0    1     2     3
        #     buckets value: [ ]  [3]   [2]   [1]
        #                          ↑     ↑     ↑
        #                    freq=1  freq=2  freq=3
        #
        #   Step 3 — read from highest bucket downward until we have k results:
        #     i=3 → [1]  → result = [1]
        #     i=2 → [2]  → result = [1, 2]  → len == k → return ✓

        # --- STEP 1: Count how many times each number appears ---
        # `count.get(num, 0)` safely returns 0 if `num` is not yet in the dict,
        # avoiding a KeyError on the first occurrence of each number.
        frequency_count: dict[int, int] = {}
        for num in nums:
            frequency_count[num] = 1 + frequency_count.get(num, 0)

        # --- STEP 2: Initialize the bucket array ---
        # We need indices 1 through n (frequency 0 is impossible for any
        # number that actually appears). We create n+1 buckets so that
        # index n is valid — index 0 will simply remain unused.
        #
        # buckets[f] will hold all numbers whose frequency is exactly f.
        buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]

        # --- STEP 3: Place each number into its frequency bucket ---
        # A number with frequency `count` goes into buckets[count].
        for num, count in frequency_count.items():
            buckets[count].append(num)

        # --- STEP 4: Collect results from highest frequency downward ---
        # We scan from the last bucket (highest possible frequency = n)
        # toward the first (frequency = 1), collecting numbers until
        # we have exactly k results.
        #
        # We stop early with `return` the moment we reach k — no extra work.
        top_k_elements: List[int] = []

        for frequency in range(len(buckets) - 1, 0, -1):
            for num in buckets[frequency]:
                top_k_elements.append(num)
                if len(top_k_elements) == k:
                    return top_k_elements