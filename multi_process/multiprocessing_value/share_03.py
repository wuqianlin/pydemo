"""
Value、Array是通过共享内存的方式共享数据
Manager是通过共享进程的方式共享数据。

进程之间共享数据(dict, list - Manager)：
"""


import multiprocessing


def func(_dict, _list):
    _dict["index1"] = "aaaaaa"  # 子进程改变dict,主进程跟着改变
    _dict["index2"] = "bbbbbb"
    _list.append(111)  # 子进程改变List,主进程跟着改变
    _list.append(222)
    _list.append(333)


def another_func(mydict, mylist):
    mydict["index3"] = "cccccc"  # 子进程改变dict,主进程跟着改变
    mydict["index4"] = "dddddd"
    mylist.append(444)  # 子进程改变List,主进程跟着改变
    mylist.append(555)
    mylist.append(666)


if __name__ == "__main__":
    with multiprocessing.Manager() as MG:  # 重命名
        _dict = multiprocessing.Manager().dict()  # 主进程与子进程共享这个字典
        _list = multiprocessing.Manager().list(range(5))  # 主进程与子进程共享这个List

        p = multiprocessing.Process(target=func, args=(_dict, _list))
        p.start()
        p.join()

        p = multiprocessing.Process(target=another_func, args=(_dict, _list))
        p.start()
        p.join()

        print(_list)
        print(_dict)
