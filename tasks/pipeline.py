#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math
import threading
from queue import Queue


def series_term(n: int, x: float) -> float:
    return 1.0 / ((2 * n - 1) * (x ** (2 * n - 1)))


def calculate_series(x: float, eps: float, out_queue: Queue) -> None:
    total_sum = 0.0
    n = 1

    while True:
        term = series_term(n, x)

        if abs(term) < eps:
            break

        total_sum += term
        n += 1

    out_queue.put(total_sum)


def calculate_control(x: float, eps: float, in_queue: Queue) -> None:
    series_sum = in_queue.get()

    control_value = 0.5 * math.log((x + 1) / (x - 1))
    diff = abs(series_sum - control_value)

    print("Результаты вычислений:")
    print(f"Сумма ряда S = {series_sum:.10f}")
    print(f"Контрольное значение y = {control_value:.10f}")
    print(f"|S - y| = {diff:.2e}")

    if diff < eps:
        print(f"Точность достигнута: |S - y| < ε = {eps}")
    else:
        print(f"Точность не достигнута: |S - y| ≥ ε = {eps}")


def run_pipeline(x: float, eps: float) -> None:
    print("=" * 50)
    print("Конвейерное вычисление суммы ряда")
    print(f"x = {x}, ε = {eps}")
    print("=" * 50)

    queue = Queue()

    t1 = threading.Thread(
        target=calculate_series,
        args=(x, eps, queue),
        name="SeriesThread",
    )

    t2 = threading.Thread(
        target=calculate_control,
        args=(x, eps, queue),
        name="ControlThread",
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()
