from typing import List


class Solution:

    def encode(self, strs: List[str]) -> str:
        # --- WHAT PROBLEM DOES ENCODE / DECODE SOLVE? ---
        #
        # The challenge: serialize a list of strings into ONE single string,
        # then be able to reconstruct the original list without ambiguity.
        #
        # Why is it tricky?
        # If you simply join words with a separator like "|":
        #   ["neet", "co|de"]  →  "neet|co|de"
        #   When decoding, is it ["neet", "co", "de"] or ["neet", "co|de"]?
        #                                                       ↑ AMBIGUOUS
        #
        # The solution: LENGTH-PREFIXED ENCODING
        # Before each string, store its length.
        #
        # Format of the encoded string:
        #
        #   "4,4,3,#neetcodelee"
        #    ↑─────↑ ↑ ↑───────
        #    lengths  # concatenated content
        #
        #   Where "#" acts as a sentinel between the "length index"
        #   and the "content block".
        #
        # Example:
        #   Input:        ["neet", "code", "lee"]
        #   Lengths:      [4, 4, 3]
        #   Header:       "4,4,3,#"
        #   Body:         "neetcodelee"
        #   Encoded:      "4,4,3,#neetcodelee"
        #
        # Now when decoding we know exactly how many characters to read
        # for each string → no ambiguity possible.

        if not strs:
            return ""

        # --- STEP 1: Collect the length of each string ---
        #
        # Iterate over the list and store len(word) for each string.
        # This forms the "header" we will use when decoding.
        #
        # ["neet", "code", "lee"]  →  string_lengths = [4, 4, 3]
        string_lengths = []
        for word in strs:
            string_lengths.append(len(word))

        # --- STEP 2: Build the header with the lengths ---
        #
        # Convert each length to a string and separate them with commas.
        # At the end of the header, append '#' as a sentinel/delimiter
        # that means "lengths are done, content starts here".
        #
        # string_lengths = [4, 4, 3]
        # parts          = ['4', ',', '4', ',', '3', ',', '#']
        #
        # We use a list (parts) instead of string concatenation
        # because in Python, string + string creates a new object each time.
        # Appending to a list and joining at the end is O(n) total.
        parts = []
        for length in string_lengths:
            parts.append(str(length))
            parts.append(',')
        parts.append('#')

        # --- STEP 3: Append the actual string content ---
        #
        # Simply add all strings one after another.
        # No separators needed because we already know the lengths.
        #
        # parts = ['4',',','4',',','3',',','#', 'neet','code','lee']
        parts.extend(strs)

        # --- STEP 4: Join everything into one string and return ---
        #
        # ''.join(parts) converts the list into a string with no separator.
        # Final output: "4,4,3,#neetcodelee"
        return ''.join(parts)

    def decode(self, encoded_str: str) -> List[str]:
        # --- HOW DOES DECODE WORK? ---
        #
        # We receive the encoded string and must reconstruct the list.
        #
        # Strategy in 2 phases:
        #   PHASE 1 — Read the header: extract the lengths
        #   PHASE 2 — Read the body:   slice substrings using those lengths
        #
        # Input:  "4,4,3,#neetcodelee"
        # Output: ["neet", "code", "lee"]

        if not encoded_str:
            return []

        string_lengths = []   # stores the lengths read from the header
        result         = []   # stores the reconstructed strings
        read_pointer   = 0    # pointer that walks through the encoded string

        # --- PHASE 1: Parse the header (comma-separated lengths) ---
        #
        # Advance read_pointer until we hit '#'.
        # For each number, use a second pointer (comma_pointer) to find the comma.
        #
        # Walk-through on "4,4,3,#neetcodelee":
        #
        #   Iteration 1:  read_pointer=0, comma_pointer moves to 1  →  s[0:1]="4"  →  lengths=[4]
        #   Iteration 2:  read_pointer=2, comma_pointer moves to 3  →  s[2:3]="4"  →  lengths=[4,4]
        #   Iteration 3:  read_pointer=4, comma_pointer moves to 5  →  s[4:5]="3"  →  lengths=[4,4,3]
        #   Next check:   read_pointer=6, s[6]='#'  →  exit while
        #
        # Why scan for the comma instead of using split(',')?
        # Because split would break everything at once, including '#' and the body.
        # With two pointers we stay in full control of our position.
        while encoded_str[read_pointer] != '#':
            comma_pointer = read_pointer
            while encoded_str[comma_pointer] != ',':
                comma_pointer += 1
            # encoded_str[read_pointer:comma_pointer] is the number without the comma
            string_lengths.append(int(encoded_str[read_pointer:comma_pointer]))
            read_pointer = comma_pointer + 1   # skip the comma

        # After the while, encoded_str[read_pointer] == '#'
        # Move read_pointer one position forward to point at the start of the body
        read_pointer += 1   # now points to 'n' in "neetcodelee"

        # --- PHASE 2: Extract strings using the stored lengths ---
        #
        # For each length, take exactly that many characters from read_pointer.
        # Then advance read_pointer by that length for the next string.
        #
        # Example with string_lengths=[4,4,3] and read_pointer at "neetcodelee":
        #
        #   length=4:  s[7:11]  = "neet"  →  read_pointer = 11
        #   length=4:  s[11:15] = "code"  →  read_pointer = 15
        #   length=3:  s[15:18] = "lee"   →  read_pointer = 18
        #
        # No ambiguity: the prefixed length guides every slice precisely.
        for length in string_lengths:
            result.append(encoded_str[read_pointer:read_pointer + length])
            read_pointer += length

        return result


# ---------------------------------------------------------------------------
# VISUAL SUMMARY
# ---------------------------------------------------------------------------
#
#  ENCODE:
#  ┌─────────────────────────────────────────────────────────────────┐
#  │  ["neet", "code", "lee"]                                        │
#  │      ↓         ↓       ↓                                        │
#  │   len=4     len=4   len=3                                       │
#  │      ↓                                                          │
#  │  header: "4,4,3,#"     body: "neetcodelee"                     │
#  │      ↓                                                          │
#  │  encoded: "4,4,3,#neetcodelee"                                  │
#  └─────────────────────────────────────────────────────────────────┘
#
#  DECODE:
#  ┌─────────────────────────────────────────────────────────────────┐
#  │  "4,4,3,#neetcodelee"                                           │
#  │   ↑─────↑                                                       │
#  │   scan until '#'  →  string_lengths = [4, 4, 3]                 │
#  │            ↑                                                     │
#  │            read_pointer starts here after '#'                   │
#  │                                                                  │
#  │   s[read_pointer : read_pointer+4] = "neet"  →  pointer += 4   │
#  │   s[read_pointer : read_pointer+4] = "code"  →  pointer += 4   │
#  │   s[read_pointer : read_pointer+3] = "lee"   →  pointer += 3   │
#  │                                                                  │
#  │  output: ["neet", "code", "lee"]  ✓                             │
#  └─────────────────────────────────────────────────────────────────┘
#
#  COMPLEXITY:
#   Encode  →  O(n·m)  where n = number of strings, m = average length
#   Decode  →  O(n·m)  same reason
#   Space   →  O(n·m)  for the output
# ---------------------------------------------------------------------------