from redis import Redis
from rq_scheduler import Scheduler
from datetime import timedelta, datetime
from scheduler.task import func
import rq

redis_connection = Redis(host='192.168.254.82', port=6380, db=2, password='zaq1<LP_')
scheduler = Scheduler(connection=redis_connection, interval=1)

scheduler.schedule(
    scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
    func=func,                     # Function to be queued
    interval=2,                   # Time before the function is called again, in seconds
    repeat=None,
    result_ttl=8
)