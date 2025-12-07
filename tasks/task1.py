#!/usr/bin/env python3
# -*- coding: utf-8 -*


import math
import threading
from queue import Queue
from time import sleep


def series_term(n: int, x: float) -> float:
    try:
        denominator = (2 * n - 1) * (x ** (2 * n - 1))
        return 1.0 / denominator
    except OverflowError:
        return 0.0


def calculate_series(
    x: float, epsilon: float, result_queue: Queue, stop_event: threading.Event, cv=None
) -> None:
    total_sum = 0.0
    n = 1

    while not stop_event.is_set():
        term = series_term(n, x)

        if term == 0.0 or abs(term) < epsilon:
            result_queue.put(total_sum)

            if cv is not None:
                with cv:
                    cv.notify()

            stop_event.set()
            break

        total_sum += term
        n += 1
        sleep(0.001)

    if result_queue.empty():
        result_queue.put(total_sum)
        if cv is not None:
            with cv:
                cv.notify()


def calculate_control_value(
    x: float,
    data_queue: Queue,
    result_queue: Queue,
    stop_event: threading.Event,
    cv: threading.Condition,
) -> None:

    with cv:
        while data_queue.empty() and not stop_event.is_set():
            cv.wait(timeout=0.1)

    if not data_queue.empty():
        series_sum = data_queue.get()

        if x > 1:
            y = 0.5 * math.log((x + 1) / (x - 1))
        else:
            y = float("nan")

        result_queue.put(
            {
                "series_sum": series_sum,
                "control_value": y,
                "difference": abs(series_sum - y),
            }
        )
        stop_event.set()


if __name__ == "__main__":
    x = 3.0
    epsilon = 1e-7

    print("=" * 50)
    print(f"Вычисление суммы ряда для x = {x}")
    print(f"Точность ε = {epsilon}")
    print("-" * 50)

    series_queue = Queue()
    result_queue = Queue()

    stop_event = threading.Event()
    cv = threading.Condition()

    series_thread = threading.Thread(
        target=calculate_series,
        args=(x, epsilon, series_queue, stop_event, cv),
        name="SeriesCalculator",
    )

    control_thread = threading.Thread(
        target=calculate_control_value,
        args=(x, series_queue, result_queue, stop_event, cv),
        name="ControlCalculator",
    )

    series_thread.start()
    control_thread.start()
    series_thread.join(timeout=5)
    control_thread.join(timeout=5)

    if not result_queue.empty():
        results = result_queue.get()

        print("Результаты вычислений:")
        print(f"Сумма ряда S = {results['series_sum']:.10f}")
        print(f"Контрольное значение y = {results['control_value']:.10f}")
        print(f"Разница |S - y| = {results['difference']:.2e}")

        if results["difference"] < epsilon:
            print(f"Точность достигнута: |S - y| < ε = {epsilon}")
        else:
            print(f"Точность не достигнута: |S - y| ≥ ε = {epsilon}")
    else:
        print("Ошибка: результаты не получены")

    print("=" * 50)
