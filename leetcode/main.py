def lengthOfLongestSubstring(s: str) -> int:
    length = len(s)
    arr = []
    for i in range(length):
        for j in range(i + 1, length + 1):
            sub = s[i:j]
            if list(set(sub)) == list(sub):
                print(sub)
                arr.append(len(set(sub)))
    return max(arr)

a = lengthOfLongestSubstring('pwwkew')
print(a)
