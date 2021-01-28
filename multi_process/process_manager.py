from multiprocessing import managers, Queue, Process


class SubscriberQueueMap:
    map = {}
    # def __init__(self):

    def add(self, name, q: Queue):
        self.map[name] = q

    def get(self, name):
        return self.map.get(name)

    def put(self, name):
        return self.map.get(name)


class MyManager(managers.BaseManager):
    pass


MyManager.register('SubscriberQueueMap', SubscriberQueueMap)


def task(queue_map):
    q3 = queue_map.get('q1')
    q3.put('123')


if __name__ == '__main__':
    # q1 = Queue(maxsize=1000)
    # q2 = Queue(maxsize=1000)
    # m = dict(q1=q1, q2=q2)
    with MyManager() as manager:
        m = manager.SubscriberQueueMap()
        q1 = Queue(maxsize=1000)
        m.add('q1', q1)

        p = Process(target=task, args=(m,))
        p.start()
        p.join()

        xx = q1.get()
        print(xx)
