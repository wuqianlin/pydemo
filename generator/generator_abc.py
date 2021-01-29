import sys


def gen():
    x = yield 1
    print('x:', x)
    y = yield 2
    print('y:', y)


g = gen()
ret = g.send(None)
print('第一次 yield 的返回值：', ret)

ret = g.send('测试')
print('第二次 yield 的返回值：', ret)

try:
    ret = g.send(999)
except StopIteration:
    exc_type, exc_value, exc_tb = sys.exc_info()
    print('异常类型：%s' % exc_type)
    print('异常值：%s' % exc_value)
    print('异常追踪信息：%s' % exc_tb)
