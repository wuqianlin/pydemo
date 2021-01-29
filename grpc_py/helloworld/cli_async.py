#!/usr/bin/env python
import asyncio
from aitertools import AsyncIterWrapper
from aiogrpc import insecure_channel
from square_pb2_grpc import SquareServiceStub
from square_pb2 import Message

url = "localhost:5000"

async def query():
    async with insecure_channel(url) as conn:
        client = SquareServiceStub(channel=conn)
        async for response in client.streamrangeSquare(AsyncIterWrapper(Message(message=i) for i in range(12))):
            print(response.message)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(query())


if __name__ == "__main__":
    main()