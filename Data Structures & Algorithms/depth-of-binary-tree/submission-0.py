from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # --- STRATEGY: Iterative DFS with an Explicit Stack ---
        # We want to find the longest path from the root down to any leaf node.
        #
        # Instead of recursion, we simulate the traversal manually using
        # a STACK — a list where we always add and remove from the END (LIFO).
        # This mimics how recursive calls work under the hood.
        #
        # Each entry in the stack stores a PAIR:
        #   [node, depth]  →  "I am at this node, and I am this many levels deep"
        #
        # We start at the root, which is at depth 1.
        # If the tree is empty (root is None), the stack starts as [[None, 1]]
        # but the while loop will immediately skip the update since node is None.
        stack = [[root, 1]]

        # `max_depth` tracks the deepest level we have reached so far.
        max_depth = 0

        # --- MAIN LOOP: Process nodes until the stack is empty ---
        while stack:

            # --- STEP 1: Pop the top entry from the stack ---
            # stack.pop() removes and returns the LAST element (most recently added).
            # We unpack the pair directly into `node` and `current_depth`.
            node, current_depth = stack.pop()

            # --- STEP 2: Process only real (non-None) nodes ---
            # None entries represent missing children — there is nothing to visit.
            if node:
                # Update the global maximum if this node is deeper than any seen before.
                max_depth = max(max_depth, current_depth)

                # --- STEP 3: Push both children onto the stack ---
                # Each child is one level deeper than the current node.
                # We push them even if they are None — the `if node` check
                # above will safely skip them when they are popped next.
                stack.append([node.left,  current_depth + 1])
                stack.append([node.right, current_depth + 1])

        # --- DONE ---
        # The stack is empty — every node has been visited.
        # `max_depth` now holds the length of the longest root-to-leaf path.
        return max_depth