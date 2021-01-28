import multiprocessing


def func(_dict, _list):
    _dict["index1"] = "aaaaaa"  # 子进程改变dict,主进程跟着改变
    _dict["index2"] = "bbbbbb"
    _list.append(11)  # 子进程改变List,主进程跟着改变
    _list.append(22)
    _list.append(33)


if __name__ == "__main__":
    with multiprocessing.Manager() as MG:  # 重命名
        share_dict = multiprocessing.Manager().dict()  # 主进程与子进程共享这个字典
        share_list = multiprocessing.Manager().list(range(5))  # 主进程与子进程共享这个List

        p = multiprocessing.Process(target=func, args=(share_dict, share_list))
        p.start()
        p.join()

        print(share_list)
        print(share_dict)