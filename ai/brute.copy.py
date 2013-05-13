from collections import defaultdict
from constants import *
from copy import deepcopy
from itertools import product
from utils.logger import L
from utils.timer import T
from utils.visualizer import V

def heuristic(city):
    return city.num_cars() - city.num_full_streets()

def check_sequence(city, light_sequence):
    city_copy = city.copy()

    for light_combo in light_sequence:
        for i, node in enumerate(city_copy.nodes_list):
            if light_combo[i]:
                city_copy.change_light(node)
        city_copy.cycle()

        if not city_copy.has_cars():
            break

    return heuristic(city_copy)

class Agent(object):
    def __init__(self):
        self.sequence = []

    def change_lights(self, city):
        if not hasattr(self, "light_sequences"):
            light_combos = product([True,False], repeat=len(city.nodes_list))
            self.light_sequences = [x for x in product(light_combos, repeat=1)]

        if self.sequence:
            return sequence.pop()

        lights_to_change = self.brute(city)
        if lights_to_change is None:
            lights_to_change = self.simple(city)

        return lights_to_change

    def brute(self, city):
        results = defaultdict(list)

        for light_sequence in self.light_sequences:
            L.pause()
            V.pause()
            score = check_sequence(city, light_sequence)
            L.play()
            V.play()

            L.log("      %s" % score, 4)
            results[score].append(light_sequence)

        best_result = min(results.keys())
        best_sequences = results[best_result]
        if len(best_sequences) > 1:
            L.log("      falling back to simple", 3)
            return None

        best_sequence = best_sequences[0]
        L.log("      using sequence %s" % str(id(best_sequence))[-3:], 3)

        for combo in reversed(best_sequence):
            lights_to_change = []
            for i, node in enumerate(city.nodes_list):
                if combo[i]:
                    lights_to_change.append(node)
            self.sequence.append(lights_to_change)

        return self.sequence.pop()

    def simple(self, city):
        lights_to_change = []

        for node in city.nodes_list:
            if T.light_cycle != 0 and not city.cars_moved():
                lights_to_change.append(node)
                continue

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
