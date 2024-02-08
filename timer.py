# timer that counts down 3 sec (lol, it's only for smooth movement of performer)

class Timer():
    def __init__(self):
        self.time = None

    def wait_3(self):
        from time import time
        self.time = time()
        while True:
            t = time()
            if t - self.time >= 1:
                self.time = None
                break


