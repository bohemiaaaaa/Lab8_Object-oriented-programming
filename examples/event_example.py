#!/usr/bin/env python3
# -*- coding: utf-8 -*


from threading import Event, Thread

event = Event()


def worker(name: str):
    event.wait()
    print(f"Worker: {name}")


if __name__ == "__main__":
    event.clear()

    workers = [Thread(target=worker, args=(f"wrk {i}",)) for i in range(5)]
    for w in workers:
        w.start()

    print("Main thread")
    event.set()
