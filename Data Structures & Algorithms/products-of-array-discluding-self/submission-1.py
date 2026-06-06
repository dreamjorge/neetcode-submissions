# ==============================================================================
# WHAT PROBLEM DOES productExceptSelf SOLVE?
#
# CHALLENGE:
#   Given a list of integers, return a new list where each position holds
#   the product of every number in the original list EXCEPT the one at
#   that position.
#
# WHY THE NAIVE APPROACH FAILS:
#   The obvious idea: "just divide the total product by each element."
#   But what if an element is 0? Division by zero crashes.
#   What if there are TWO zeros? Every product becomes 0 anyway.
#   So we need special handling for zeros before any division happens.
#
# CHOSEN STRATEGY — "Count Zeros + Guarded Division":
#   1. Compute the product of ALL non-zero numbers (skip zeros while counting them).
#   2. Use the zero count to decide what each output slot should be:
#      - More than 1 zero  → every result is 0  (nothing can be non-zero)
#      - Exactly 1 zero    → only the slot WHERE the zero sits gets the total
#                            product; every other slot gets 0
#      - No zeros          → normal division: total_product // current_element
#
# LABELED EXAMPLE:
#   Input:           [1,  0,  4,  5]
#   non_zero_product = 1 * 4 * 5 = 20        (skipped the 0)
#   zero_count       = 1
#
#   Fill output:
#     index 0, element=1 → zero_count>0 and element≠0 → result[0] = 0
#     index 1, element=0 → zero_count>0 and element==0 → result[1] = 20  ← the one zero slot
#     index 2, element=4 → zero_count>0 and element≠0 → result[2] = 0
#     index 3, element=5 → zero_count>0 and element≠0 → result[3] = 0
#   Output: [0, 20, 0, 0]  ✓
# ==============================================================================

from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:

        # ----------------------------------------------------------------------
        # STEP 1 — Compute the product of non-zero elements & count zeros
        #
        # WHY: We want a single "total" we can reuse.  Skipping zeros prevents
        #      a divide-by-zero crash and keeps the product meaningful.
        #
        # WHY not just `math.prod(nums)`?  That collapses to 0 the moment any
        #      zero appears, destroying the information we need for Step 2.
        #
        # EXAMPLE with nums = [2, 0, 3, 4]:
        #   iteration 0: element=2, non-zero → non_zero_product = 1*2 = 2
        #   iteration 1: element=0, zero     → zero_count = 1  (product unchanged)
        #   iteration 2: element=3, non-zero → non_zero_product = 2*3 = 6
        #   iteration 3: element=4, non-zero → non_zero_product = 6*4 = 24
        #   Result: non_zero_product=24, zero_count=1
        # ----------------------------------------------------------------------
        non_zero_product = 1
        zero_count = 0

        for current_element in nums:
            if current_element:                        # truthy → not zero
                non_zero_product *= current_element
            else:                                      # element is exactly 0
                zero_count += 1

        # ----------------------------------------------------------------------
        # STEP 2 — Early exit: more than one zero means all results are 0
        #
        # WHY: If two or more positions are 0, every "product except self"
        #      must include at least one remaining 0, so the whole output
        #      list is zeros. Returning early avoids wasted work.
        #
        # EXAMPLE: nums = [1, 0, 0, 9]
        #   zero_count = 2 → return [0, 0, 0, 0] immediately
        # ----------------------------------------------------------------------
        if zero_count > 1:
            return [0] * len(nums)

        # ----------------------------------------------------------------------
        # STEP 3 — Build the result list using the zero count as a switch
        #
        # WHY a list filled afterward instead of appending?
        #   Pre-allocating [0] * len(nums) and indexing is slightly more
        #   memory-predictable than repeated .append() calls for fixed-size output.
        #
        # THREE CASES decided by (zero_count, current_element):
        #
        #   Case A — zero_count >= 1 AND element != 0:
        #     The product "except self" must include the zero(s) still in the
        #     list, so the result for this slot is 0.
        #
        #   Case B — zero_count >= 1 AND element == 0:
        #     This slot IS the zero. All other numbers (the non-zero ones)
        #     multiply to non_zero_product. Result = non_zero_product.
        #
        #   Case C — zero_count == 0:
        #     No zeros anywhere. Safe to divide: non_zero_product // element.
        #     (Integer division is exact here because element is a factor of
        #      non_zero_product by construction.)
        #
        # WALK-THROUGH TRACE for nums = [2, 0, 3, 4], non_zero_product=24, zero_count=1:
        #   index=0, element=2: zero_count>0 and 2≠0  → result[0] = 0
        #   index=1, element=0: zero_count>0 and 0==0 → result[1] = 24
        #   index=2, element=3: zero_count>0 and 3≠0  → result[2] = 0
        #   index=3, element=4: zero_count>0 and 4≠0  → result[3] = 0
        #   Final result: [0, 24, 0, 0]  ✓
        #
        # WALK-THROUGH TRACE for nums = [1, 2, 3, 4], non_zero_product=24, zero_count=0:
        #   index=0, element=1: no zeros → result[0] = 24 // 1 = 24
        #   index=1, element=2: no zeros → result[1] = 24 // 2 = 12
        #   index=2, element=3: no zeros → result[2] = 24 // 3 = 8
        #   index=3, element=4: no zeros → result[3] = 24 // 4 = 6
        #   Final result: [24, 12, 8, 6]  ✓
        # ----------------------------------------------------------------------
        result = [0] * len(nums)

        for current_index, current_element in enumerate(nums):
            if zero_count:                                      # Case A or B
                result[current_index] = 0 if current_element else non_zero_product
            else:                                               # Case C
                result[current_index] = non_zero_product // current_element

        return result


# ==============================================================================
# VISUAL SUMMARY
#
#  ┌─────────────────────────────────────────────────────────────────────────┐
#  │                     productExceptSelf ALGORITHM FLOW                    │
#  ├─────────────────────────────────────────────────────────────────────────┤
#  │  INPUT: nums list                                                       │
#  │         │                                                               │
#  │         ▼                                                               │
#  │  ┌─────────────────────────────────┐                                    │
#  │  │ STEP 1: scan nums               │                                    │
#  │  │  • multiply non-zeros together  │  → non_zero_product                │
#  │  │  • count zeros                  │  → zero_count                      │
#  │  └────────────────┬────────────────┘                                    │
#  │                   │                                                     │
#  │                   ▼                                                     │
#  │  ┌────────────────────────────┐                                         │
#  │  │ STEP 2: zero_count > 1?    │──── YES ──→ return [0, 0, ..., 0]       │
#  │  └────────────────┬───────────┘                                         │
#  │                   │ NO                                                  │
#  │                   ▼                                                     │
#  │  ┌──────────────────────────────────────────────────────────────┐       │
#  │  │ STEP 3: for each (index, element) in nums                    │       │
#  │  │                                                              │       │
#  │  │   zero_count > 0?                                            │       │
#  │  │   ├─ YES, element != 0  →  result[index] = 0    (Case A)     │       │
#  │  │   ├─ YES, element == 0  →  result[index] = non_zero_product  │       │
#  │  │   │                                             (Case B)     │       │
#  │  │   └─ NO (zero_count==0) →  result[index] =                   │       │
#  │  │                              non_zero_product // element     │       │
#  │  │                                             (Case C)         │       │
#  │  └──────────────────────────────────────────────────────────────┘       │
#  │                   │                                                     │
#  │                   ▼                                                     │
#  │              return result                                              │
#  └─────────────────────────────────────────────────────────────────────────┘
#
#  TIME  COMPLEXITY: O(n) — two separate single-pass loops over nums
#  SPACE COMPLEXITY: O(n) — the output list; O(1) extra (just two scalar vars)
# ==============================================================================