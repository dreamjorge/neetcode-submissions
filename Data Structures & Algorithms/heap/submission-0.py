"""
================================================================================
WHAT PROBLEM DOES MinHeap SOLVE?
================================================================================

THE CORE CHALLENGE:
    We need a data structure that always gives us the SMALLEST element
    instantly, while still allowing fast insertions and deletions.

WHY A NAIVE APPROACH FAILS:
    - A sorted list gives O(1) access to the minimum, but inserting a new
      value requires O(n) time to shift elements and keep order.
    - An unsorted list allows O(1) insertion, but finding the minimum
      requires an O(n) scan every time.
    We need something in between.

THE CHOSEN STRATEGY — A Binary Min-Heap:
    A heap is a COMPLETE BINARY TREE stored in an array, where every parent
    is SMALLER than its children (the "heap property"). This gives us:
        - O(log n) push  (bubble new value UP until heap property is restored)
        - O(log n) pop   (swap root with last, bubble DOWN to restore order)
        - O(1)    top    (the root is always the minimum)
        - O(n)    heapify (build a heap from scratch faster than n pushes)

THE INDEX TRICK (why we put a dummy 0 at index 0):
    Storing the tree in a 1-indexed array lets us navigate with pure math:
        parent of node at index k  →  k // 2
        left  child of node at k  →  2 * k
        right child of node at k  →  2 * k + 1
    A dummy value at index 0 makes index 1 the root, so every formula works
    without special-casing the root.

LABELED EXAMPLE — push [5, 3, 8, 1]:
    After each push the heap array (ignoring index-0 dummy) looks like:

    push 5 → [5]
    push 3 → [3, 5]        (3 bubbled up past 5: 3 < 5)
    push 8 → [3, 5, 8]     (8 is already larger than parent 3; stays put)
    push 1 → [1, 3, 8, 5]  (1 bubbled up: 1<5, then 1<3, reaches root)

    Tree shape after push 1:
            1          ← root (index 1)
           / \
          3   8        ← index 2, 3
         /
        5              ← index 4

    pop() → returns 1, promotes 5 to root, bubbles 5 down past 3:
            3
           / \
          5   8
================================================================================
"""

from typing import List


class MinHeap:

    # ------------------------------------------------------------------ #
    # STEP 1 — INITIALIZE                                                  #
    # ------------------------------------------------------------------ #
    # We start with a list containing a single dummy value at index 0.
    # This dummy occupies slot 0 so the real heap begins at index 1,
    # making the parent/child index formulas (k//2, 2k, 2k+1) work
    # without any offset correction.
    #
    # Example: after __init__,  self.heap = [0]
    #          after push(5),   self.heap = [0, 5]
    #          after push(3),   self.heap = [0, 3, 5]   ← 3 bubbled to root
    def __init__(self):
        self.heap = [0]  # index 0 is a permanently unused sentinel/dummy


    # ------------------------------------------------------------------ #
    # STEP 2 — PUSH (insert a new value)                                  #
    # ------------------------------------------------------------------ #
    # WHAT:  Append the new value at the end of the array (the next open
    #        leaf slot in the tree), then restore the heap property by
    #        bubbling the value UP toward the root.
    #
    # WHY APPEND THEN BUBBLE UP:
    #   Appending keeps the tree "complete" (no gaps).  Bubbling up is the
    #   only repair needed because every other existing node was already
    #   in a valid parent-child relationship.
    #
    # EXAMPLE: heap = [0, 3, 5, 8], push(1)
    #   Append → [0, 3, 5, 8, 1]   new value lands at index 4
    #   _bubble_up(4): parent = 4//2 = 2, heap[2]=5 > heap[4]=1 → swap
    #                  → [0, 3, 1, 8, 5]   now at index 2
    #   _bubble_up(2): parent = 2//2 = 1, heap[1]=3 > heap[2]=1 → swap
    #                  → [0, 1, 3, 8, 5]   now at index 1 (root) → done
    def push(self, val: int) -> None:
        self.heap.append(val)                  # place new value at the last leaf
        self._bubble_up(len(self.heap) - 1)   # repair upward from that position


    # ------------------------------------------------------------------ #
    # STEP 3 — POP (remove and return the minimum)                        #
    # ------------------------------------------------------------------ #
    # WHAT:  The minimum is always at index 1 (the root).  We save it,
    #        move the LAST leaf to the root position, remove the now-
    #        duplicate last element, and bubble the promoted value DOWN.
    #
    # WHY REPLACE ROOT WITH LAST ELEMENT:
    #   Simply deleting the root would split the tree into two subtrees.
    #   Replacing it with the last leaf keeps the tree complete (one node
    #   is removed from the bottom), and a single bubble-down pass
    #   restores the heap property.
    #
    # EDGE CASES handled first to avoid index errors:
    #   - Empty heap (only dummy at index 0)   → return -1
    #   - One real element (index 1 only)      → pop() directly (no swap needed)
    #
    # EXAMPLE: heap = [0, 1, 3, 8, 5], pop()
    #   root = heap[1] = 1                         save the answer
    #   heap[1] = heap.pop() → heap becomes [0, 5, 3, 8]   last leaf → root
    #   _bubble_down(1): left child at 2 (val=3), right child at 3 (val=8)
    #                    smaller child is 3 at index 2; 5>3 → swap
    #                    → [0, 3, 5, 8]   5 is now at index 2
    #   _bubble_down(2): left child at 4 — index 4 >= len(heap)=4 → stop
    #   return 1   ✓
    def pop(self) -> int:
        if len(self.heap) <= 1:     # heap is empty (only dummy exists)
            return -1
        if len(self.heap) == 2:     # exactly one real element; no swap needed
            return self.heap.pop()  # removes and returns heap[1]

        minimum_value = self.heap[1]        # save the root (the answer)
        self.heap[1] = self.heap.pop()      # move last leaf to root, shrink array
        self._bubble_down(1)                # restore heap property from the root
        return minimum_value


    # ------------------------------------------------------------------ #
    # STEP 4 — TOP (peek at the minimum without removing it)             #
    # ------------------------------------------------------------------ #
    # WHAT:  Simply read index 1 (the root).  No modification needed.
    # WHY O(1): The heap property guarantees the minimum is always at the
    #           root; there is no searching involved.
    #
    # EXAMPLE: heap = [0, 1, 3, 8, 5]  →  top() returns 1
    def top(self) -> int:
        return self.heap[1] if len(self.heap) > 1 else -1


    # ------------------------------------------------------------------ #
    # STEP 5 — HEAPIFY (build a heap from an existing list in O(n))      #
    # ------------------------------------------------------------------ #
    # WHAT:  Accept an unordered list and rearrange it into a valid heap.
    #
    # WHY NOT JUST PUSH n TIMES:
    #   Calling push() n times costs O(n log n).  Heapify is smarter:
    #   leaf nodes (bottom half of the array) are already trivially valid
    #   heaps of size 1, so we only need to bubble DOWN the non-leaf nodes.
    #   Starting from the last non-leaf (index n//2) and working toward
    #   the root means each bubble-down touches at most O(height) nodes,
    #   and the math works out to O(n) total.
    #
    # FINDING THE LAST NON-LEAF:
    #   In a 1-indexed array of length L (including the dummy), the real
    #   elements occupy indices 1 … L-1.  The last non-leaf is at
    #   index (L-1)//2  =  len(self.heap)//2  after prepending the dummy.
    #
    # EXAMPLE: nums = [5, 3, 8, 1, 2]
    #   self.heap = [0, 5, 3, 8, 1, 2]   (dummy prepended)
    #   len = 6  →  last non-leaf at index 6//2 = 3  (value 8)
    #
    #   Iteration order (reversed range so we go bottom-up):
    #     i=3: bubble_down(3) — heap[3]=8, left child index 6 ≥ len → stop
    #     i=2: bubble_down(2) — heap[2]=3, left child at 4 (val=1), right at 5 (val=2)
    #                           smaller child is 1 at index 4; 3>1 → swap
    #                           → [0, 5, 1, 8, 3, 2]
    #     i=1: bubble_down(1) — heap[1]=5, left child at 2 (val=1), right at 3 (val=8)
    #                           smaller child is 1 at index 2; 5>1 → swap
    #                           → [0, 1, 5, 8, 3, 2]
    #                           now at index 2, left child at 4 (val=3), right at 5 (val=2)
    #                           smaller child is 2 at index 5; 5>2 → swap
    #                           → [0, 1, 2, 8, 3, 5]
    #   Final heap: [0, 1, 2, 8, 3, 5]  → minimum 1 is at the root ✓
    def heapify(self, nums: List[int]) -> None:
        self.heap = [0] + nums                              # prepend dummy at index 0
        last_non_leaf_index = len(self.heap) // 2          # leaves need no repair
        for current_index in reversed(range(1, last_non_leaf_index + 1)):
            self._bubble_down(current_index)               # repair each internal node


    # ------------------------------------------------------------------ #
    # HELPER A — _bubble_up (used by push)                                #
    # ------------------------------------------------------------------ #
    # WHAT:  Repeatedly swap a node with its parent as long as the node is
    #        SMALLER than its parent (violating the min-heap property).
    #
    # TERMINATION CONDITIONS (either one stops the loop):
    #   1. index == 1  → we reached the root; nothing above to compare.
    #   2. heap[parent] <= heap[index]  → parent is already ≤ child; valid.
    #
    # WALK-THROUGH TRACE for heap = [0, 3, 5, 8], pushing 1 at index 4:
    #
    #   Iteration 1:
    #     index=4, parent=4//2=2, heap[2]=5, heap[4]=1
    #     5 > 1  →  swap  →  heap = [0, 3, 1, 8, 5]
    #     index=2, parent=2//2=1
    #
    #   Iteration 2:
    #     index=2, parent=1, heap[1]=3, heap[2]=1
    #     3 > 1  →  swap  →  heap = [0, 1, 3, 8, 5]
    #     index=1  →  loop condition (index > 1) is False  →  stop
    def _bubble_up(self, index: int) -> None:
        parent_index = index // 2
        while index > 1 and self.heap[parent_index] > self.heap[index]:
            # swap the current node with its parent
            self.heap[parent_index], self.heap[index] = (
                self.heap[index], self.heap[parent_index]
            )
            index = parent_index          # move focus up to where parent was
            parent_index = index // 2    # recalculate the new parent


    # ------------------------------------------------------------------ #
    # HELPER B — _bubble_down (used by pop and heapify)                   #
    # ------------------------------------------------------------------ #
    # WHAT:  Repeatedly swap a node with its SMALLER child as long as the
    #        node is LARGER than at least one child (violating min-heap).
    #
    # WHY PICK THE SMALLER CHILD:
    #   If we swapped with the larger child, that larger value would become
    #   the parent of the smaller child, violating the heap property there.
    #   Swapping with the smaller child guarantees the new parent is ≤ both
    #   of its children after the swap.
    #
    # TERMINATION CONDITIONS:
    #   1. left_child_index >= len(self.heap)  → no children exist; at a leaf.
    #   2. heap[smaller_child] >= heap[index]  → both children are ≥ current
    #                                             node; heap property satisfied.
    #
    # WALK-THROUGH TRACE for heap = [0, 5, 3, 8] after a pop, bubble_down(1):
    #
    #   Iteration 1:
    #     index=1, left_child_index=2*1=2
    #     right child index = 3; heap[2]=3, heap[3]=8
    #     3 < 8  →  smaller child is at index 2 (value 3)
    #     heap[1]=5 > heap[2]=3  →  swap  →  heap = [0, 3, 5, 8]
    #     index=2, left_child_index=2*2=4
    #
    #   Iteration 2:
    #     left_child_index=4 >= len(heap)=4  →  loop condition False  →  stop
    #
    #   Result: [0, 3, 5, 8]  ✓
    def _bubble_down(self, index: int) -> None:
        left_child_index = 2 * index    # left child is always at 2*parent

        while left_child_index < len(self.heap):

            # --- Find the smaller of the two children ---
            # Check if a right child exists AND is smaller than the left child.
            right_child_index = left_child_index + 1
            smaller_child_index = left_child_index   # assume left is smaller

            if (right_child_index < len(self.heap) and
                    self.heap[left_child_index] > self.heap[right_child_index]):
                smaller_child_index = right_child_index  # right is actually smaller

            # --- Decide whether to swap ---
            # If the current node is already ≤ the smaller child, heap is valid.
            if self.heap[smaller_child_index] >= self.heap[index]:
                break   # no violation; stop early

            # --- Swap and move down ---
            self.heap[smaller_child_index], self.heap[index] = (
                self.heap[index], self.heap[smaller_child_index]
            )
            index = smaller_child_index          # follow the swapped value down
            left_child_index = 2 * index         # recalculate left child position


"""
================================================================================
VISUAL SUMMARY — MinHeap Algorithm Flow
================================================================================

  PUSH(val)                          POP()
  ─────────────────────────────      ──────────────────────────────────
  Append val at end of array         Save root (= minimum)
          │                                    │
          ▼                                    ▼
  ┌───────────────────┐              ┌─────────────────────────────┐
  │  _bubble_up(last) │              │  Move last leaf → root[1]   │
  │                   │              │  Shrink array by 1          │
  │  while parent >   │              └─────────────┬───────────────┘
  │  current:         │                            │
  │    swap up        │                            ▼
  │    move index up  │              ┌─────────────────────────────┐
  └───────────────────┘              │  _bubble_down(1)            │
                                     │                             │
  HEAPIFY(nums)                      │  while left child exists:   │
  ─────────────────────────────      │    pick smaller child       │
  Prepend dummy [0] + nums           │    if child < current:      │
          │                          │      swap down              │
          ▼                          │    else: break              │
  For i = last_non_leaf → 1:        └─────────────────────────────┘
      _bubble_down(i)
  (leaves are already valid;                TOP()
   only internal nodes need repair)  ─────────────────────────────
                                     return heap[1]   →  O(1)

  INDEX ARITHMETIC (1-indexed array with dummy at 0):
  ┌────────────────────────────────────────────────┐
  │  parent  of index k  →  k // 2                │
  │  left child of k     →  2 * k                 │
  │  right child of k    →  2 * k + 1             │
  └────────────────────────────────────────────────┘

================================================================================
COMPLEXITY ANALYSIS
================================================================================

  Operation   Time        Space   Reason
  ─────────── ─────────── ─────── ──────────────────────────────────────
  push        O(log n)    O(1)    Bubble up traverses tree height
  pop         O(log n)    O(1)    Bubble down traverses tree height
  top         O(1)        O(1)    Direct array read at index 1
  heapify     O(n)        O(1)*   Bottom-up repair; math proves O(n)
                                  (* O(n) extra space to store the heap)

  Overall storage for the heap array itself: O(n)
================================================================================
"""