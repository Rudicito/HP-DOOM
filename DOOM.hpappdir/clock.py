from hpprime import eval
class Clock:
    def __init__(self):
        self.dt = 100
        self.old_time = self.get_time()
        # time is in ms
        self.time = None

    def tick(self):
        self.time = self.get_time()
        self.dt = self.time - self.old_time
        self.old_time = self.time
        return self.dt

    def get_time(self):
        return int(eval("ticks"))
    
    def cycles(self, interval, number):
        if number < 0:
            raise ValueError("Number cannot be negative")
        if not isinstance(number, int):
            raise ValueError("Number must be an integer")
        
        a = int(self.time // interval)
        return a % number