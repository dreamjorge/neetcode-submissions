class Solution:
    def isPalindrome(self, text: str) -> bool:
        """
        Check if a string is a palindrome.

        A palindrome reads the same forward and backward once we:
        1. Ignore spaces, symbols, and punctuation.
        2. Ignore uppercase/lowercase differences.

        Examples:
            "racecar" -> True
            "A man, a plan, a canal: Panama" -> True
            "hello" -> False

        Strategy:
        We use two pointers:

        - left_index  -> starts at the beginning
        - right_index -> starts at the end

        Then:
        1. Move left_index forward until it points to a letter/number.
        2. Move right_index backward until it points to a letter/number.
        3. Compare both characters in lowercase.
        4. If different -> not palindrome.
        5. If equal -> move both pointers inward.
        6. Continue until pointers cross.

        Why this is efficient:
        - We scan the string only once.
        - No extra cleaned string is created.

        Time Complexity:
            O(n)  -> each character is visited at most once

        Space Complexity:
            O(1)  -> only pointer variables are used
        """
        left_index = 0
        right_index = len(text) - 1

        while left_index < right_index:

            # Move left pointer until it finds a valid character
            while (
                left_index < right_index
                and not self._is_alphanumeric(text[left_index])
            ):
                left_index += 1

            # Move right pointer until it finds a valid character
            while (
                left_index < right_index
                and not self._is_alphanumeric(text[right_index])
            ):
                right_index -= 1

            left_char = text[left_index].lower()
            right_char = text[right_index].lower()

            # If characters do not match, it is not palindrome
            if left_char != right_char:
                return False

            # Move both pointers toward center
            left_index += 1
            right_index -= 1

        # If all comparisons matched
        return True

    def _is_alphanumeric(self, character: str) -> bool:
        """
        Return True if character is:
        - A-Z
        - a-z
        - 0-9

        We use ASCII values with ord().

        Example:
            ord("A") = 65
            ord("a") = 97
            ord("0") = 48
        """
        return (
            ord("A") <= ord(character) <= ord("Z")
            or ord("a") <= ord(character) <= ord("z")
            or ord("0") <= ord(character) <= ord("9")
        )