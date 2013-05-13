from constants import *
from timer import T

class Logger(object):
    def __init__(self, breakpoint=None, verbosity=0):
        self.breakpoint = breakpoint
        self.verbosity = verbosity
        self.paused = False

    def log(self, msg, verbosity=1):
        if not self.paused and verbosity <= self.verbosity:
            if self.verbosity > 0:
                msg = ("%s:" % T.frame).ljust(6) + msg
            if self.breakpoint and T.frame >= self.breakpoint:
                raw_input(msg)
            else:
                print msg

    def pause(self):
        self.paused = True

    def play(self):
        self.paused = False

L = Logger()
