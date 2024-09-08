"""Async entry point for the application."""

from aiohttp import ClientSession
from asyncio import get_event_loop
from asyncio.queues import Queue
from asyncio.tasks import Task
import sys
import json
import pprint

"""Create class RequestHandler that will handle the requests
It'll have a method that will handle the requests.
It'll have a session that will be used to make the requests.
"""


class RequestHandler:
    def __init__(self, url):
        self.url = url
        self.session = ClientSession()


async def get(url):
    """Make a request to the API and return the response."""
    async with ClientSession() as session:
        async with session.get(url) as resp:
            print("Status: {}".format(resp.status))
            print("Content-Type:", resp.headers["Content-Type"])
            resp_json = await resp.json()
            return resp_json


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    loop = get_event_loop()
    # URL to get request IP from
    URL = "http://httpbin.org/ip"

    """Run Asyncio Server"""

    asyncio_task = loop.create_task(get(URL))
    loop.run_until_complete(asyncio_task)
    result = asyncio_task.result()
    pprint.pprint(result, indent=4)
    loop.close()
    if loop.is_closed():
        sys.exit(0)
