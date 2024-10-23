import threading


class ThreadPool:
    def __init__(self, num_threads):

        """
        A ThreadPool class that manages a pool of worker threads to execute tasks.

        Attributes:
            num_threads (int): The number of threads in the pool.
            tasks (list): A list of tasks to be executed.
            threads (list): A list of thread objects.
            lock (threading.Lock): A lock to ensure thread-safe operations.
            condition (threading.Condition): A condition variable to manage task queue.
            stop (bool): A flag to indicate if the thread pool should stop.
        """

        self.num_threads: int = num_threads
        self.tasks = []
        self.threads = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.stop = False

        for _ in range(num_threads):

            """
            Initializes the ThreadPool with a specified number of threads.

            Args:
                num_threads (int): The number of threads to create in the pool.
            """
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self):

        """
        The worker function that each thread runs. It continuously checks for tasks
        and executes them.
        """

        while True:
            with self.condition:
                while not self.tasks:
                    self.condition.wait()

                task = self.tasks.pop(0)

            if task is None:
                break

            task()

    def enqueue(self, task):

        """
        Adds a task to the task queue.

        Args:
            task (callable): The task to be executed.
        """

        with self.condition:
            self.tasks.append(task)
            self.condition.notify()

    def dispose(self):

        """
        Stops the thread pool and waits for all threads to finish.
        """

        with self.condition:

            self.stop = True
            for _ in range(self.num_threads):
                self.tasks.append(None)
            self.condition.notify_all()

        for thread in self.threads:
            thread.join()
