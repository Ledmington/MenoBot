from threading import Thread


class Worker:
    def __init__(self, task):
        if not callable(task):
            raise TypeError
        self.task = task
        self.th = None
        self.shutdown = False

    def is_shutdown(self) -> bool:
        return self.shutdown

    def is_alive(self) -> bool:
        return self.th is not None

    def start(self):
        if self.th is not None:
            raise ValueError
        self.th = Thread(target=self._loop)
        self.th.start()

    def _loop(self):
        while self.shutdown is False:
            self.task()

    def die(self):
        self.shutdown = True

    def join(self):
        self.die()
        self.th.join()
        self.th = None
