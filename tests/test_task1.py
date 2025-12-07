import math
import threading
from queue import Queue

import pytest
import task1
from task1 import calculate_control_value, calculate_series, series_term


class TestSeriesTerm:
    def test_series_term_correct_calculation(self):
        result = series_term(1, 3.0)
        expected = 1.0 / 3.0
        assert result == pytest.approx(expected, rel=1e-10)

    def test_series_term_overflow_handling(self):
        result = series_term(1000, 1.5)
        assert result == 0.0


class TestCalculateSeries:
    def test_calculate_series_converges_to_required_precision(self):
        result_queue = Queue()
        stop_event = threading.Event()

        calculate_series(3.0, 1e-7, result_queue, stop_event)

        assert not result_queue.empty()
        series_sum = result_queue.get()
        assert series_sum > 0.0

    def test_calculate_series_with_immediate_stop(self):
        result_queue = Queue()
        stop_event = threading.Event()
        stop_event.set()

        calculate_series(3.0, 1e-7, result_queue, stop_event)


class TestCalculateControlValue:
    def test_calculate_control_value_correctness(self):
        data_queue = Queue()
        result_queue = Queue()
        stop_event = threading.Event()
        cv = threading.Condition()

        test_series_sum = 0.346573590
        data_queue.put(test_series_sum)

        calculate_control_value(3.0, data_queue, result_queue, stop_event, cv)

        assert not result_queue.empty()
        results = result_queue.get()

        expected_control = 0.5 * math.log((3 + 1) / (3 - 1))
        assert results["control_value"] == pytest.approx(expected_control, rel=1e-10)
        assert results["series_sum"] == test_series_sum


class TestIntegration:
    def test_full_pipeline_meets_requirements(self):
        x = 3.0
        epsilon = 1e-7

        series_queue = Queue()
        result_queue = Queue()
        stop_event = threading.Event()
        cv = threading.Condition()

        series_thread = threading.Thread(
            target=task1.calculate_series, args=(x, epsilon, series_queue, stop_event)
        )

        control_thread = threading.Thread(
            target=task1.calculate_control_value,
            args=(x, series_queue, result_queue, stop_event, cv),
        )

        series_thread.start()
        control_thread.start()

        import time

        time.sleep(0.1)

        with cv:
            cv.notify()

        series_thread.join(timeout=2)
        control_thread.join(timeout=2)

        assert not result_queue.empty()
        results = result_queue.get()

        assert "series_sum" in results
        assert "control_value" in results
        assert "difference" in results

        assert results["difference"] < epsilon
