import time


class AlarmClock:
    def __init__(self, duration:float, start:bool=False):
        """
        This class is a timer, which does not require the program to pause to run.
        :param duration: The amount of time the timer will run for
        :param start: If the timer should start when the class is instantiated
        """
        self.duration = duration
        self.start_time = None
        if start:
            self.start()

    def start(self):
        """
        Starts the clock 
        """
        self.start_time = time.time()

    @property
    def time(self):
        """
        Returns the amount of time left in the countdown
        """
        return time.time() - self.start_time

    @property
    def finished(self):
        """
        Returns if the timer has finished
        """
        return time.time() - self.start_time >= self.duration

    def restart(self):
        """
        Restarts the clock
        (This is a wrapper for the above "start" method)
        """
        self.start()

    def stop(self):
        """
        Stops the clock
        """
        self.start_time = None

    @property
    def running(self):
        """
        Returns if the clock is still running
        """
        return self.start_time is not None
