class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        closeToOpen = {")": "(", "]": "[", "}": "{"}
        opens = set(closeToOpen.values())
        closes = set(closeToOpen.keys())

        for c in s:
            if c in opens:
                stack.append(c)

            elif c in closes:
                if stack and stack[-1] == closeToOpen[c]:
                    stack.pop()
                else:
                    return False

            else:
                # ignore other characters
                continue

        return not stack
