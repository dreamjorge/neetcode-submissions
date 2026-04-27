class Solution:
    def twoSum(self, numbers: List[int], target_sum: int) -> List[int]:
        """
        Find the indices of two numbers whose sum equals the target value.

        Uses a hash map to store previously visited numbers and their indices
        for efficient O(1) average lookup.

        Args:
            numbers: List of integers.
            target_sum: Required sum of two numbers.

        Returns:
            A list with the indices of the matching pair.

        Raises:
            ValueError: If no valid pair exists.

        Time Complexity:
            O(n)

        Space Complexity:
            O(n)
        """
        value_to_index: Dict[int, int] = {}

        for current_index, current_value in enumerate(numbers):
            required_value = target_sum - current_value

            if required_value in value_to_index:
                return [value_to_index[required_value], current_index]

            value_to_index[current_value] = current_index

        raise ValueError("No two numbers sum to the target value.")