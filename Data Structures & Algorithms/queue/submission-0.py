"""
WHAT PROBLEM DOES Deque SOLVE?

CHALLENGE:
A deque (double-ended queue) needs O(1) insert and delete from BOTH ends.
A plain Python list fails this because inserting or removing at index 0
forces every existing element to shift one position → O(n).

WHY A PLAIN LIST FAILS:
    items = [10, 20, 30]
    items.insert(0, 5)   # shifts 10, 20, 30 one slot right → O(n)
    items.pop(0)         # shifts 20, 30 one slot left      → O(n)

CHOSEN STRATEGY — Doubly Linked List with Sentinel Nodes:
Every node holds a value plus two pointers: one toward the tail (next_node)
and one toward the head (prev_node). Two permanent "dummy" sentinel nodes
(sentinel_head, sentinel_tail) act as fixed anchors. Real data nodes always
live BETWEEN them. Every insert/delete rewires exactly four pointers → O(1).

LABELED EXAMPLE:
    Input operations: append(10), append(20), appendleft(5)

    After append(10):
        sentinel_head <-> [10] <-> sentinel_tail

    After append(20):
        sentinel_head <-> [10] <-> [20] <-> sentinel_tail

    After appendleft(5):
        sentinel_head <-> [5] <-> [10] <-> [20] <-> sentinel_tail

    pop()     → removes [20], returns 20
    popleft() → removes [5],  returns 5

    Final state:
        sentinel_head <-> [10] <-> sentinel_tail
"""


# ─────────────────────────────────────────────
#  NODE
# ─────────────────────────────────────────────

class Node:
    """One element of the doubly linked list."""

    def __init__(self, value: int):
        self.value = value
        self.next_node = None   # points toward sentinel_tail
        self.prev_node = None   # points toward sentinel_head


# ─────────────────────────────────────────────
#  DEQUE
# ─────────────────────────────────────────────

class Deque:

    # ── STEP 1 · Create the two sentinel anchors ─────────────────────────
    # WHY SENTINELS: without them, every insert/delete needs a special case
    # for an empty list ("there is no previous node yet"). Sentinels
    # guarantee a left neighbour and a right neighbour always exist, so the
    # same four-pointer rewire works whether the deque holds 0 or 1000 items.
    #
    # INITIAL STATE (empty deque):
    #   sentinel_head.next_node ──► sentinel_tail
    #   sentinel_tail.prev_node ──► sentinel_head

    def __init__(self):
        self.sentinel_head = Node(-1)   # left anchor — value is never read
        self.sentinel_tail = Node(-1)   # right anchor — value is never read

        self.sentinel_head.next_node = self.sentinel_tail
        self.sentinel_tail.prev_node = self.sentinel_head


    # ── STEP 2 · is_empty ────────────────────────────────────────────────
    # The deque is empty when the two sentinels are direct neighbours,
    # meaning no real node exists between them.
    #
    # Example (empty):     sentinel_head.next_node IS sentinel_tail → True
    # Example (non-empty): sentinel_head.next_node is Node(10)      → False

    def is_empty(self) -> bool:
        return self.sentinel_head.next_node is self.sentinel_tail


    # ── STEP 3 · append — insert at the BACK ────────────────────────────
    # Place new_node immediately to the left of sentinel_tail.
    #
    # WHY THIS ORDER: we read last_real_node BEFORE changing any pointers.
    # If we moved sentinel_tail.prev_node first we would lose the reference
    # to the node that was previously last.
    #
    # BEFORE append(30), deque = [10, 20]:
    #   sentinel_head <-> [10] <-> [20] <-> sentinel_tail
    #                               ↑ last_real_node
    #
    # Four-pointer rewire:
    #   ① last_real_node.next_node = new_node       old last looks right → new
    #   ② new_node.prev_node       = last_real_node  new looks left  → old last
    #   ③ new_node.next_node       = sentinel_tail   new looks right → tail
    #   ④ sentinel_tail.prev_node  = new_node        tail looks left → new
    #
    # AFTER:
    #   sentinel_head <-> [10] <-> [20] <-> [30] <-> sentinel_tail

    def append(self, value: int) -> None:
        new_node = Node(value)
        last_real_node = self.sentinel_tail.prev_node   # capture before rewiring

        last_real_node.next_node = new_node             # ①
        new_node.prev_node       = last_real_node        # ②
        new_node.next_node       = self.sentinel_tail    # ③
        self.sentinel_tail.prev_node = new_node          # ④


    # ── STEP 4 · appendleft — insert at the FRONT ───────────────────────
    # Mirror image of append: place new_node immediately to the right of
    # sentinel_head.
    #
    # BEFORE appendleft(5), deque = [10, 20]:
    #   sentinel_head <-> [10] <-> [20] <-> sentinel_tail
    #                      ↑ first_real_node
    #
    # Four-pointer rewire:
    #   ① self.sentinel_head.next_node = new_node        head looks right → new
    #   ② new_node.prev_node           = sentinel_head   new looks left  → head
    #   ③ new_node.next_node           = first_real_node new looks right → old first
    #   ④ first_real_node.prev_node    = new_node        old first looks left → new
    #
    # AFTER:
    #   sentinel_head <-> [5] <-> [10] <-> [20] <-> sentinel_tail

    def appendleft(self, value: int) -> None:
        new_node = Node(value)
        first_real_node = self.sentinel_head.next_node  # capture before rewiring

        self.sentinel_head.next_node = new_node          # ①
        new_node.prev_node           = self.sentinel_head # ②
        new_node.next_node           = first_real_node    # ③
        first_real_node.prev_node    = new_node           # ④


    # ── STEP 5 · pop — remove from the BACK ─────────────────────────────
    # Find the last real node, save its value, then bridge sentinel_tail
    # directly to the node that was second-to-last. The removed node has no
    # remaining references → Python garbage-collects it automatically.
    #
    # BEFORE pop(), deque = [10, 20, 30]:
    #   sentinel_head <-> [10] <-> [20] <-> [30] <-> sentinel_tail
    #                                        ↑ last_real_node
    #                               ↑ node_before_last
    #
    # Two-pointer bridge:
    #   node_before_last.next_node  = sentinel_tail
    #   sentinel_tail.prev_node     = node_before_last
    #
    # AFTER:
    #   sentinel_head <-> [10] <-> [20] <-> sentinel_tail
    # Returns: 30

    def pop(self) -> int:
        if self.is_empty():
            return -1

        last_real_node   = self.sentinel_tail.prev_node
        node_before_last = last_real_node.prev_node
        removed_value    = last_real_node.value

        node_before_last.next_node   = self.sentinel_tail   # bridge right
        self.sentinel_tail.prev_node = node_before_last      # bridge left
        return removed_value


    # ── STEP 6 · popleft — remove from the FRONT ────────────────────────
    # Mirror image of pop.
    #
    # BEFORE popleft(), deque = [5, 10, 20]:
    #   sentinel_head <-> [5] <-> [10] <-> [20] <-> sentinel_tail
    #                      ↑ first_real_node
    #                              ↑ node_after_first
    #
    # Two-pointer bridge:
    #   sentinel_head.next_node    = node_after_first
    #   node_after_first.prev_node = sentinel_head
    #
    # AFTER:
    #   sentinel_head <-> [10] <-> [20] <-> sentinel_tail
    # Returns: 5

    def popleft(self) -> int:
        if self.is_empty():
            return -1

        first_real_node  = self.sentinel_head.next_node
        node_after_first = first_real_node.next_node
        removed_value    = first_real_node.value

        self.sentinel_head.next_node = node_after_first      # bridge right
        node_after_first.prev_node   = self.sentinel_head    # bridge left
        return removed_value

    def isEmpty(self) -> bool:
        return self.is_empty()

    def appendLeft(self, value: int) -> None:
        self.appendleft(value)

    def popLeft(self) -> int:
        return self.popleft()