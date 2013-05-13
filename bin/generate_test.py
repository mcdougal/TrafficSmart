#!/usr/bin/env python
import json
import os
import random
import sys

class TestGenerator(object):
    def __init__(self, width, height, min_cars, max_cars):
        self.width = width
        self.height = height
        self.min_cars = min_cars
        self.max_cars = max_cars

    def generate(self):
        city = self.generate_city()

        for y, row in enumerate(city['city']):
            for x, node in enumerate(row):
                for d in ["north","south","east","west"]:
                    for i in range(random.randint(self.min_cars, self.max_cars)):
                        self.add_cars_to_node(city, node, x, y, d)

        return city

    def generate_city(self):
        city = {"city": []}
        for y in range(height):
            row = []
            for x in range(width):
                green = "h" if random.randint(0,0) else "v"
                row.append({"green": green})
            city['city'].append(row)

        return city

    def add_cars_to_node(self, city, node, x, y, d):
        carsd = "cars_%s" % d
        if carsd not in node:
            node[carsd] = []

        path = self.generate_path(city, node, x, y, d)
        node[carsd].append({"path": path})

    def generate_path(self, city, node, x, y, d):
        path = []
        while self.in_bounds(city, x, y):
            next_turn = random.choice(["left","right","straight"])
            path.append(next_turn)
            x, y, d = self.get_dest(x, y, d, next_turn)
        return path

    def in_bounds(self, city, x, y):
        return x >= 0 \
            and x < len(city["city"][0]) \
            and y >= 0 \
            and y < len(city["city"])

    def get_dest(self, x, y, start_direction, turn):
        if start_direction == "north" and turn == "left":
            return x+1, y, "west"
        if start_direction == "north" and turn == "right":
            return x-1, y, "east"
        if start_direction == "north" and turn == "straight":
            return x, y+1, "north"

        if start_direction == "south" and turn == "left":
            return x-1, y, "east"
        if start_direction == "south" and turn == "right":
            return x+1, y, "west"
        if start_direction == "south" and turn == "straight":
            return x, y-1, "south"

        if start_direction == "east" and turn == "left":
            return x, y+1, "north"
        if start_direction == "east" and turn == "right":
            return x, y-1, "south"
        if start_direction == "east" and turn == "straight":
            return x-1, y, "east"

        if start_direction == "west" and turn == "left":
            return x, y-1, "south"
        if start_direction == "west" and turn == "right":
            return x, y+1, "north"
        if start_direction == "west" and turn == "straight":
            return x+1, y, "west"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('output_file')
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    parser.add_argument('--min', type=int, default=1)
    parser.add_argument('--max', type=int, default=3)
    parser.add_argument('--force', action="store_true", default=False)
    args = parser.parse_args()

    width = args.width
    height = args.height
    filename = args.output_file

    if width <= 0 or height <= 0:
        print "Please specify width and height > 0"
        sys.exit(1)

    if args.min and args.min < 0:
        print "Please specify a at least 0 cars as the minimum"
        sys.exit(1)
    if args.max and args.max > 3:
        print "Please specify a at most 3 cars as the maximum"
        sys.exit(1)

    if not args.force and os.path.exists(filename):
        answer = raw_input("File exists. Overwrite? [Y/n] ")
        if answer.lower() == "n":
            sys.exit(0)

    city = TestGenerator(width, height, args.min, args.max).generate()

    with open(filename,"w") as f:
        f.write(json.dumps(city, sort_keys=True, indent=4))
