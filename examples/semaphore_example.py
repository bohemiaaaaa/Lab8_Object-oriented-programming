#!/usr/bin/env python3
# -*- coding: utf-8 -*


from threading import BoundedSemaphore, Thread
from time import sleep, time

ticket_office = BoundedSemaphore(value=3)


def ticket_buyer(number):
    start_service = time()
    with ticket_office:
        sleep(1)
        print(f"client {number}, service time: {time() - start_service}")


if __name__ == "__main__":
    buyers = [Thread(target=ticket_buyer, args=(i,)) for i in range(5)]

    for b in buyers:
        b.start()
