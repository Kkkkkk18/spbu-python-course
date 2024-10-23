import threading
import time
import pytest
from project.thread_pool.thread_pool import ThreadPool


def sample_task(x):

    time.sleep(1)
    print(f"The task {x} is completed")


def test_enqueue():
    pool = ThreadPool(3)

    tasks_executed = []

    def ex_task(x):
        tasks_executed.append(x)

    for i in range(4):
        pool.enqueue(lambda i=i: ex_task(i))

    time.sleep(1)
    pool.dispose()

    assert (
        len(tasks_executed) == 4
    ), f"Expected 5 tasks completed, got {len(tasks_executed)}"


def test_dispose():

    pool = ThreadPool(5)

    pool.enqueue(sample_task)
    pool.dispose()
    pool.enqueue(sample_task)

    for thread in pool.threads:
        assert not thread.is_alive(), "!not all threads are completed!"


def test_thread_pool():

    pool = ThreadPool(6)

    assert len(pool.threads) == 6, f"Expected 5 threads, found {len(pool.threads)}"

    pool.dispose()


def test_active_thread():

    active_threads = threading.active_count()
    pool = ThreadPool(7)

    time.sleep(0.5)

    new_active_threads = threading.active_count()
    res_active_threads = new_active_threads - active_threads
    pool.dispose()

    assert (
        res_active_threads == 7
    ), f"Expected 7 active threads, found {res_active_threads}"
