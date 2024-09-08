import asyncio
from asyncio import Queue, AbstractEventLoop
import time
import random
import colorama
from datetime import datetime, timedelta


### Create producer that takes an integer
# and produces squares of each integer till n
# puts them all onto the queue
async def producer(n: int, queue: Queue, name):
    for i in range(1, n + 1):
        # takes between 0.5 and 1.5 seconds to complete this task
        work_time = random.random() + 0.5
        dt_start = datetime.now()
        print(
            colorama.Fore.YELLOW
            + " -- Generating item {} in Producer {} at {}".format(i, name, dt_start),
            flush=True,
        )
        # actual work
        await asyncio.sleep(work_time)
        sq_i = i**2
        # put work on queue
        work = (name, sq_i, dt_start)
        await queue.put(work)


### Create consumer that takes an integer n
# and consumes n items from the queue
# and prints them out
async def consumer(n: int, queue: Queue, name):
    processed = 0
    while processed < n:
        # If no item in queue, wait for one. else asynhronously get item
        item = await queue.get()
        processed += 1

        producer_name, sq_i, start = item
        now = datetime.now()
        delay = now - start

        # do some computation with the item
        print(
            colorama.Fore.GREEN
            + " -- consumed item {} in Consumer{} by Producer{}  at {} after {} i.e {:.4f} seconds".format(
                sq_i, name, producer_name, now, delay, delay.total_seconds()
            ),
            flush=True,
        )
        await asyncio.sleep(0.5)


def main():
    t0 = time.time()
    print(colorama.Fore.WHITE + "App started.", flush=True)

    # create asyncio Queue
    data = Queue(maxsize=2)

    # Run these with asyncio.gather()
    tasks = [
        producer(10, data, "1"),
        producer(10, data, "2"),
        consumer(5, data, "1"),
        consumer(5, data, "2"),
        consumer(5, data, "3"),
        consumer(5, data, "4"),
        # consumer(1,data,"2"),
        # consumer(6,data,"3")
        # consumer(6,data,"2") ,
        # consumer(6,data,"3"),
    ]

    loop: AbstractEventLoop = asyncio.get_event_loop()
    # Run all the asyncio tasks
    loop.run_until_complete(asyncio.gather(*tasks))

    dt = time.time() - t0
    print(
        colorama.Fore.WHITE + "App exiting, total time: {:.2f} sec.".format(dt),
        flush=True,
    )


if __name__ == "__main__":
    main()
