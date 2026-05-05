from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # --- STRATEGY: Recursive DFS with Running Sum ---
        #
        # A "path" here means: from the ROOT down to a LEAF node.
        # A LEAF is a node with NO children (left is None AND right is None).
        #
        # We walk every root-to-leaf path, accumulating the sum as we go.
        # The moment we reach a leaf, we check if the accumulated sum == targetSum.
        #
        # We use an INNER FUNCTION so it can access `targetSum` from the
        # outer scope without passing it as a parameter on every call.

        def dfs(node: Optional[TreeNode], running_sum: int) -> bool:
            # --- BASE CASE: We walked past a leaf (empty node) ---
            # This happens when a leaf's child is accessed — which is None.
            # There is no value to add and no path to complete, so return False.
            if not node:
                return False

            # --- STEP 1: Accumulate the current node's value ---
            # `running_sum` tracks the total from root down to `node`.
            running_sum += node.val

            # --- STEP 2: Check if we reached a LEAF ---
            # A leaf has no children. This is the only place where a valid
            # root-to-leaf path ends, so this is the only place we can
            # confirm a match.
            is_leaf = not node.left and not node.right
            if is_leaf:
                return running_sum == targetSum

            # --- STEP 3: Recurse into both subtrees ---
            # We don't need BOTH paths to match — just ONE is enough.
            # The `or` short-circuits: if the left path matches,
            # Python never evaluates the right path.
            left_has_path  = dfs(node.left,  running_sum)
            right_has_path = dfs(node.right, running_sum)
            return left_has_path or right_has_path

        # Kick off the DFS from the root with a running sum of zero.
        return dfs(root, 0)