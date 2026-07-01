class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """
        WHAT PROBLEM DOES THIS SOLVE?

        We need the length of the longest run of consecutive integers
        hidden inside an unsorted list, in O(n) time.

        Naive approach (sorting): O(n log n) - too slow for the optimal
        solution we want here.

        Naive approach (walk from every number using a set): looks O(n)
        but is actually O(n^2) in the worst case, because a number in
        the middle of a long run re-walks the whole run every time.
        Example: for [1, 2, 3, ..., 100000], starting the walk from
        50000 retraces almost the entire array, and then starting from
        49999 retraces nearly the same ground again.

        CHOSEN STRATEGY: "boundary compression".
        Keep a dictionary, run_length_at_boundary, where a number's
        value is ONLY guaranteed accurate if that number sits at the
        left or right edge of a known consecutive run. When a new
        number arrives, we read the run-length already stored at its
        left neighbor (current_number - 1) and right neighbor
        (current_number + 1), combine them, and write the combined
        length back into the NEW edges of the merged run.

        Example: nums = [100, 4, 200, 1, 3, 2]
          -> 1 creates a run of length 1
          -> 3 creates a separate run of length 1
          -> 2 arrives and bridges 1 and 3 into a run of length 3,
             updating the edges (1 and 3) to both say "3"
          -> 4 arrives later and bridges into that run, extending it
             to length 4
        Final answer: 4
        """

        # run_length_at_boundary maps a number -> length of the
        # consecutive run it belongs to. This value is only trustworthy
        # at the two ends of a run; interior numbers are stale and
        # never looked at again, which is what keeps this O(n).
        run_length_at_boundary = defaultdict(int)

        longest_run_found = 0

        # STEP 1: Visit every number exactly once.
        # WHY: Each number is processed a single time, and each
        # processing step does constant-time dictionary lookups/writes.
        # This is what gives us O(n) overall instead of O(n^2).
        for current_number in nums:

            # STEP 2: Skip numbers we've already folded into a run.
            # WHY: If run_length_at_boundary[current_number] is already
            # non-zero, this exact value was already merged into a run
            # by an earlier iteration (it's a "used" interior number),
            # so re-processing it would do wasted, redundant work.
            # Example: after processing 2 in [100,4,200,1,3,2], the
            # entry mp[3] became 3 (a boundary value) - if 3 appeared
            # again in the array, we'd skip it here.
            if not run_length_at_boundary[current_number]:

                # STEP 3: Look up the run-length sitting at both
                # neighbors and merge them with the current number.
                # WHY: run_length_at_boundary[current_number - 1] is 0
                # if no run currently ends at (current_number - 1), and
                # likewise for + 1. Adding them plus 1 (for the current
                # number itself) gives the length of the brand-new,
                # merged run.
                # Example: current_number = 2, with mp[1] = 1 and
                # mp[3] = 1 already set from earlier iterations:
                #   merged_run_length = 1 (left) + 1 (right) + 1 (self) = 3
                merged_run_length = (
                    run_length_at_boundary[current_number - 1]
                    + run_length_at_boundary[current_number + 1]
                    + 1
                )
                run_length_at_boundary[current_number] = merged_run_length

                # STEP 4: Push the new merged length out to the FAR
                # edges of the run (not just the immediate neighbors).
                # WHY: Future numbers that try to extend this run will
                # only check the immediate neighbor of the run's edge,
                # so the edge itself must hold the up-to-date total
                # length, not just a length of 1.
                # Example continued (current_number = 2):
                #   left edge  = 2 - run_length_at_boundary[1] = 2 - 1 = 1
                #   -> run_length_at_boundary[1] = 3
                #   right edge = 2 + run_length_at_boundary[3] = 2 + 1 = 3
                #   -> run_length_at_boundary[3] = 3
                # Now both ends of the run [1,2,3] correctly report "3".
                left_edge = current_number - run_length_at_boundary[current_number - 1]
                run_length_at_boundary[left_edge] = merged_run_length

                right_edge = current_number + run_length_at_boundary[current_number + 1]
                run_length_at_boundary[right_edge] = merged_run_length

                # STEP 5: Track the best answer seen so far.
                longest_run_found = max(longest_run_found, merged_run_length)

        return longest_run_found