from constants import *
from utils.timer import T
import random

class Agent(object):
    def __init__(self):
        self.fails = 0

    def change_lights(self, city):
        if T.light_cycle != 0 and not city.cars_moved() and self.fails > 3:
            return self.random(city)

        lights_to_change = []

        for node in city.nodes_list:
            if T.light_cycle != 0 and not city.cars_moved():
                lights_to_change.append(node)
                self.fails += 1
                continue

            self.fails = 0

            num_cars_north = len(node.cars[NORTH])
            num_cars_south = len(node.cars[SOUTH])
            num_cars_east = len(node.cars[EAST])
            num_cars_west = len(node.cars[WEST])

            num_cars_vertical = num_cars_north + num_cars_south
            num_cars_horizontal = num_cars_east + num_cars_west
            
            if num_cars_vertical + num_cars_horizontal == 0:
                continue

            if num_cars_vertical > num_cars_horizontal:
                if node.green == HORIZONTAL:
                    lights_to_change.append(node)

            if num_cars_horizontal > num_cars_vertical:
                if node.green == VERTICAL:
                    lights_to_change.append(node)

        return lights_to_change

    def random(self, city):
        lights_to_change = []
        for node in city.nodes_list:
            if random.randint(0,1):
                lights_to_change.append(node)

        return lights_to_change
