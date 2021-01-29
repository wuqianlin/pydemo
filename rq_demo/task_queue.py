from redis import Redis
from rq import Queue, Connection, Worker
from task import count_words_at_url
import time

q = Queue(connection=Redis(host='192.168.254.82', port=6380, db=2, password='zaq1<LP_'))
job = q.enqueue(count_words_at_url, 'https://www.baidu.com/')
print(job.result)   # => None

# Now, wait a while, until the worker is finished
time.sleep(4)
print(job.result)   # => 889
