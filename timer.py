class Timer:

    def __init__(self, duration: int) -> None:
        self.duration = duration
        self.active = False

    def start(self):
        self.active = True
        