from collections import defaultdict
from constants import *
from itertools import product
from numpy import mean
from utils.logger import L
from utils.timer import T
from utils.visualizer import V

DEPTH = 3

class Agent(object):
    def __init__(self):
        self.sequence = []

    def change_lights(self, city):
        if not hasattr(self, "light_combos"):
            # raw_input("making light combos...")
            self.light_combos = list(product([True,False], repeat=len(city.nodes_list)))
            # raw_input("light combos: %s" % len(self.light_combos))

        if not hasattr(self, "threshold"):
            num_combos = len(self.light_combos)
            x = 0
            num_sequences = None
            while num_sequences is None or num_sequences > 512:
                num_combos /= 2
                num_sequences = num_combos ** DEPTH
                x += 1
            self.threshold = x
            # raw_input("threshold: %s" % self.threshold)

        if self.sequence:
            return self.sequence.pop()

        node_map = {i:node.num_cars() for i, node in enumerate(city.nodes_list)}
        node_map = sorted(node_map.iteritems(), key=lambda x: x[1])
        node_map = node_map[:self.threshold]
        wildcards = [x[0] for x in node_map]

        light_combos = []
        for combo in self.light_combos:
            if all([combo[wildcard] for wildcard in wildcards]):
                light_combos.append(combo)

        # raw_input("light combos: %s" % len(light_combos))

        light_sequences = list(product(light_combos, repeat=DEPTH))

        # raw_input("light sequences: %s" % len(light_sequences))

        lights_to_change = self.brute(city, light_sequences)
        if lights_to_change is None:
            lights_to_change = self.simple(city)

        return lights_to_change

    def heuristic(self, city):
        return city.num_cars() - city.num_full_streets()

    def brute(self, city, light_sequences):
        results = defaultdict(list)

        for light_sequence in light_sequences:
            V.draw(city, msg="TESTING SEQUENCE: %s" % str(id(light_sequence))[-3:], verbosity=3)
            history_index = city.get_history_index()

            for light_combo in light_sequence:

                if L.verbosity < 4:
                    L.pause()
                    V.pause()

                for i, node in enumerate(city.nodes_list):
                    if light_combo[i]:
                        city.change_light(node)
                city.cycle()

                if L.verbosity < 4:
                    L.play()
                    V.play()

                if not city.has_cars():
                    break

            score = self.heuristic(city)
            results[score].append(light_sequence)
            city.rollback(history_index)
            V.draw(city, msg="SCORE: %s" % score, verbosity=3)

        best_result = min(results.keys())
        best_sequences = results[best_result]
        if len(best_sequences) > 1:
            V.draw(city, msg="NO BEST RESULT, FALLING BACK TO SIMPLE", verbosity=3)
            return None

        best_sequence = best_sequences[0]
        V.draw(city, msg="BEST RESULT: %s" % best_result, verbosity=3)

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
