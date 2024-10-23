import threading


class ThreadPool:
    def __init__(self, num_threads):

        self.num_threads: int = num_threads
        self.tasks = []
        self.threads = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.stop = False

        for _ in range(num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self):

        while True:
            with self.condition:
                while not self.tasks:
                    self.condition.wait()

                task = self.tasks.pop(0)

            if task is None:
                break

            task()

    def enqueue(self, task):

        with self.condition:
            self.tasks.append(task)
            self.condition.notify()

    def dispose(self):

        with self.condition:

            self.stop = True
            for _ in range(self.num_threads):
                self.tasks.append(None)
            self.condition.notify_all()

        for thread in self.threads:
            thread.join()
