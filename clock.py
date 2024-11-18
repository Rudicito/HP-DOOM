from hpprime import eval
class Clock:
    def __init__(self):
        self.dt = 100
        self.old_time = self.get_time()
        self.time = None

    def tick(self):
        self.time = self.get_time()
        self.dt = self.time - self.old_time
        self.old_time = self.time
        return self.dt

    def get_time(self):
        return int(eval("ticks"))