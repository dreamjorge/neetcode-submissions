from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # --- STRATEGY: Character Frequency Fingerprint ---
        # Two words are anagrams if they contain the EXACT same letters
        # with the EXACT same frequencies — just in a different order.
        #
        # Key insight: instead of sorting each word (which works but costs
        # O(k log k) per word), we build a "fingerprint" — a fixed-size
        # array of 26 counters, one per letter of the alphabet.
        #
        # Words with identical fingerprints belong to the same anagram group.
        #
        # We use defaultdict(list) so that accessing a brand-new key
        # automatically creates an empty list for us — no manual check needed.
        res = defaultdict(list)

        for s in strs:
            # --- STEP 1: Build the frequency fingerprint ---
            # 26 slots → one for each letter: index 0 = 'a', index 25 = 'z'
            # All counters start at zero.
            count = [0] * 26

            for c in s:
                # ord(c) gives the ASCII code of character c.
                # ord('a') is 97, ord('b') is 98, ..., ord('z') is 122.
                #
                # Subtracting ord('a') maps each letter to an index 0–25:
                #   'a' → 0,  'b' → 1,  'c' → 2, ..., 'z' → 25
                #
                # Example for s = "eat":
                #   'e' → index 4  → count[4]  becomes 1
                #   'a' → index 0  → count[0]  becomes 1
                #   't' → index 19 → count[19] becomes 1
                count[ord(c) - ord('a')] += 1

            # --- STEP 2: Use the fingerprint as a dictionary key ---
            # Lists cannot be dictionary keys (they are mutable),
            # so we convert our count array to a TUPLE — which is immutable
            # and therefore hashable.
            #
            # "eat", "tea", and "ate" all produce the same tuple:
            #   (1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
            #    ^a          ^e                         ^t
            #
            # So they all land in the same bucket in our dictionary.
            res[tuple(count)].append(s)

        # --- STEP 3: Return all groups ---
        # Each value in `res` is a list of words sharing the same fingerprint.
        # dict.values() gives us all those groups; we wrap it in list().
        return list(res.values())