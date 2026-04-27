class Solution:
    def isPalindrome(self, text: str) -> bool:
        """
        Determine whether a string is a palindrome considering only
        alphanumeric characters and ignoring letter case.

        Uses the two-pointer technique to compare characters from both ends.

        Args:
            text: Input string to evaluate.

        Returns:
            True if the cleaned string is a palindrome, otherwise False.

        Time Complexity:
            O(n)

        Space Complexity:
            O(1)
        """
        left_index = 0
        right_index = len(text) - 1

        while left_index < right_index:
            while (
                left_index < right_index
                and not self._is_alphanumeric(text[left_index])
            ):
                left_index += 1

            while (
                left_index < right_index
                and not self._is_alphanumeric(text[right_index])
            ):
                right_index -= 1

            if text[left_index].lower() != text[right_index].lower():
                return False

            left_index += 1
            right_index -= 1

        return True

    def _is_alphanumeric(self, character: str) -> bool:
        """
        Check whether a character is alphanumeric using ASCII ranges.

        Args:
            character: Single character to validate.

        Returns:
            True if the character is a letter or digit, otherwise False.
        """
        return (
            ord("A") <= ord(character) <= ord("Z")
            or ord("a") <= ord(character) <= ord("z")
            or ord("0") <= ord(character) <= ord("9")
        )