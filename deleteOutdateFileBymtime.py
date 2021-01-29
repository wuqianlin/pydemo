import os
import time
import logging
from pathlib import Path
logger = logging.getLogger(__name__)


def dele_outdate_file_bymtime(folder, keep_second):
    now = time.time()
    files = [os.path.join(folder, filename) for filename in os.listdir(folder)]
    logger.info(f'开始清理过期文件，文件保质期为：{keep_second} 秒。')

    for filename in files:
        if os.path.isfile(filename):
            if (now - os.stat(filename).st_mtime) > keep_second:
                os.remove(filename)
                logger.info(f'清理过期文件：{filename}')


if __name__ == '__main__':
    pwd = os.path.dirname(os.path.abspath(__file__))
    folder = Path(pwd, 'folder02')
    keep_second = 1800
    # dele_outdate_file_bymtime(folder, keep_second)
