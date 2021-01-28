import json
import functools
import logging
import os
import time
import concurrent.futures
from collections import defaultdict
import multiprocessing
from typing import Dict
import zmq


ZMQ_PushPull_To_AlarmJudge = 'tcp://127.0.0.1:5557'

def generator():
    _context = zmq.Context()
    receiver = _context.socket(zmq.PULL)
    receiver.connect(ZMQ_PushPull_To_AlarmJudge)

    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    while True:
        evts = poller.poll(100)
        if evts:
            yield receiver.recv_json()
        else:
            yield None



def judge_pod(args):
    if args is None:
        print('get None')
    args = json.loads(args)
    print(args['header']['msg_id'])


def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(judge_pod, generator(), chunksize=10)


main()