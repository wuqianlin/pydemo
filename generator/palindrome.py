
def is_palindrome(num):
    # Skip single-digit inputs
    if num // 10 == 0:
        return False
    temp = num
    reversed_num = 0

    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10

    if num == reversed_num:
        return True
    else:
        return False


def infinite_palindromes():
    num = 0
    while True:
        if is_palindrome(num):
            i = (yield num)
            print('yield return value: ',i)
            if i is not None:
                num = i
        num += 1


pal_gen = infinite_palindromes()
for x in pal_gen:
    print('generator value: ', x)
    digits = len(str(x))
    pal_gen.send(10 ** (digits))

