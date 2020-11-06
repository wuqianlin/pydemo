"""
multiprocessing.Queue

```
import multiprocessing

def worker(name, que):
    que.put(f"{name} is done")

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=3)
    q = multiprocessing.Queue()
    workers = pool.apply(worker, (33, q))
```
will raise Exception:
RuntimeError: Queue objects should only be shared between processes through inheritance
why?
read this: https://stackoverflow.com/questions/9908781/sharing-a-result-queue-among-several-processes
"""
import multiprocessing


def worker(name, que):
    que.put(f"{name} is done")


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=3)
    m = multiprocessing.Manager()
    q = m.Queue()
    workers = pool.apply(worker, (33, q))
    print(q.get())
