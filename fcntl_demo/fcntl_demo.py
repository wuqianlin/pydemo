"""
文件锁 python 进程间锁 fcntl

http://blog.csdn.net/jianhong1990/article/details/26370519
http://yunjianfei.iteye.com/blog/2061756
http://zhou123.blog.51cto.com/4355617/1650185
https://blog.jamespan.me/posts/deadlock-with-python-fcntl-flock

python的文件锁目前使用的是fcntl这个库，它实际上为 Unix上的ioctl，flock和fcntl 函数提供了一个接口。
https://www.cnblogs.com/my_life/articles/7602981.html
"""

import os
import time
import fcntl


FILE = "../counter.txt"

if not os.path.exists(FILE):
    # create the counter file if it doesn't exist
    file = open(FILE, "w")
    file.write("0")
    file.close()

for i in range(20):
    file = open(FILE, "r+")  # 由于flock生成的是劝告锁，不能阻止进程对文件的操作，所以这里可以正常打开文件
    fcntl.flock(file.fileno(), fcntl.LOCK_EX)  # 为了避免同时操作文件，需要程序自己来检查该文件是否已经被加锁。这里如果检查到加锁了，进程会被阻塞
    print('acquire lock')
    counter = int(file.readline()) + 1
    file.seek(0)
    file.write(str(counter))
    print(os.getpid(), "=>", counter)
    time.sleep(10)
    file.close()  # unlocks the file
    print('release lock')
    time.sleep(3)

"""
分别启动2个进程来同时运行这个脚本，我们可以很明显的看到2者互相之间交替阻塞。同一时刻只有一个进程能够对counter.txt文件进行操作。
"""