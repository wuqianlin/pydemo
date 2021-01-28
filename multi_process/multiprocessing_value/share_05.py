import time
import asyncio
from collections import defaultdict
from multiprocessing import Process
from multiprocessing.managers import BaseManager


def defaultdict_construct():
    return defaultdict(list)


class AlarmConfigShare:
    alarm_config = defaultdict(defaultdict_construct)

    def value(self):
        return self.alarm_config

    def setitem(self, key1, key2, value):
        self.alarm_config[key1][key2].append(value)


class AlarmConfigManager(BaseManager):
    pass


AlarmConfigManager.register('AlarmConfigShare', AlarmConfigShare)


async def receive_data(_alarm_share):
    _alarm_share.setitem('key1', 'key2', 'fuck')
    print(_alarm_share.value())


def func01(_alarm_share):
    loop = asyncio.get_event_loop()
    loop.create_task(receive_data(_alarm_share))
    try:
        loop.run_forever()
    finally:
        loop.close()


def func02(_alarm_share):
    time.sleep(2)
    print('func02', _alarm_share.value())


if __name__ == '__main__':
    with AlarmConfigManager() as manager:
        alarm_share = manager.AlarmConfigShare()

        p1 = Process(target=func01, args=(alarm_share,))
        p1.start()

        p2 = Process(target=func02, args=(alarm_share,))
        p2.start()

        p1.join()
        p2.join()
