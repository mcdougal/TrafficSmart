from constants import *
from utils.timer import T

class Agent(object):
    def change_lights(self, city):
        lights_to_change = set()
        lights_to_skip = set()

        for node in city.nodes_list:
            cars_out_v = sum([x.next_node is None for x in node.get_cars_at(NORTH)])
            cars_out_v += sum([x.next_node is None for x in node.get_cars_at(SOUTH)])

            cars_out_h = sum([x.next_node is None for x in node.get_cars_at(EAST)])
            cars_out_h += sum([x.next_node is None for x in node.get_cars_at(WEST)])

            if (node.green == HORIZONTAL and cars_out_v > cars_out_h) \
                    or node.green == VERTICAL and cars_out_h > cars_out_v:
                lights_to_change.add(node)

            elif cars_out_v or cars_out_h:
                lights_to_skip.add(node)

        for node in city.nodes_list:
            print 
            print "node:", node
            if node in lights_to_change or node in lights_to_skip:
                continue

            node_north = city.get_node(node.x, node.y-1)
            node_south = city.get_node(node.x, node.y+1)
            node_east = city.get_node(node.x+1, node.y)
            node_west = city.get_node(node.x-1, node.y)

            node_north_lane = node_north.num_cars(SOUTH) if node_north else -3
            node_south_lane = node_south.num_cars(NORTH) if node_south else -3
            node_east_lane = node_east.num_cars(WEST) if node_east else -3
            node_west_lane = node_west.num_cars(EAST) if node_west else -3

            for car in node.get_cars_at(NORTH):
                if car.next_turn() == STRAIGHT:
                    node_south_lane += 1
                if car.next_turn() == LEFT:
                    node_east_lane += 1
                if car.next_turn() == RIGHT:
                    node_west_lane += 1

            for car in node.get_cars_at(SOUTH):
                if car.next_turn() == STRAIGHT:
                    node_north_lane += 1
                if car.next_turn() == LEFT:
                    node_west_lane += 1
                if car.next_turn() == RIGHT:
                    node_east_lane += 1

            if node_north_lane == 3 or node_south_lane == 3:
                if node.green == HORIZONTAL:
                    lights_to_change.add(node)
                    continue
                else:
                    lights_to_skip.add(node)
                    continue

            if node_east_lane == 3 or node_west_lane == 3:
                if node.green == VERTICAL:
                    lights_to_change.add(node)
                    continue
                else:
                    lights_to_skip.add(node)
                    continue

            node_north_lane = node_north.num_cars(SOUTH) if node_north else -3
            node_south_lane = node_south.num_cars(NORTH) if node_south else -3
            node_east_lane = node_east.num_cars(WEST) if node_east else -3
            node_west_lane = node_west.num_cars(EAST) if node_west else -3

            for car in node.get_cars_at(EAST):
                if car.next_turn() == STRAIGHT:
                    node_west_lane += 1
                if car.next_turn() == LEFT:
                    node_south_lane += 1
                if car.next_turn() == RIGHT:
                    node_north_lane += 1

            for car in node.get_cars_at(WEST):
                if car.next_turn() == STRAIGHT:
                    node_east_lane += 1
                if car.next_turn() == LEFT:
                    node_north_lane += 1
                if car.next_turn() == RIGHT:
                    node_south_lane += 1

            if node_north_lane == 3 or node_south_lane == 3:
                if node.green == HORIZONTAL:
                    lights_to_change.add(node)
                    continue
                else:
                    lights_to_skip.add(node)
                    continue

            if node_east_lane == 3 or node_west_lane == 3:
                if node.green == VERTICAL:
                    lights_to_change.add(node)
                    continue
                else:
                    lights_to_skip.add(node)
                    continue

        for node in set(city.nodes_list) - lights_to_change - lights_to_skip:
            if self.simple(city, node):
                lights_to_change.add(node)

        return lights_to_change

    def simple(self, city, node):
        if T.light_cycle != 0 and not city.cars_moved():
            return True

        num_cars_north = len(node.cars[NORTH])
        num_cars_south = len(node.cars[SOUTH])
        num_cars_east = len(node.cars[EAST])
        num_cars_west = len(node.cars[WEST])

        num_cars_vertical = num_cars_north + num_cars_south
        num_cars_horizontal = num_cars_east + num_cars_west

        if num_cars_vertical + num_cars_horizontal == 0:
            return False

        if num_cars_vertical > num_cars_horizontal:
            if node.green == HORIZONTAL:
                return True

        if num_cars_horizontal > num_cars_vertical:
            if node.green == VERTICAL:
                return True

