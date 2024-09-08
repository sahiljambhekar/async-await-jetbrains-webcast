import asyncio
import datetime
from asyncio import AbstractEventLoop
from re import S

import colorama
import random
import time


def main():
    # Create the asyncio loop
    loop: AbstractEventLoop = asyncio.get_event_loop()

    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)

    data = asyncio.Queue()  # maybe a better data structure?

    # Run these with asyncio.gather()

    task = asyncio.gather(
        generate_data(10, data, "Producer1"),
        generate_data(10, data, "Producer2"),
        process_data(5, data, "Consumer1"),
        process_data(5, data, "Consumer2"),
        process_data(5, data, "Consumer3"),
        process_data(5, data, "Consumer4"),
    )

    loop.run_until_complete(task)

    dt = datetime.datetime.now() - t0
    print(
        colorama.Fore.WHITE
        + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()),
        flush=True,
    )


### producer
async def generate_data(num: int, data: asyncio.Queue, name: str):
    for idx in range(1, num + 1):
        item = idx * idx
        # Use queue
        work = (item, datetime.datetime.now())
        # data.append(work)
        await data.put(work)

        print(
            colorama.Fore.YELLOW + " -- generated item {} in {}".format(idx, name),
            flush=True,
        )
        # Sleep better
        # time.sleep(random.random() + .5)
        await asyncio.sleep(random.random() + 0.5)


### con
async def process_data(num: int, data: asyncio.Queue, name: str):
    processed = 0
    while processed < num:
        # Use queue
        # item = data.pop(0)
        # if not item:
        #     time.sleep(.01)
        #     continue
        item = await data.get()
        # item is a tuple

        processed += 1
        value = item[0]
        t = item[1]
        delay = datetime.datetime.now() - t

        print(
            colorama.Fore.CYAN
            + " +++ Processed value {} in {} after {:,.2f} sec.".format(
                value, name, delay.total_seconds()
            ),
            flush=True,
        )
        # Sleep better
        # time.sleep(.5)
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    main()
