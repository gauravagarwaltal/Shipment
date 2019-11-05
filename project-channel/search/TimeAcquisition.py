import time


class TimeAcquisition:
    def __init__(self):
        self.start = 0
        self.end = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print(self.end - self.start)


with TimeAcquisition() as time_consumed:
    time.sleep(1)
    with TimeAcquisition() as time_consumed_1:
        time.sleep(0.5)

print(time.asctime(time.localtime(1571203800)))
