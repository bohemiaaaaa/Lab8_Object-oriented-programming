from threading import Thread, Event
from time import sleep, time

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