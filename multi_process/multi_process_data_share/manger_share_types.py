from multiprocessing import Process, Manager


def func1(share_list, share_value, share_dict, lock):
    with lock:
        share_value.value += 1
        share_dict[1] = '1'
        share_dict[2] = '2'
        for i in range(len(share_list)):
            share_list[i] += 1


if __name__ == '__main__':
    manager = Manager()
    _list = manager.list([1, 2, 3, 4, 5])
    _dict = manager.dict()
    _array = manager.Array('i', range(10))
    _value = manager.Value('i', 1)
    _lock = manager.Lock()

    proc = [ Process(target=func1, args=(_list, _value, _dict, _lock)) for i in range(20) ]
    for p in proc:
        p.start()
    for p in proc:
        p.join()
    print(_list)
    print(_dict)
    print(_array)
    print(_value)
    print(_lock)
