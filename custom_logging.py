# -*- coding:utf-8 -*-
"""
摘抄于：https://www.cnblogs.com/dasheng-maritime/p/11715746.html
logging.Formatter的format方法，首先会按照格式化串格式化message，
然后如果出现异常，是直接再message后面加上异常；此时格式已经不是指定的格式，因此这里需要修自定义。
"""
import json
import logging
import os
import traceback


BASE_DIR = os.path.abspath(os.getcwd())
LOG_DIR = os.path.join(BASE_DIR,  "logs")

host_ip = "localhost"

JSON_LOGGING_FORMAT = json.dumps({
    "ip": "%(ip)s",
    "app": "%(app)s",
    "level": "%(levelname)s",
    "trace": "%(stack_msg)s",
    "filepath": "%(pathname)s",
    "line_number": "%(lineno)s",
    "time": "%(asctime)s",
    "message": "%(message)s",
    "stack_trace": "%(exc_text)s"
})


class JsonLoggingFilter(logging.Filter):
    def __init__(self, name, ip, app):
        logging.Filter.__init__(self, name=name)
        self.ip = ip
        self.app = app

    def filter(self, record):
        record.ip = self.ip
        record.app = self.app
        # 为record 添加异常堆栈信息字段; 当有多个handler 的时候，这里会判断多次
        if hasattr(record, "stack_msg") and hasattr(record, "stack_trace"):
            return True

        if record.exc_info:
            ex_type, ex_val, ex_stack = record.exc_info
            stack_list = []
            for stack in traceback.extract_tb(ex_stack):
                stack_list.append("%s" % stack)

            record.stack_msg = ex_val
            record.stack_trace = "#".join(stack_list)
        else:
            record.stack_msg, record.stack_trace = "", ""

        return True


class JsonFormatter(logging.Formatter):
    def __init__(self, fmt=None):
        logging.Formatter.__init__(self, fmt=fmt)

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info).replace("\n", " ").replace("\"", "'")

        s = self.formatMessage(record)
        return s


class JsonLogger(logging.Logger):
    logger = None
    level = None
    mode = None

    def __init__(self, app_name, level=logging.DEBUG, console_level=logging.INFO, mode="w"):
        self.name = app_name
        self.app_name = app_name

        logging.Logger.__init__(self, name=app_name)

        self.logger = logging.Logger(name=app_name)
        self.logger.setLevel(level)

        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        log_file_path = os.path.join(LOG_DIR, "%s.json" % app_name)
        json_logging_filter = JsonLoggingFilter(app_name, ip=host_ip, app=app_name)
        json_formatter = JsonFormatter(JSON_LOGGING_FORMAT)

        # 文件日志
        file_handle = logging.FileHandler(log_file_path, mode=mode)
        file_handle.setLevel(level)
        file_handle.setFormatter(json_formatter)
        file_handle.addFilter(json_logging_filter)
        # 控制台日志
        console_handle = logging.StreamHandler()
        console_handle.setLevel(console_level)
        console_handle.setFormatter(json_formatter)
        console_handle.addFilter(json_logging_filter)

        self.logger.addHandler(file_handle)
        self.logger.addHandler(console_handle)

    def getLogger(self):
        return self.logger

    def setLevel(self, level):
        self.logger.level = level


if __name__ == '__main__':
    my_logger = JsonLogger("python-common").getLogger()
    my_logger.info("info  level log")
    try:
        open('/path/to/does/not/exist', 'rb')
    except FileNotFoundError as e:
        my_logger.exception("file exception", exc_info=e)
