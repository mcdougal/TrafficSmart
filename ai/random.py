import random

class Agent(object):
    def change_lights(self, city):
        lights_to_change = []
        for node in city.nodes_list:
            if random.randint(0,1):
                lights_to_change.append(node)

        return lights_to_change
