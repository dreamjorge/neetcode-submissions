from typing import List

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        # --- STRATEGY: Sorted Array as a Manual Max-Heap ---
        #
        # The problem: repeatedly smash the two heaviest stones together.
        #   - If they are equal     → both destroyed (nothing remains)
        #   - If they are different → the difference survives
        #
        # We need fast access to the two LARGEST values at every step.
        #
        # Approach: keep the list SORTED AT ALL TIMES (ascending order).
        # The two heaviest stones are always at the END — easy to pop.
        # After smashing, if a remainder exists, we insert it back
        # into the correct sorted position using Binary Search.
        #
        # This avoids re-sorting the entire list on every iteration.
        stones.sort()

        # `active_count` tracks how many stones are currently in play.
        # We use this instead of calling len(stones) repeatedly, because
        # we manually manage insertions without resizing the list each time.
        active_count = len(stones)

        # --- MAIN LOOP: Keep smashing until one or zero stones remain ---
        while active_count > 1:

            # --- STEP 1: Smash the two heaviest stones ---
            # pop() removes and returns the last element (the heaviest).
            # We call it twice to get the two largest stones.
            heaviest      = stones.pop()   # largest stone
            second_heaviest = stones.pop() # second largest stone
            remainder     = heaviest - second_heaviest
            active_count -= 2              # we removed two stones

            # --- STEP 2: Reinsert the remainder (if any) ---
            # If remainder == 0, both stones destroyed each other — nothing to reinsert.
            # If remainder  > 0, a fragment survived and must go back into sorted order.
            if remainder > 0:

                # --- Binary Search: find the correct insertion position ---
                # We search within the active portion of the list [0 .. active_count).
                # Goal: find the leftmost index where stones[index] >= remainder.
                # Everything to the left will be smaller; everything to the right, larger.
                left, right = 0, active_count

                while left < right:
                    mid = (left + right) // 2
                    if stones[mid] < remainder:
                        left = mid + 1   # remainder belongs further right
                    else:
                        right = mid      # mid could be the insertion point; keep narrowing

                insertion_position = left

                # --- Shift elements right to open a slot ---
                # We extend the list by one (reuse the slot freed by the earlier pops)
                # then shift every element from insertion_position onward one place right.
                active_count += 1
                stones.append(0)         # placeholder to extend the list by one slot

                for index in range(active_count - 1, insertion_position, -1):
                    stones[index] = stones[index - 1]

                # Place the remainder in its correct sorted position
                stones[insertion_position] = remainder

        # --- RESULT ---
        # If one stone remains, return it.
        # If no stones remain (all destroyed each other), return 0.
        return stones[0] if active_count > 0 else 0