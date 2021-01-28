import multiprocessing


def func(_array):
    _array[2] = 9999  # 子进程改变数组，主进程跟着改变


if __name__ == "__main__":
    array = multiprocessing.Array("i", [1, 2, 3, 4, 5])  # 主进程与子进程共享这个数组
    print(array[:])

    p = multiprocessing.Process(target=func, args=(array,))
    p.start()
    p.join()

    print(array[:])