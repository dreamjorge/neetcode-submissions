# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        # --- STRATEGY: Dummy Head Node ---
        # We create a temporary "dummy" node as the starting anchor.
        # It has no real value — it's just a convenient fixed point
        # so we don't have to handle the "empty result list" edge case separately.
        #
        # Both `dummy` and `node` point to the SAME object initially.
        # - `dummy` stays fixed at the start → lets us return the final list later.
        # - `node` moves forward as we build the merged list.
        dummy = node = ListNode()

        # --- STEP 1: Merge while BOTH lists still have nodes ---
        # We compare the front values of list1 and list2 at each step.
        # The node with the smaller value gets appended to our result.
        while list1 and list2:

            if list1.val < list2.val:
                # list1's current node is smaller → attach it to the merged list
                node.next = list1
                # Advance list1 to its next node
                list1 = list1.next
            else:
                # list2's current node is smaller (or equal) → attach it instead
                node.next = list2
                # Advance list2 to its next node
                list2 = list2.next

            # Move our `node` pointer forward to keep building at the tail
            node = node.next

        # --- STEP 2: Attach the leftover tail ---
        # When the while loop ends, AT LEAST ONE list is exhausted.
        # The other list (if non-empty) is already sorted, so we simply
        # link the remaining nodes directly — no need to loop again.
        #
        # `list1 or list2` returns whichever one still has nodes (or None if both are empty).
        node.next = list1 or list2

        # --- STEP 3: Return the merged list ---
        # `dummy` still points to our placeholder node.
        # The REAL merged list begins at dummy.next.
        return dummy.next