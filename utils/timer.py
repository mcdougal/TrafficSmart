from constants import *

class Timer(object):
    def __init__(self):
        self.light_cycle = 0
        self.time_step = 0
        self.frame = 0
        self.beginning_of_light_cycle = True
        self.beginning_of_time_step = True

    def copy(self):
        copy = Timer()
        copy.light_cycle = self.light_cycle
        copy.time_step = self.time_step
        copy.frame = self.frame
        copy.beginning_of_light_cycle = self.beginning_of_light_cycle
        copy.beginning_of_time_step = self.beginning_of_time_step
        return copy

    @property
    def sub_cycle(self):
        return self.time_step % CYCLE_SIZE

    def increment_light_cycle(self):
        self.light_cycle += 1
        self.beginning_of_light_cycle = True

    def decrement_light_cycle(self):
        self.light_cycle -= 1

    def increment_time_step(self):
        self.time_step += 1
        self.beginning_of_time_step = True

    def decrement_time_step(self):
        self.time_step -= 1

    def increment_frame(self):
        self.frame += 1
        self.beginning_of_light_cycle = False
        self.beginning_of_time_step = False

    def decrement_frame(self):
        self.frame -= 1

T = Timer()
