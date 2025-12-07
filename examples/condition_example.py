from queue import Empty, Queue
from threading import Condition, Thread
from time import sleep

cv = Condition()
q = Queue()


def order_processor(name):
    while True:
        with cv:
            while q.empty():
                cv.wait()
            try:
                order = q.get_nowait()
                print(f"{name}: {order}")
                if order == "stop":
                    break
            except Empty:
                pass
        sleep(0.1)


if __name__ == "__main__":
    Thread(target=order_processor, args=("thread 1",)).start()
    Thread(target=order_processor, args=("thread 2",)).start()
    Thread(target=order_processor, args=("thread 3",)).start()

    for i in range(10):
        q.put(f"order {i}")

    for _ in range(3):
        q.put("stop")

    with cv:
        cv.notify_all()
