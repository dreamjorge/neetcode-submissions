"""
WHAT PROBLEM DOES LinkedList SOLVE?

CHALLENGE:
  A linked list is a linear data structure where each element ("node") stores
  a value AND a pointer to the next node. Unlike Python lists (arrays), nodes
  are NOT stored contiguously in memory — they are scattered, and only the
  pointer chain connects them.

  This implementation uses a "dummy head" sentinel node at position -1 to
  simplify edge cases (inserting/removing at the very front without special
  handling).

WHY NAIVE APPROACHES FAIL:
  Without a dummy head, inserting at index 0 requires special-casing:
    "is the list empty? is this the head?" — two separate logic paths.
  With a dummy head, the real first node is always at head.next, and
  every insertion/removal looks the same regardless of position.

STRATEGY — Dummy Head + Tail Pointer:
  Input:  insertHead(1) → insertTail(2) → insertTail(3)
  Steps:
    dummy(-1) → 1 → None          (after insertHead(1), tail = node(1))
    dummy(-1) → 1 → 2 → None      (after insertTail(2), tail = node(2))
    dummy(-1) → 1 → 2 → 3 → None  (after insertTail(3), tail = node(3))
  Output: getValues() → [1, 2, 3]

  We keep a `tail` pointer so insertTail() is O(1) — no full traversal needed.
"""

from typing import List


# ---------------------------------------------------------------------------
# NODE DEFINITION
# ---------------------------------------------------------------------------

class ListNode:
    """A single node in the singly linked list."""

    def __init__(self, node_value, next_node=None):
        self.val = node_value    # The data this node holds
        self.next = next_node    # Pointer to the next node (or None if last)


# ---------------------------------------------------------------------------
# LINKED LIST IMPLEMENTATION
# ---------------------------------------------------------------------------

class LinkedList:

    def __init__(self):
        # STEP 1 — Create the sentinel (dummy) head node.
        #
        # WHAT:  A permanent dummy node at the front with value -1.
        #        It is never returned to the user; it just anchors the list.
        # WHY:   With a dummy head, self.head.next is ALWAYS the first real
        #        node (or None if the list is empty). This eliminates special
        #        cases in insert/remove when operating at index 0.
        # EXAMPLE:
        #   Empty list:  dummy(-1) → None
        #   After one insert: dummy(-1) → node(5) → None

        self.head = ListNode(-1)   # sentinel / dummy head node
        self.tail = self.head      # tail starts pointing at the dummy head
                                   # (means "list is currently empty")


    # -----------------------------------------------------------------------
    # GET
    # -----------------------------------------------------------------------

    def get(self, target_index: int) -> int:
        """
        STEP 1 — Walk from the first real node until we reach target_index.

        WHAT:  Traverse the list counting from 0. Return the value when the
               walk counter matches target_index.
        WHY:   Linked lists have no random access (no arr[i]). We must walk
               pointer-by-pointer; there's no faster way for a singly linked list.
        EXAMPLE:
          List:  dummy → 10 → 20 → 30 → None
          get(1):
            current_node = node(10), walk_counter = 0  → not 1, advance
            current_node = node(20), walk_counter = 1  → match! return 20
        """

        current_node = self.head.next   # skip the dummy head
        walk_counter = 0

        # LOOP WALK-THROUGH for get(1) on list [10, 20, 30]:
        #   Iteration 1: walk_counter=0, current_node.val=10 → 0≠1, advance
        #   Iteration 2: walk_counter=1, current_node.val=20 → match, return 20

        while current_node:
            if walk_counter == target_index:
                return current_node.val
            walk_counter += 1
            current_node = current_node.next

        return -1   # target_index is out of bounds or list is empty


    # -----------------------------------------------------------------------
    # INSERT HEAD
    # -----------------------------------------------------------------------

    def insertHead(self, new_value: int) -> None:
        """
        STEP 1 — Create a new node that points to the current first real node.
        STEP 2 — Rewire dummy head's .next to point to this new node.
        STEP 3 — Update tail if the list was empty before insertion.

        WHAT:  Insert a new node immediately after the dummy head.
        WHY:   O(1) — no traversal needed. The dummy head gives us direct
               access to the front insertion point at all times.
        EXAMPLE:
          Before: dummy(-1) → 5 → None     (tail = node(5))
          Insert 3:
            new_node(3).next = node(5)       ← STEP 1
            dummy.next = new_node(3)         ← STEP 2
          After:  dummy(-1) → 3 → 5 → None  (tail still = node(5))

          Edge case — empty list:
          Before: dummy(-1) → None           (tail = dummy)
          Insert 7:
            new_node(7).next = None          ← STEP 1
            dummy.next = new_node(7)         ← STEP 2
            tail = new_node(7)               ← STEP 3 (list was empty)
          After: dummy(-1) → 7 → None        (tail = node(7))
        """

        # STEP 1 — Build new node; it inherits the current first real node as its next
        new_node = ListNode(new_value)
        new_node.next = self.head.next

        # STEP 2 — Dummy head now points at the new node (it becomes the new front)
        self.head.next = new_node

        # STEP 3 — If new_node.next is None, the list was empty before; tail must update
        if not new_node.next:
            self.tail = new_node


    # -----------------------------------------------------------------------
    # INSERT TAIL
    # -----------------------------------------------------------------------

    def insertTail(self, new_value: int) -> None:
        """
        STEP 1 — Attach a new node after the current tail.
        STEP 2 — Advance the tail pointer to the newly added node.

        WHAT:  Append a new node at the end of the list.
        WHY:   O(1) because we always hold a `tail` pointer. Without it,
               we'd need to walk the entire list to find the last node — O(n).
        EXAMPLE:
          Before: dummy(-1) → 1 → 2 → None   (tail = node(2))
          insertTail(3):
            tail.next = new_node(3)           ← STEP 1
            tail = new_node(3)                ← STEP 2
          After:  dummy(-1) → 1 → 2 → 3 → None  (tail = node(3))
        """

        # STEP 1 — The current tail's .next was None; now it points to the new node
        self.tail.next = ListNode(new_value)

        # STEP 2 — Advance tail to the newly created node
        self.tail = self.tail.next


    # -----------------------------------------------------------------------
    # REMOVE
    # -----------------------------------------------------------------------

    def remove(self, target_index: int) -> bool:
        """
        STEP 1 — Walk to the node BEFORE the one we want to remove (the "predecessor").
        STEP 2 — Skip over the target node by rewiring predecessor.next.
        STEP 3 — If we removed the tail, update self.tail to the predecessor.

        WHAT:  Remove the node at target_index from the list.
        WHY:   In a singly linked list we can only "skip" a node from its
               predecessor — we can't unlink a node from the node itself.
               The dummy head means the predecessor of index 0 is always
               self.head (the dummy), so no special case is needed.
        EXAMPLE:
          List:  dummy(-1) → 10 → 20 → 30 → None   (tail = node(30))
          remove(1)  (remove the node with value 20):

          Walk to predecessor of index 1 (stop at index 0):
            walk_counter=0, predecessor=dummy(-1)
            → loop runs once: walk_counter becomes 1? No wait — see walk-through below.

          LOOP WALK-THROUGH for remove(1):
            Start:       walk_counter=0, predecessor=dummy(-1)
            Iteration 1: walk_counter=0 < 1 → advance: walk_counter=1, predecessor=node(10)
            Exit loop:   walk_counter=1 == target_index → predecessor is node(10) ✓

          predecessor.next = node(20)  → the node to remove
          predecessor.next.next = node(30)
          Rewire: predecessor.next = node(30)
          After: dummy(-1) → 10 → 30 → None  (tail still = node(30))

          TAIL EDGE CASE — remove(2) (removing node(30), which IS the tail):
            predecessor = node(20)
            predecessor.next == self.tail → update self.tail = node(20)
            node(20).next = None
          After: dummy(-1) → 10 → 20 → None  (tail = node(20))
        """

        walk_counter = 0
        predecessor = self.head    # start at dummy so index 0 has a predecessor

        # STEP 1 — Advance until predecessor is just before the target index
        while walk_counter < target_index and predecessor:
            walk_counter += 1
            predecessor = predecessor.next

        # STEP 2 — Remove the node ahead of predecessor (if both exist)
        if predecessor and predecessor.next:

            # STEP 3 — If the node being removed is the tail, pull tail back
            if predecessor.next == self.tail:
                self.tail = predecessor

            predecessor.next = predecessor.next.next   # skip over the target node
            return True

        return False   # target_index was out of bounds


    # -----------------------------------------------------------------------
    # GET VALUES
    # -----------------------------------------------------------------------

    def getValues(self) -> List[int]:
        """
        STEP 1 — Walk every real node and collect its value into a list.
        STEP 2 — Return the collected list.

        WHAT:  Return all node values in order as a plain Python list.
        WHY:   Building a list and returning it is O(n) time, O(n) space —
               the minimum possible since we must visit every node once.
        EXAMPLE:
          List:  dummy(-1) → 4 → 7 → 2 → None
          Walk:  collected = [4, 7, 2]
          Return [4, 7, 2]
        """

        current_node = self.head.next   # skip dummy head
        collected_values = []

        # LOOP WALK-THROUGH for list [4, 7, 2]:
        #   Iteration 1: current_node.val=4  → collected=[4],  advance
        #   Iteration 2: current_node.val=7  → collected=[4,7], advance
        #   Iteration 3: current_node.val=2  → collected=[4,7,2], advance
        #   current_node = None → exit loop

        while current_node:
            collected_values.append(current_node.val)
            current_node = current_node.next

        return collected_values


"""
╔══════════════════════════════════════════════════════════════════════╗
║              LINKED LIST — ALGORITHM FLOW DIAGRAM                   ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  MEMORY LAYOUT (after insertHead(1), insertTail(2), insertTail(3))  ║
║                                                                      ║
║   self.head                             self.tail                   ║
║       │                                     │                       ║
║       ▼                                     ▼                       ║
║  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          ║
║  │ val: -1 │──▶│ val:  1 │───▶│ val:  2 │───▶│ val:  3│───▶None  ║
║  │ (dummy) │    │         │    │         │    │         │          ║
║  └─────────┘    └─────────┘    └─────────┘    └─────────┘          ║
║   index: -       index: 0       index: 1       index: 2            ║
║                                                                      ║
║  insertHead(v) ─▶ O(1)  new node wired right after dummy head       ║
║  insertTail(v) ─▶ O(1)  tail pointer lets us skip full traversal    ║
║  remove(i)     ─▶ O(n)  must walk to predecessor at index i-1       ║
║  get(i)        ─▶ O(n)  must walk from head to index i              ║
║  getValues()   ─▶ O(n)  full traversal to collect all values        ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  TIME COMPLEXITY                                                     ║
║    insertHead / insertTail : O(1)  — direct pointer rewire          ║
║    get / remove / getValues: O(n)  — traversal required             ║
║                                                                      ║
║  SPACE COMPLEXITY                                                    ║
║    Structure overall       : O(n)  — one node per stored element    ║
║    Per-operation overhead  : O(1)  — only a few local pointer vars  ║
╚══════════════════════════════════════════════════════════════════════╝
"""