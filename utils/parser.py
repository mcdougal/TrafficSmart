import json
from models import *

class Parser(object):
    def parse(self, json_file, agent):
        with open(json_file) as f:
            data = json.load(f)

        nodes = []
        for y, row_data in enumerate(data["city"]):
            row = []
            for x, node in enumerate(row_data):
                green = node["green"]
                cars = defaultdict(list)
                for direction in [NORTH,SOUTH,EAST,WEST]:
                    car_data = node.get("cars_%s" % direction,[])
                    for car in car_data:
                        cars[direction].append(Car(car["path"]))
                row.append(Node(x, y, green, cars))

            nodes.append(row)

        city = City(nodes, agent)
        self.create_node_paths(city)

        return city

    def create_node_paths(self, city):
        for node in city.nodes_list:
            for d in [NORTH,SOUTH,EAST,WEST]:
                for car in node.cars[d]:
                    self.parse_path(city, node, d, car)

    def parse_path(self, city, node, d, car):
        car.node_path.append((node, d))
        turn = car.turn_path[0]
        dest = self.get_dest(car, node, d, turn)
        end_node_x, end_node_y, end_direction = dest
        end_node = city.get_node(end_node_x, end_node_y)

        turn_index = 1
        while end_node is not None:
            car.node_path.append((end_node, end_direction))
            turn = car.turn_path[turn_index]
            dest = self.get_dest(car, end_node, end_direction, turn)
            end_node_x, end_node_y, end_direction = dest
            end_node = city.get_node(end_node_x, end_node_y)
            turn_index += 1

    def get_dest(self, car, start_node, start_direction, turn):
        x, y = start_node.x, start_node.y

        if start_direction == NORTH and turn == LEFT:
            return x+1, y, WEST
        if start_direction == NORTH and turn == RIGHT:
            return x-1, y, EAST
        if start_direction == NORTH and turn == STRAIGHT:
            return x, y+1, NORTH

        if start_direction == SOUTH and turn == LEFT:
            return x-1, y, EAST
        if start_direction == SOUTH and turn == RIGHT:
            return x+1, y, WEST
        if start_direction == SOUTH and turn == STRAIGHT:
            return x, y-1, SOUTH

        if start_direction == EAST and turn == LEFT:
            return x, y+1, NORTH
        if start_direction == EAST and turn == RIGHT:
            return x, y-1, SOUTH
        if start_direction == EAST and turn == STRAIGHT:
            return x-1, y, EAST

        if start_direction == WEST and turn == LEFT:
            return x, y-1, SOUTH
        if start_direction == WEST and turn == RIGHT:
            return x, y+1, NORTH
        if start_direction == WEST and turn == STRAIGHT:
            return x+1, y, WEST

P = Parser()
