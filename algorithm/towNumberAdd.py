# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    re = ListNode(0)
    r = re
    carry = 0
    while l1 or l2:
        x = l1.val if l1 else 0
        y = l2.val if l2 else 0
        s = carry + x + y
        carry = s // 10
        r.next = ListNode(s % 10)
        r = r.next
        if l1 is not None: l1 = l1.next
        if l2 is not None: l2 = l2.next
    if carry > 0:
        r.next = ListNode(1)
    return re.next

# 输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
# 输出：7 -> 0 -> 8
# 原因：342 + 465 = 807


ln1 = ListNode(2)
ln1.next = ListNode(4)
ln1.next.next = ListNode(3)

ln2 = ListNode(5)
ln2.next = ListNode(6)
ln2.next.next = ListNode(4)

a = addTwoNumbers(ln1, ln2)
while a.next is not None:
    print('r', a.val)
    a = a.next

print('r', a.val)

