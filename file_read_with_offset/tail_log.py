from pathlib import Path

log_file_path = Path(__file__).absolute().parent / 'bigfile.log'


class FileInfo(object):
    def __init__(self, path, seek_to_end=True):
        """
        默认值为 0。给offset参数一个定义，表示要从哪个位置开始偏移；
        0代表从文件开头开始算起，1代表从当前位置开始算起，2代表从文件末尾算起。
        """
        self.path = path
        self.fd = open(path, 'r')
        if seek_to_end:
            self.fd.seek(0, 2)  # 2==os.SEEK_END, which isn't available on py2.4
        self.line_buffer = None

    def close(self):
        self.fd.close()


def read_file():
    with open(log_file_path, "rb") as f:
        f.seek(-1000, 2)
        for line in f:
            yield line


def main():
    max_line = 10
    i = 1
    for line in read_file():
        line = line.decode('utf-8')
        print(line, end="")
        i += 1
        if i >= max_line:
            break


if __name__ == "__main__":
    main()
