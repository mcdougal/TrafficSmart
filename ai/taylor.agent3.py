from constants import *

class Agent(object):

    def change_lights(self, city):
    
        at_least_one_light_changed = False
        
        for x, y, node in city.iterate_nodes():
            num_cars_north = len(node.cars[NORTH])
            num_cars_south = len(node.cars[SOUTH])
            num_cars_east = len(node.cars[EAST])
            num_cars_west = len(node.cars[WEST])

            num_cars_vertical = num_cars_north + num_cars_south
            num_cars_horizontal = num_cars_east + num_cars_west
            num_cars_total = num_cars_vertical + num_cars_horizontal
            
            if num_cars_total == 0:
                continue
                
            if num_cars_vertical > num_cars_horizontal:
                if node.green == HORIZONTAL:
                    node.change_light()
                    at_least_one_light_changed = True

            if num_cars_horizontal > num_cars_vertical:
            #else:
                if node.green == VERTICAL:
                    node.change_light()
                    at_least_one_light_changed = True
        
        return at_least_one_light_changed