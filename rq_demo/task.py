import requests
import asyncio
import time

async def count_words_at_url(url):
    """Just an example function that's called async."""
    # resp = requests.get(url)
    await asyncio.sleep(1)
    return 123
