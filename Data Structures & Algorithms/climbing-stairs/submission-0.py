class Solution:
    def climbStairs(self, current_step: int = None, total_steps: int = None) -> int:
        """
        WHAT PROBLEM DOES THIS SOLVE?

        THE CHALLENGE:
        You are climbing a staircase with `total_steps` steps. Each move you
        can climb either 1 step or 2 steps. You need to count the total
        number of DISTINCT ways to reach the top.

        WHY A NAIVE APPROACH (plain recursion, no memoization) FAILS:
        The brute-force idea is: "from step X, try climbing 1 step, then
        try climbing 2 steps, and add up all the ways those lead to the top."
        This is correct in terms of LOGIC, but it is disastrously slow,
        because the same sub-problems get solved over and over again.

        Concrete ambiguous-looking example: total_steps = 5
            ways(5) = ways(4) + ways(3)
            ways(4) = ways(3) + ways(2)   <-- ways(3) computed again
            ways(3) = ways(2) + ways(1)   <-- ways(2) computed again
        Notice ways(3) is requested by both ways(5) and ways(4).
        ways(2) is requested by both ways(4) and ways(3).
        Without caching, the number of redundant calls doubles at every
        level, giving exponential time, O(2^n), even though there are only
        `total_steps` truly distinct sub-problems.

        THE STRATEGY (Bottom-Up Dynamic Programming):
        Instead of recursing top-down and re-solving the same sub-problems,
        we build the answer from the ground up. We notice:

            ways(0) = 1   (one way to "stand still" at the bottom: do nothing)
            ways(1) = 1   (only one path: a single 1-step move)
            ways(step) = ways(step - 1) + ways(step - 2)   for step >= 2

        This is exactly the Fibonacci recurrence. We only ever need the
        last two computed values to get the next one, so we don't even
        need an array -- two rolling variables are enough.

        LABELED EXAMPLE: total_steps = 5
            Input:  total_steps = 5
            Intermediate steps (rolling values):
                ways_to_reach_previous_step = 1   (ways(1))
                ways_to_reach_current_step  = 1   (ways(2))
                -> after step 3: 2
                -> after step 4: 3
                -> after step 5: 5
            Output: 5
            (Real paths for 5 steps: 1+1+1+1+1, 1+1+1+2, 1+1+2+1, 1+2+1+1,
             2+1+1+1, 1+2+2, 2+1+2, 2+2+1  -> 8 ways... wait, let's recount
             properly inside the trace below.)
        """

        # This solution is written to match LeetCode's required signature:
        # def climbStairs(self, n: int) -> int
        # The parameters above are renamed for teaching purposes; the
        # actual method below uses the original required signature and
        # descriptive internal variable names.

        pass


class Solution:
    def climbStairs(self, n: int) -> int:
        """
        WHAT PROBLEM DOES THIS SOLVE?

        THE CHALLENGE:
        Given `n` steps, and the ability to climb 1 or 2 steps at a time,
        count how many distinct sequences of moves reach exactly step n.

        WHY THE NAIVE RECURSIVE APPROACH FAILS:
        A direct translation of "try 1 step, try 2 steps, sum the results"
        looks like:

            def dfs(current_step):
                if current_step >= n:
                    return current_step == n
                return dfs(current_step + 1) + dfs(current_step + 2)

        This is logically correct, but each call branches into 2 more
        calls, and many of those calls compute the SAME current_step value
        multiple times. For n = 5, dfs(3) gets called from both dfs(2) and
        dfs(1)'s grandchildren -- the same sub-problem is solved repeatedly.
        This gives O(2^n) time complexity, which becomes far too slow once
        n grows past ~35-40.

        THE STRATEGY (Bottom-Up Dynamic Programming, O(n) time, O(1) space):
        Recognize that the number of ways to reach step `current_step` only
        depends on the number of ways to reach the two steps right before
        it:

            ways(current_step) = ways(current_step - 1) + ways(current_step - 2)

        This is the Fibonacci sequence in disguise. Instead of recursing
        downward and re-solving sub-problems, we iterate UPWARD from the
        base cases and keep only the last two results in memory.

        LABELED EXAMPLE: n = 5
            Base cases: ways(1) = 1, ways(2) = 2
            ways(3) = ways(2) + ways(1) = 2 + 1 = 3
            ways(4) = ways(3) + ways(2) = 3 + 2 = 5
            ways(5) = ways(4) + ways(3) = 5 + 3 = 8
            Input: n = 5  ->  Output: 8
        """

        # STEP 1: Handle the smallest cases directly.
        # WHY: Steps 1 and 2 don't have two "previous" values to add
        # together yet, so they need to be defined as starting points
        # (base cases) for the recurrence to work.
        # EXAMPLE: if n = 1, there is exactly 1 way (a single 1-step move).
        #          if n = 2, there are exactly 2 ways (1+1, or 2).
        if n == 1:
            return 1
        if n == 2:
            return 2

        # STEP 2: Initialize the two rolling values that represent
        # ways(1) and ways(2), since those are the first two terms
        # we'll use to build up to ways(n).
        # WHY THIS APPROACH OVER AN ARRAY: We only ever need the two most
        # recent values to compute the next one, so storing the entire
        # history in a list would waste O(n) space for no benefit.
        # EXAMPLE STATE after this step: ways_two_steps_back = 1 (ways(1))
        #                                 ways_one_step_back = 2 (ways(2))
        ways_two_steps_back = 1   # represents ways(current_step_index - 2)
        ways_one_step_back = 2    # represents ways(current_step_index - 1)

        # STEP 3: Iterate upward from step 3 to step n, applying the
        # recurrence ways(current) = ways(current - 1) + ways(current - 2)
        # at each iteration, then "sliding" the rolling values forward.
        # WHY: This avoids recomputation entirely -- each step is computed
        # exactly once, giving O(n) time instead of the naive O(2^n).
        #
        # WALK-THROUGH TRACE for n = 5:
        #
        #   current_step_index=3: ways_at_current_step = 2 + 1 = 3
        #       -> ways_two_steps_back becomes 2, ways_one_step_back becomes 3
        #   current_step_index=4: ways_at_current_step = 3 + 2 = 5
        #       -> ways_two_steps_back becomes 3, ways_one_step_back becomes 5
        #   current_step_index=5: ways_at_current_step = 5 + 3 = 8
        #       -> ways_two_steps_back becomes 5, ways_one_step_back becomes 8
        #   Loop ends (range stops after current_step_index = n = 5)
        #   Final ways_one_step_back = 8  <-- this is our answer
        for current_step_index in range(3, n + 1):
            ways_at_current_step = ways_one_step_back + ways_two_steps_back

            # Slide the window forward: what was "one step back" becomes
            # "two steps back", and our new result becomes "one step back".
            ways_two_steps_back = ways_one_step_back
            ways_one_step_back = ways_at_current_step

        # STEP 4: After the loop, ways_one_step_back holds ways(n),
        # because the last iteration always computes the value for the
        # final index in the range, which is n itself.
        return ways_one_step_back

        # -----------------------------------------------------------
        # VISUAL SUMMARY (n = 5 example):
        #
        #   index:   1     2     3     4     5
        #   ways:  [ 1 ] [ 2 ] [ 3 ] [ 5 ] [ 8 ]
        #             \     \     \     \
        #              +     +     +     +   (each cell = sum of previous two)
        #
        #   +------------------+------------------+
        #   | two_steps_back   | one_step_back     |
        #   +------------------+------------------+
        #   |        1         |        2          |  start (index 1,2)
        #   |        2         |        3          |  after index 3
        #   |        3         |        5          |  after index 4
        #   |        5         |        8          |  after index 5 -> answer
        #   +------------------+------------------+
        #
        # TIME COMPLEXITY:  O(n)  -- one pass from 3 to n, constant work
        #                            per iteration.
        # SPACE COMPLEXITY: O(1)  -- only two rolling variables are kept,
        #                            regardless of how large n is.
        # -----------------------------------------------------------