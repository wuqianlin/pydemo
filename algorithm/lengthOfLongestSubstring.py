def lengthOfLongestSubstring(s: str) -> int:
    length = len(s)
    i = 0
    while True:
        for x in range(i + 1):
            sub_s = s[x:length-i+x]
            print(sub_s, x, i, length-i-x)
            if len(sub_s) == len(set(sub_s)):
                print('xx', sub_s)
                _max = len(sub_s)
                return _max
        i += 1


if '__main__' == __name__:
    s1 = "abcabcbb"
    s2 = "bbbbb"
    s3 = "pwwkew"
    s4 = "jhhthogonzpheevzetkvygpvbdhcaisjpbfwslmflbopgmqmfcjdkzbmckqeskpjluhditltvzkdlap"
    num = lengthOfLongestSubstring(s4)
    print(num)
