#!/usr/bin/env python
import grpc
from square_pb2_grpc import SquareServiceStub
from square_pb2 import Message

url = "localhost:5000"
channel = grpc.insecure_channel(url)
client = SquareServiceStub(channel=channel)
for result in client.streamrangeSquare(Message(message=i) for i in range(12)):
    print(result)