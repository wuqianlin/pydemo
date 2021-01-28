import multiprocessing

def func1(a,_arr):
    a.value=3.14
    for i in range(len(arr)):
        arr[i]=-_arr[i]

if __name__ == '__main__':
    num=multiprocessing.Value('d',1.0)
    arr=multiprocessing.Array('i',range(10))
    p=multiprocessing.Process(target=func1, args=(num,arr))
    p.start()
    p.join()
    print(num.value)
    print(arr[:])