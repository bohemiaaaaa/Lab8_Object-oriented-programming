#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math
from queue import Queue

import pytest
from pipeline import calculate_series, series_term


def test_series_term_basic() -> None:
    x: float = 2.0
    n: int = 1
    expected: float = 1 / (1 * 2.0)
    assert series_term(n, x) == expected


@pytest.mark.parametrize(
    "n, x, expected",
    [
        (1, 2.0, 1 / (1 * 2.0)),
        (2, 2.0, 1 / (3 * 8.0)),
        (3, 3.0, 1 / (5 * 243.0)),
    ],
)
def test_series_term_parametrized(n: int, x: float, expected: float) -> None:
    assert series_term(n, x) == expected


def test_calculate_series_puts_value_in_queue() -> None:
    q: Queue[float] = Queue()
    x: float = 2.0
    eps: float = 1e-6
    calculate_series(x, eps, q)
    assert not q.empty()
    value: float = q.get()
    assert value > 0


def test_calculate_series_accuracy() -> None:
    q: Queue[float] = Queue()
    x: float = 2.0
    eps: float = 1e-6
    calculate_series(x, eps, q)
    series_sum: float = q.get()
    control_value: float = 0.5 * math.log((x + 1) / (x - 1))
    assert abs(series_sum - control_value) < 1e-5


def test_series_with_large_x() -> None:
    q: Queue[float] = Queue()
    x: float = 10.0
    eps: float = 1e-6
    calculate_series(x, eps, q)
    series_sum: float = q.get()
    control_value: float = 0.5 * math.log((x + 1) / (x - 1))
    assert abs(series_sum - control_value) < eps
