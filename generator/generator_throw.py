def gen():
    try:
        yield 1
    except GeneratorExit:
        print('捕获到 GeneratorExit')
        raise


g1 = gen()
next(g1)
g1.close()
"""
捕获到 GeneratorExit
"""

# 没有激活生成器，就不会触发 GeneratorExit 异常
print()
g2 = gen()
g2.close()
print('脚本运行完毕')



