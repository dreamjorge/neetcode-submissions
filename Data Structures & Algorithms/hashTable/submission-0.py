"""
WHAT PROBLEM DOES A HASH TABLE SOLVE?

CORE CHALLENGE:
    We need a data structure that can store and retrieve key-value pairs
    in (ideally) O(1) time — faster than scanning a list O(n) or
    walking a tree O(log n).

WHY A NAIVE APPROACH FAILS:
    A plain list requires scanning every element to find a key.
    Example: storing 1000 entries and looking up key=999 means
    checking ~999 nodes in the worst case.

CHOSEN STRATEGY — Hash + Chaining:
    1. Convert every key into a bucket index using:
           index = key % capacity
    2. Store a linked list at each bucket to handle COLLISIONS
       (two different keys mapping to the same index).
    3. Automatically RESIZE when the table gets too full (load factor ≥ 0.5)
       to keep chains short and lookups fast.

LABELED EXAMPLE:
    capacity = 4, insert keys 5, 9, 13

    hash(5)  = 5 % 4 = 1  →  table[1] → Node(5)
    hash(9)  = 9 % 4 = 1  →  table[1] → Node(5) → Node(9)   [collision!]
    hash(13) = 13 % 4 = 1 →  table[1] → Node(5) → Node(9) → Node(13)

    Lookup key=9:
        Go to table[1], walk chain: 5 ≠ 9 → 9 == 9 ✓  return value
"""


class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.next = None  # pointer to next node in the collision chain


class HashTable:
    def __init__(self, capacity: int):
        # STEP 1 — Initialise the internal bucket array
        # We allocate `capacity` slots, all empty (None).
        # `size` tracks how many key-value pairs currently live in the table.
        # Example: capacity=8  →  self.table = [None, None, None, None, None, None, None, None]
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity

    # ------------------------------------------------------------------
    def hash_function(self, key: int) -> int:
        # STEP 2 — Map any integer key to a valid bucket index
        # Modulo guarantees the result is always in [0, capacity-1].
        # Example: key=23, capacity=8  →  23 % 8 = 7
        return key % self.capacity

    # ------------------------------------------------------------------
    def insert(self, key: int, value: int) -> None:
        """
        WHAT DOES insert DO?
            Adds a new key-value pair or updates the value of an existing key.
            After inserting, checks the load factor and resizes if needed.
        """

        # STEP 1 — Find the destination bucket
        # We hash the key to get the array index where this pair belongs.
        # Example: key=10, capacity=8  →  bucket_index = 10 % 8 = 2
        bucket_index = self.hash_function(key)
        current_node = self.table[bucket_index]

        # STEP 2 — Handle an EMPTY bucket (no collision)
        # If the slot is None, we can drop a new node directly here.
        # This is the ideal O(1) path.
        if not current_node:
            self.table[bucket_index] = Node(key, value)
            self.size += 1

        else:
            # STEP 3 — Walk the collision chain
            # If the bucket already has nodes, we must:
            #   (a) update the value if the key already exists, OR
            #   (b) append a new node at the end of the chain.
            # We keep `predecessor_node` so we can attach the new node later.
            #
            # Walk-through trace for bucket_index=2, chain = [Node(2,A), Node(10,B)],
            # inserting key=18 (new), capacity=8:
            #
            #   Iteration 1: current_node=Node(2),  key 2  ≠ 18  →  predecessor=Node(2),  advance
            #   Iteration 2: current_node=Node(10), key 10 ≠ 18  →  predecessor=Node(10), advance
            #   Iteration 3: current_node=None  →  loop ends
            #   → predecessor_node.next = Node(18, value)
            predecessor_node = None
            while current_node:
                if current_node.key == key:
                    current_node.value = value  # KEY EXISTS → just update value, no size change
                    return
                predecessor_node, current_node = current_node, current_node.next

            # Append brand-new node at the tail of the chain
            predecessor_node.next = Node(key, value)
            self.size += 1

        # STEP 4 — Check the LOAD FACTOR and resize if needed
        # Load factor = size / capacity.
        # At ≥ 0.5 chains grow long and performance degrades toward O(n).
        # Doubling the capacity halves the average chain length.
        # Example: size=4, capacity=8  →  4/8 = 0.5  →  trigger resize to capacity=16
        if self.size / self.capacity >= 0.5:
            self.resize()

    # ------------------------------------------------------------------
    def get(self, key: int) -> int:
        """
        WHAT DOES get DO?
            Returns the value associated with `key`, or -1 if not found.

        Walk-through trace for key=10, capacity=8, chain at index 2 = [Node(2,A), Node(10,B)]:
            Iteration 1: current_node=Node(2),  key 2  ≠ 10  →  advance
            Iteration 2: current_node=Node(10), key 10 == 10 →  return B
        """

        # STEP 1 — Jump directly to the correct bucket
        bucket_index = self.hash_function(key)
        current_node = self.table[bucket_index]

        # STEP 2 — Walk the chain looking for a key match
        while current_node:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next

        # STEP 3 — Key not found anywhere in the chain
        return -1

    # ------------------------------------------------------------------
    def remove(self, key: int) -> bool:
        """
        WHAT DOES remove DO?
            Deletes the node with the matching key from its chain.
            Returns True on success, False if key doesn't exist.

        WHY DO WE NEED predecessor_node?
            In a singly-linked list we cannot go backwards.
            To unlink Node(B) from  A → B → C  we need A so we can do:
                A.next = C
            Without A we can't re-wire the chain.

        Walk-through trace, removing key=10 from chain [Node(2,A) → Node(10,B) → Node(18,C)]:
            Iteration 1: current_node=Node(2),  key 2  ≠ 10  →  predecessor=Node(2),  advance
            Iteration 2: current_node=Node(10), key 10 == 10 →  predecessor.next = Node(18)
                         Node(10) is now unreachable → garbage collected
        """

        # STEP 1 — Locate the bucket
        bucket_index = self.hash_function(key)
        current_node = self.table[bucket_index]
        predecessor_node = None

        # STEP 2 — Walk the chain, tracking the node just behind current
        while current_node:
            if current_node.key == key:

                # STEP 3 — Unlink the target node
                if predecessor_node:
                    # Middle or tail node: bypass it
                    predecessor_node.next = current_node.next
                else:
                    # Head node: point bucket directly at the second node (or None)
                    self.table[bucket_index] = current_node.next

                self.size -= 1
                return True

            predecessor_node, current_node = current_node, current_node.next

        return False  # key was never in the table

    # ------------------------------------------------------------------
    def getSize(self) -> int:
        return self.size

    def getCapacity(self) -> int:
        return self.capacity

    # ------------------------------------------------------------------
    def resize(self) -> None:
        """
        WHAT DOES resize DO?
            Doubles capacity and re-inserts every existing node into a fresh
            bucket array. This is necessary because the bucket index of every
            key changes when capacity changes (index = key % NEW_capacity).

        WHY NOT RE-USE insert()?
            insert() calls resize() itself, which would cause infinite recursion.
            Instead we do a raw re-hash loop that never triggers another resize.

        Walk-through trace — capacity 4 → 8, existing nodes: key=5, key=9
            key=5: 5 % 8 = 5  →  new_table[5] = Node(5, ...)
            key=9: 9 % 8 = 1  →  new_table[1] = Node(9, ...)
            (They no longer collide! The longer table spread them apart.)
        """

        # STEP 1 — Allocate a fresh table at double the capacity
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        # STEP 2 — Walk every bucket in the OLD table
        for chain_head_node in self.table:
            current_node = chain_head_node

            # STEP 3 — Walk every node in this bucket's chain
            while current_node:
                # Re-hash using the NEW capacity
                new_bucket_index = current_node.key % new_capacity

                if new_table[new_bucket_index] is None:
                    # Empty slot — place node directly
                    new_table[new_bucket_index] = Node(current_node.key, current_node.value)
                else:
                    # Collision in new table — walk to the tail and append
                    tail_node = new_table[new_bucket_index]
                    while tail_node.next:
                        tail_node = tail_node.next
                    tail_node.next = Node(current_node.key, current_node.value)

                current_node = current_node.next  # advance through old chain

        # STEP 4 — Swap in the new table (size stays the same; only shape changed)
        self.capacity = new_capacity
        self.table = new_table


"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ALGORITHM FLOW — FULL ASCII DIAGRAM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  INSERT(key, value)
  ┌──────────────────────────────────────────────────────────────┐
  │  bucket_index = key % capacity                               │
  │       │                                                      │
  │       ▼                                                      │
  │  table[bucket_index] empty?                                  │
  │  ┌────YES──────────────────────────────────┐                 │
  │  │  Place new Node here                    │                 │
  │  └─────────────────────────────────────────┘                 │
  │  ┌────NO: walk chain──────────────────────┐                  │
  │  │  key already exists? → UPDATE value    │                  │
  │  │  reached tail?       → APPEND new Node │                  │
  │  └────────────────────────────────────────┘                  │
  │       │                                                      │
  │  size += 1                                                   │
  │  load_factor = size / capacity ≥ 0.5? → RESIZE (×2)         │
  └──────────────────────────────────────────────────────────────┘

  GET(key)
  ┌──────────────────────────────────────────────────────────────┐
  │  bucket_index = key % capacity                               │
  │  Walk chain → key match? → return value                      │
  │              No match?   → return -1                         │
  └──────────────────────────────────────────────────────────────┘

  REMOVE(key)
  ┌──────────────────────────────────────────────────────────────┐
  │  bucket_index = key % capacity                               │
  │  Walk chain with predecessor_node                            │
  │  key match?                                                  │
  │  ┌── head node:   table[index]     = node.next ──┐          │
  │  └── middle/tail: predecessor.next = node.next ──┘          │
  │  size -= 1  →  return True                                   │
  │  Not found  →  return False                                  │
  └──────────────────────────────────────────────────────────────┘

  RESIZE  (triggered when load_factor ≥ 0.5)
  ┌──────────────────────────────────────────────────────────────┐
  │  new_capacity = capacity × 2                                 │
  │  new_table    = [None] × new_capacity                        │
  │  For every node in old table:                                │
  │      new_index = key % new_capacity   ← KEY STEP            │
  │      insert into new_table chain                             │
  │  self.table    = new_table                                   │
  │  self.capacity = new_capacity                                │
  └──────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  COMPLEXITY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Operation │ Average Case │ Worst Case   │ Notes
  ──────────┼──────────────┼──────────────┼────────────────────────
  insert    │   O(1)       │   O(n)       │ Worst: all keys collide
  get       │   O(1)       │   O(n)       │ Worst: full chain scan
  remove    │   O(1)       │   O(n)       │ Worst: full chain scan
  resize    │   O(n)       │   O(n)       │ Visits every existing node
  ──────────┼──────────────┼──────────────┼────────────────────────

  SPACE COMPLEXITY
  ┌─────────────────────────────────────────────────────────────┐
  │  O(capacity + size)                                         │
  │  · capacity  = number of bucket slots allocated             │
  │  · size      = number of Node objects currently stored      │
  │  Because load_factor is capped at 0.5, capacity ≤ 2×size,  │
  │  so this simplifies to O(n) where n = number of entries.   │
  └─────────────────────────────────────────────────────────────┘
"""