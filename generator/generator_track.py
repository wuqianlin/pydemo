def infinite_palindromes():
    num = 0
    while True:
        i = yield num
        print('yield return value: ', i)
        num += 1


pal_gen = infinite_palindromes()
for j in pal_gen:
    print('generator value: ', j)
    digits = len(str(j))
    pal_gen.send(10 ** digits)


