from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # --- STRATEGY: Recursive Tree Traversal ---
        # To invert a binary tree, every node must have its
        # left and right children swapped.
        #
        # The key insight: if we swap the children of EVERY node
        # (from top to bottom), the entire tree becomes its mirror image.
        #
        # We use RECURSION — the function calls itself on smaller
        # subproblems until it reaches a base case.

        # --- BASE CASE: Empty node ---
        # If the current node does not exist, there is nothing to invert.
        # This also handles the case where root itself is None (empty tree).
        # Returning None unwinds the recursion safely.
        if not root:
            return None

        # --- STEP 1: Swap the left and right children ---
        # Python allows simultaneous assignment, so both sides are
        # evaluated BEFORE any assignment happens. No temporary variable needed.
        #
        # Before swap:          After swap:
        #       4                     4
        #      / \                   / \
        #     2   7       →         7   2
        #    / \ / \               / \ / \
        #   1  3 6  9             9  6 3  1
        root.left, root.right = root.right, root.left

        # --- STEP 2: Recursively invert the LEFT subtree ---
        # Now we go deeper and repeat the same swap logic
        # for every node in the left subtree.
        self.invertTree(root.left)

        # --- STEP 3: Recursively invert the RIGHT subtree ---
        # Same process for the right subtree.
        self.invertTree(root.right)

        # --- STEP 4: Return the current node ---
        # The node itself hasn't moved — only its children were swapped.
        # Returning root lets the parent node continue its own recursion.
        return root