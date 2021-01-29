import os
import time

def report_device_info(max_count):
    print(os.getppid())
    count = 0
    while True:
        time.sleep(1000 / 1e6)
        count += 1
        if count > max_count:
            print(f"execute {max_count}")
            break


report_device_info(max_count=10**3)