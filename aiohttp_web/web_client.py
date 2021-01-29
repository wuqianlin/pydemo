import asyncio
from aiohttp import ClientSession


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def run(r):
    url = "http://localhost:8080/{}"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url.format(i), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print(responses)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(12))
