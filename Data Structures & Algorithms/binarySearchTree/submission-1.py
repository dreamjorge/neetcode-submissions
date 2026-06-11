# ============================================================
# WHAT PROBLEM DOES TreeMap SOLVE?
# ============================================================
# CHALLENGE:
#   We need a key-value store where keys are always kept in
#   sorted order, and we can efficiently insert, look up,
#   find the min/max, delete, and traverse in sorted order.
#
# WHY A PLAIN DICT FAILS:
#   Python dicts are unordered (insertion order only).
#   They give us no way to ask "what is the smallest key?"
#   or walk all keys in sorted order without sorting first.
#
# CHOSEN STRATEGY — Binary Search Tree (BST):
#   Every node stores (key, val).
#   Invariant: left subtree keys < node.key < right subtree keys
#
#   Example tree after inserting keys 5, 3, 7, 1, 4:
#
#          5
#         / \
#        3   7
#       / \
#      1   4
#
#   - Smallest key  → keep going left  → 1
#   - Largest key   → keep going right → 7
#   - Sorted order  → in-order traversal (left, root, right) → [1,3,4,5,7]
# ============================================================

from typing import List


class TreeNode:

       # ----------------------------------------------------------
    # CAMELCASE ALIASES  (keeps compatibility with existing callers)
    # ----------------------------------------------------------

    """A single node in the BST holding a key-value pair."""
    def __init__(self, key: int, val: int):
        self.key   = key    # used for ordering / lookup
        self.val   = val    # the payload we actually want to store
        self.left  = None   # pointer to left  child (smaller keys)
        self.right = None   # pointer to right child (larger  keys)


class TreeMap:

       # ----------------------------------------------------------
    # CAMELCASE ALIASES  (keeps compatibility with existing callers)
    # ----------------------------------------------------------
    def getMin(self)                          -> int:        return self.get_min()
    def getMax(self)                          -> int:        return self.get_max()
    def getInorderKeys(self)                  -> List[int]:  return self.get_inorder_keys()
    def findMin(self, node: TreeNode)         -> TreeNode:   return self._find_min(node)
    def removeHelper(self, node: TreeNode, key: int) -> TreeNode:
                                                             return self._remove_helper(node, key)
    def __init__(self):
        self.root = None   # empty tree

    # ----------------------------------------------------------
    # INSERT
    # ----------------------------------------------------------
    def insert(self, key: int, val: int) -> None:
        """
        WHAT insert DOES:
          Adds a new (key, val) pair, or overwrites val if key exists.

        STEP 1 — Handle empty tree:
          If the tree is empty, the new node becomes the root directly.
          Example: insert(5, 'a') into empty tree → root = Node(5,'a')

        STEP 2 — Walk down to the correct spot:
          Compare the new key against current_node.key at every level.
          Go left  if new key is smaller.
          Go right if new key is larger.
          Stop as soon as we hit an empty child slot and attach there.
          If we find an exact key match, just update the value (no duplicates).

        WALK-THROUGH — insert keys 5, 3, 7, 1 in order:
          After insert(5):  root=5
          After insert(3):  3 < 5 → go left, slot empty → root.left=3
          After insert(7):  7 > 5 → go right, slot empty → root.right=7
          After insert(1):  1 < 5 → go left (node 3)
                            1 < 3 → go left, slot empty → node(3).left=1
        """
        new_node = TreeNode(key, val)

        # STEP 1 — Empty tree: first node becomes root
        if self.root is None:
            self.root = new_node
            return

        # STEP 2 — Walk down until we find the right empty slot
        current_node = self.root
        while True:
            if key < current_node.key:
                if current_node.left is None:          # empty slot found
                    current_node.left = new_node
                    return
                current_node = current_node.left       # keep walking left
            elif key > current_node.key:
                if current_node.right is None:         # empty slot found
                    current_node.right = new_node
                    return
                current_node = current_node.right      # keep walking right
            else:
                current_node.val = val                 # duplicate key → update value only
                return

    # ----------------------------------------------------------
    # GET
    # ----------------------------------------------------------
    def get(self, key: int) -> int:
        """
        WHAT get DOES:
          Looks up the value stored under a given key.
          Returns -1 if the key does not exist.

        STEP 1 — Walk down the BST using key comparisons:
          Same navigation as insert: go left if key is smaller,
          right if larger, return val on exact match.

        WHY NOT a linear scan?
          A scan would be O(n). BST navigation is O(log n) on
          average because each comparison halves the remaining search space.

        WALK-THROUGH — get(3) on tree {5, 3, 7, 1, 4}:
          current = 5  →  3 < 5  → go left
          current = 3  →  3 == 3 → return val ✓
        """
        current_node = self.root
        while current_node is not None:
            if key < current_node.key:
                current_node = current_node.left
            elif key > current_node.key:
                current_node = current_node.right
            else:
                return current_node.val   # exact match
        return -1   # fell off the tree → key not found

    # ----------------------------------------------------------
    # GET MIN / GET MAX
    # ----------------------------------------------------------
    def get_min(self) -> int:
        """
        WHAT get_min DOES:
          Returns the value associated with the smallest key in the tree.

        STEP 1 — Reuse find_min helper:
          The BST invariant guarantees the leftmost node always holds
          the smallest key, so we just keep walking left until
          there is no more left child.

        Example on {5, 3, 7, 1, 4}:
          5 → left → 3 → left → 1 → no left child → min key = 1
        """
        minimum_node = self._find_min(self.root)
        return minimum_node.val if minimum_node else -1

    def _find_min(self, subtree_root: TreeNode) -> TreeNode:
        """
        Helper — walks as far left as possible.
        Used by both get_min and remove (to find the in-order successor).

        WALK-THROUGH on subtree rooted at 3 (nodes 3, 1, 4):
          node = 3 → has left (1) → node = 1 → no left → return node(1)
        """
        current_node = subtree_root
        while current_node and current_node.left:
            current_node = current_node.left
        return current_node

    def get_max(self) -> int:
        """
        WHAT get_max DOES:
          Returns the value associated with the largest key in the tree.

        STEP 1 — Mirror of get_min:
          Keep walking right until there is no more right child.
          The rightmost node holds the largest key by BST invariant.

        Example on {5, 3, 7, 1, 4}:
          5 → right → 7 → no right child → max key = 7
        """
        current_node = self.root
        while current_node and current_node.right:
            current_node = current_node.right
        return current_node.val if current_node else -1

    # ----------------------------------------------------------
    # REMOVE
    # ----------------------------------------------------------
    def remove(self, key: int) -> None:
        """
        WHAT remove DOES:
          Deletes the node with the given key while keeping the BST invariant.
          Uses a recursive helper that rebuilds parent→child pointers on the
          way back up the call stack.
        """
        self.root = self._remove_helper(self.root, key)

    def _remove_helper(self, current_node: TreeNode, key: int) -> TreeNode:
        """
        STEP 1 — Navigate to the target node:
          Recurse left or right until we reach the node whose key matches,
          or None (key not found — nothing to do).

        STEP 2 — Three deletion cases once we find the target:

          CASE A — Node has no left child:
            Promote the right child upward to take this node's place.
            Example: remove 7 from { 5, 3, 7(right=9) }
            → node(7) replaced by node(9)

          CASE B — Node has no right child:
            Promote the left child upward.
            Example: remove 3 from { 5, 3(left=1) }
            → node(3) replaced by node(1)

          CASE C — Node has BOTH children (the tricky case):
            We cannot simply delete it — we'd disconnect a subtree.
            Strategy: replace this node's (key, val) with those of its
            IN-ORDER SUCCESSOR (the smallest key in the right subtree),
            then delete that successor node from the right subtree instead.

            WHY the in-order successor?
              It is the next-larger key after current_node, so swapping it in
              preserves the BST invariant on both sides:
                - Everything in left subtree is still smaller than successor's key.
                - Everything remaining in right subtree is still larger.

            WALK-THROUGH — remove 5 from {5, 3, 7, 1, 4, 6, 9}:
              current_node.key = 5, has both children.
              In-order successor = _find_min(right subtree) = node(6).
              Copy key=6, val=val_of_6 into current node.
              Recurse: _remove_helper(right_subtree, 6) → deletes original 6.
              Result tree: root becomes 6, left=3, right=7(left=None, right=9) ✓

        STEP 3 — Return current_node:
          Each recursive call returns the (possibly replaced) subtree root,
          which the parent call re-attaches via curr.left = ... or curr.right = ...
        """
        # STEP 1 — Base case: key not found
        if current_node is None:
            return None

        # STEP 1 (continued) — Navigate toward the target
        if key > current_node.key:
            current_node.right = self._remove_helper(current_node.right, key)
        elif key < current_node.key:
            current_node.left = self._remove_helper(current_node.left, key)

        # STEP 2 — We are now AT the node to delete
        else:
            # CASE A — No left child: promote right child
            if current_node.left is None:
                return current_node.right

            # CASE B — No right child: promote left child
            elif current_node.right is None:
                return current_node.left

            # CASE C — Two children: swap with in-order successor, then delete successor
            else:
                inorder_successor = self._find_min(current_node.right)
                current_node.key  = inorder_successor.key   # overwrite with successor data
                current_node.val  = inorder_successor.val
                # Now delete the successor from the right subtree (it has at most one child)
                current_node.right = self._remove_helper(
                    current_node.right, inorder_successor.key
                )

        # STEP 3 — Return the (unchanged or modified) node to re-attach to parent
        return current_node

    # ----------------------------------------------------------
    # IN-ORDER TRAVERSAL
    # ----------------------------------------------------------
    def get_inorder_keys(self) -> List[int]:
        """
        WHAT get_inorder_keys DOES:
          Returns all keys in ascending sorted order.
          This is one of the primary advantages of a BST over a hash map.
        """
        sorted_keys = []
        self._inorder_traversal(self.root, sorted_keys)
        return sorted_keys

    def _inorder_traversal(self, current_node: TreeNode, sorted_keys: List[int]) -> None:
        """
        STEP 1 — Recurse left subtree first (smaller keys).
        STEP 2 — Append current node's key (middle value).
        STEP 3 — Recurse right subtree last (larger keys).

        WHY left → root → right?
          That visit order follows the BST invariant directly:
          everything left is smaller, then current, then everything right is larger.

        WALK-THROUGH on {5, 3, 7, 1, 4}:
          _inorder(5) → _inorder(3) → _inorder(1)
            → _inorder(None) [left of 1]
            → append 1   → sorted_keys = [1]
            → _inorder(None) [right of 1]
          → append 3   → sorted_keys = [1, 3]
          → _inorder(4)
            → append 4   → sorted_keys = [1, 3, 4]
          → append 5   → sorted_keys = [1, 3, 4, 5]
          → _inorder(7)
            → append 7   → sorted_keys = [1, 3, 4, 5, 7]
        """
        if current_node is None:
            return
        self._inorder_traversal(current_node.left,  sorted_keys)  # STEP 1
        sorted_keys.append(current_node.key)                       # STEP 2
        self._inorder_traversal(current_node.right, sorted_keys)   # STEP 3