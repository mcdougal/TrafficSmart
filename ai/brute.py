from collections import defaultdict
from constants import *
from itertools import product
from utils.logger import L
from utils.timer import T
from utils.visualizer import V

class Agent(object):
    def change_lights(self, city):
        if not hasattr(self, "light_sequences"):
            light_combos = product([True,False], repeat=len(city.nodes_list))
            self.light_sequences = [x for x in product(light_combos, repeat=1)]
        
        lights_to_change = self.brute(city)
        if lights_to_change is None:
            lights_to_change = self.simple(city)

        return lights_to_change

    def heuristic(self, city):
        return city.num_cars() - city.num_full_streets()

    def brute(self, city):
        results = defaultdict(list)

        for x, light_sequence in enumerate(self.light_sequences):
            V.draw(city, msg="TESTING SEQUENCE: %s" % str(light_sequence), verbosity=3)
            history_index = city.get_history_index()

            for light_combo in light_sequence:
                V.draw(city, msg="COMBO: %s" % str(light_combo), verbosity=3)

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
            results[score].append(light_combo)
            city.rollback(history_index)
            V.draw(city, msg="SCORE: %s" % score, verbosity=3)

        best_result = min(results.keys())
        best_combos = results[best_result]
        if len(best_combos) > 1:
            V.draw(city, msg="NO BEST RESULT, FALLING BACK TO SIMPLE", verbosity=3)
            return None

        best_combo = best_combos[0]
        V.draw(city, msg="BEST RESULT: %s" % best_result, verbosity=3)
        V.draw(city, msg="USING COMBO: %s" % str(best_combo), verbosity=3)

        lights_to_change = []
        for i, node in enumerate(city.nodes_list):
            if best_combo[i]:
                lights_to_change.append(node)

        return lights_to_change

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
