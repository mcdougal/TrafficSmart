from collections import defaultdict
from constants import *
from copy import deepcopy
from utils.logger import L
from utils.timer import T
from utils.visualizer import V

class City(object):

    #
    # SETUP
    #

    def __init__(self, nodes, agent):
        self.nodes = nodes
        self.agent = agent
        self.memoize()
        self.history = []
        self.T = T

    def copy(self):
        new_timer = self.T.copy()
        nodes_copy = []
        nodes_map = {}
        for row in self.nodes:
            nodes_copy_row = []
            for node in row:
                node_copy = node.copy(new_timer)
                nodes_copy_row.append(node_copy)
                nodes_map[node] = node_copy
            nodes_copy.append(nodes_copy_row)

        copy = City(nodes_copy, None)
        copy.memoize()
        copy.history = list(self.history)
        copy.T = new_timer

        for car in copy.cars_list:
            node_path_copy = []
            for node, direction in car.node_path:
                node_path_copy.append((nodes_map[node], direction))
            car.node_path = node_path_copy

            node_path_history_copy = []
            for node, direction in car.node_path_history:
                node_path_history_copy.append((nodes_map[node], direction))
            car.node_path_history = node_path_history_copy

        return copy

    def memoize(self):
        self.nodes_list = []
        for row in self.nodes:
            for node in row:
                self.nodes_list.append(node)

        self.cars_list = []
        for node in self.nodes_list:
            for d in [NORTH,SOUTH,EAST,WEST]:
                for car in node.cars[d]:
                    self.cars_list.append(car)

    #
    # GENERATION
    #

    def generate(self):
        V.draw(self, msg="starting simulation...")

        while self.has_cars():
            L.log("Light cycle %s" % self.T.light_cycle)
            self.change_lights()
            self.cycle()
            self.T.increment_light_cycle()

        L.log("")
        L.log("SUCCESS! All cars are out of the city.")
        L.log("Cycles: %s" % self.T.light_cycle, 0)

    def change_lights(self):
        L.log("  checking for light change")
        V.draw(self, msg="changing lights...")
        
        nodes_to_change = self.agent.change_lights(self)
        if not nodes_to_change:
            L.log("    no change needed")
            V.draw(self, msg="no change needed")
        else:
            for node in nodes_to_change:
                self.change_light(node)
            L.log("    lights changed")
            V.draw(self)

    def cycle(self):
        for i in range(CYCLE_SIZE):
            L.log("  Sub cycle %s" % self.T.sub_cycle)
            self.time_step()
            self.T.increment_time_step()

    def time_step(self):
        moved = {}

        for node in self.nodes_list:
            V.draw(self, node, msg="checking node %s" % node, verbosity=5)

            if node.green == HORIZONTAL:
                dir1, dir2 = EAST, WEST
            else:
                dir1, dir2 = NORTH, SOUTH

            car1 = node.get_car_at(dir1)
            car2 = node.get_car_at(dir2)

            # check if we already moved a car at car1's position
            if (node, dir1) in moved:
                turn = moved[(node, dir1)]
                V.draw(self,node,msg="already moved a car %s at %s %s" % (turn,node,dir1),verbosity=5)
                # make sure we don't move the next car
                if car1:
                    car1.block()
                    V.draw(self, node, msg="don't move the next car", verbosity=5)
                    car1 = None

                # check if the opposite car would have been able to move
                if car2:
                    free_turns = node.get_free_turns(turn, car2.next_turn())
                    if free_turns == 1:
                        car2.block()
                        V.draw(self, node, msg="don't move the opposite car", verbosity=5)
                        car2 = None

            # check if we already moved a car at car2's position
            if (node, dir2) in moved:
                turn = moved[(node, dir2)]
                V.draw(self,node,msg="already moved a car %s at %s %s" % (turn,node,dir2),verbosity=5)
                # make sure we don't move the next car
                if car2:
                    car2.block()
                    V.draw(self, node, msg="don't move the next car", verbosity=5)
                    car2 = None

                # check if the opposite car would have been able to move
                if car1:
                    free_turns = node.get_free_turns(turn, car1.next_turn())
                    if free_turns == 1:
                        car1.block()
                        V.draw(self, node, msg="don't move the opposite car", verbosity=5)
                        car1 = None

            free_cars = node.get_free_cars(car1, car2)

            # check who can and can't turn
            blocked_car1 = False
            blocked_car2 = False
            if len(free_cars) == 2:
                V.draw(self, node, msg="both cars can turn", verbosity=5)
            else:
                if car1:
                    if car1 in free_cars:
                        V.draw(self, node, car1, msg="car1 is free", verbosity=5)
                    else:
                        car1.block()
                        blocked_car1 = True
                        V.draw(self, node, msg="car1 is not free", verbosity=5)
                if car2:
                    if car2 in free_cars:
                        V.draw(self, node, car2, msg="car2 is free", verbosity=5)
                    else:
                        car2.block()
                        blocked_car2 = True
                        V.draw(self, node, msg="car2 is not free", verbosity=5)

            # move car1
            moved_car1 = False
            moved_car2 = False
            if car1 and car1 in free_cars:
                chain = self.get_move_chain(car1)
                if car1 in chain:
                    moved_car1 = True
                    for car in reversed(chain):
                        moved[car.current_node()] = car.next_turn()
                        self.move(car)
                else:
                    # if car1 can't move, see if car2 can move
                    V.draw(self, node, msg="car1 can't turn!", verbosity=5)
                    if car2:
                        if blocked_car2:
                            car2.unblock()
                        V.draw(self, node, car2, msg="let's see if car2 can turn", verbosity=5)
                        chain = self.get_move_chain(car2)
                        if car2 not in chain:
                            car2.block()
                            V.draw(self, node, msg="car2 can't turn either :(", verbosity=5)
                        else:
                            V.draw(self, node, msg="but car2 can!", verbosity=5)
                            moved_car2 = True
                            for car in reversed(chain):
                                moved[car.current_node()] = car.next_turn()
                                self.move(car)

            # move car2
            if not moved_car2 and car2 and car2 in free_cars:
                chain = self.get_move_chain(car2)
                if car2 in chain:
                    for car in reversed(chain):
                        moved[car.current_node()] = car.next_turn()
                        self.move(car)
                else:
                    # if car2 can't move, see if car1 can move
                    V.draw(self, node, msg="car2 can't turn!", verbosity=5)
                    if not moved_car1 and car1:
                        if blocked_car1:
                            car1.unblock()
                        V.draw(self, node, car2, msg="let's see if car1 can turn", verbosity=5)
                        chain = self.get_move_chain(car1)
                        if car1 not in chain:
                            car1.block()
                            V.draw(self, node, msg="car1 can't turn either :(", verbosity=5)
                        else:
                            V.draw(self, node, msg="but car1 can!", verbosity=5)
                            for car in reversed(chain):
                                moved[car.current_node()] = car.next_turn()
                                self.move(car)

    def get_move_chain(self, car, block_chain=None, proper_blocked=None):
        chain = [car] # for order preservation
        chain_set = {car} # for constant time lookups
        next_node, next_direction = car.next_node()

        if block_chain is None:
            block_chain = {car}
        else:
            block_chain.add(car)

        if proper_blocked is None:
            proper_blocked = set()

        V.draw(self, car.current_node()[0], car, "I WANNA GO!", 5)

        while next_node and not next_node.has_space(next_direction):
            # cars are blocked by light
            if (next_node.green == HORIZONTAL and next_direction not in (EAST,WEST)) \
                    or (next_node.green == VERTICAL and next_direction not in (NORTH,SOUTH)):
                V.draw(self, next_node, car, "stoopid lights", 5)
                chain = []
                break

            next_car = next_node.get_car_at(next_direction)
            if not next_car:
                V.draw(self, car.current_node()[0], car, "looks like the street is full", 5)
                chain = []
                break

            V.draw(self, next_node, next_car, "I WANNA GO!", 5)

            # we got back to a car in the chain, so there's a loop
            if next_car in chain_set:
                V.draw(self, next_node, next_car, "hai! it's me again :)", 5)
                chain = chain[chain.index(next_car):]
                break

            opposite_direction = NORTH if next_direction == SOUTH \
                else SOUTH if next_direction == NORTH \
                else EAST if next_direction == WEST \
                else WEST
            opposite_car = next_node.get_car_at(opposite_direction)

            # cars are blocked by car that can't turn
            cars = next_node.get_free_cars(next_car, opposite_car)
            if next_car not in cars and opposite_car not in proper_blocked:
                V.draw(self, next_node, next_car, "ut oh! I'm blocked ><", 5)

                # if the blocking car is in the block chain, this block can't be fixed
                if opposite_car in block_chain:
                    V.draw(self, next_node, opposite_car, "hai! it's me again :)", 5)
                    V.draw(self, car.current_node()[0], car, "guess I'm proper blocked", 5)
                    proper_blocked.add(car)
                    car.block()
                    chain = []
                    break

                # if the blocking car can't move, our chain can go
                opposite_chain = self.get_move_chain(opposite_car, block_chain, proper_blocked)
                if opposite_car in opposite_chain:
                    next_car.block()
                    V.draw(self, next_node, msg="well, i iz blocked for sure...", verbosity=5)
                    chain = []
                    break

            # this car is part of the chain
            chain.append(next_car)
            chain_set.add(next_car)
            block_chain.add(next_car)

            # check if the car can move
            next_node, next_direction = next_car.next_node()
            if not next_node or next_node.has_space(next_direction):
                V.draw(self, next_car.current_node()[0], next_car, "I can haz move now", 5)
                break

        return chain

    def move(self, car):
        start_node, start_direction = car.current_node()
        end_node, end_direction = car.next_node()

        V.draw(self, focused_node=start_node, focused_car=car)
        L.log("    moving %s %s" % (car, car.next_turn()))
        L.log("      moving to %s" % end_node, 2)

        self.remove_car_from_node(start_node, start_direction)
        L.log("      removed from %s %s" % car.current_node(), 2)

        if not end_node:
            self.remove_car_from_cars_list(car)
        else:
            self.put_car_at_node(end_node, end_direction, car)
            L.log("      added to %s %s" % car.next_node(), 2)

        self.move_car(car)

        V.draw(self, focused_node=start_node, focused_car=car)

    #
    # UTILS
    #

    def get_node(self, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return self.nodes[y][x]
        except IndexError, TypeError:
            return None

    def cars_moved(self):
        car_moved = lambda x: x.last_move >= self.T.light_cycle-1
        return any(map(car_moved, self.cars_list))
        
    def has_cars(self):
        for node in self.nodes_list:
            if node.has_cars():
                return True

    def num_cars(self):
        return len(self.cars_list)

    def num_full_streets(self):
        full_streets = 0
        for node in self.nodes_list:
            for direction in [NORTH,SOUTH,EAST,WEST]:
                if node.num_cars(direction) == STREET_SIZE:
                    full_streets += 1

        return full_streets

    def num_rows(self):
        return len(self.nodes)

    def num_cols(self):
        return len(self.nodes[0])

    #
    # TRACKED ACTIONS
    #

    NODE_CHANGED = "NODE_CHANGED"
    REMOVE_CAR_FROM_NODE = "REMOVE_CAR_FROM_NODE"
    PUT_CAR_AT_NODE = "PUT_CAR_AT_NODE"
    REMOVED_FROM_CARS_LIST = "REMOVED_FROM_CARS_LIST"
    MOVE_CAR = "MOVE_CAR"

    def change_light(self, node):
        node.change_light()
        self.history.append((self.NODE_CHANGED, node))

    def unchange_light(self, node):
        node.change_light()

    def remove_car_from_node(self, node, direction):
        car = node.pop(direction)
        self.history.append((self.REMOVE_CAR_FROM_NODE, node, direction, car))

    def unremove_car_from_node(self, node, direction, car):
        node.unpop(direction, car)

    def put_car_at_node(self, node, direction, car):
        node.put(car, direction)
        self.history.append((self.PUT_CAR_AT_NODE, node, direction, car))

    def unput_car_at_node(self, node, direction, car):
        node.unput(car, direction)

    def remove_car_from_cars_list(self, car):
        self.cars_list.remove(car)
        self.history.append((self.REMOVED_FROM_CARS_LIST, car))

    def unremove_car_from_cars_list(self, car):
        self.cars_list.append(car)

    def move_car(self, car):
        car.move()
        self.history.append((self.MOVE_CAR, car))

    def unmove_car(self, car):
        car.unmove()

    def get_history_index(self):
        return len(self.history)

    def rollback(self, index):
        for i in range(len(self.history) - index):
            event = self.history.pop()
            action = event[0]
            params = event[1:]

            func = None
            if action == self.NODE_CHANGED:
                func = self.unchange_light
            elif action == self.REMOVE_CAR_FROM_NODE:
                func = self.unremove_car_from_node
            elif action == self.PUT_CAR_AT_NODE:
                func = self.unput_car_at_node
            elif action == self.REMOVED_FROM_CARS_LIST:
                func = self.unremove_car_from_cars_list
            elif action == self.MOVE_CAR:
                func = self.unmove_car

            func(*params)

class Node(object):
    def __init__(self, x, y, green, cars):
        self.x = x
        self.y = y
        self.green = green
        self.cars = cars
        self.T = T

    def __str__(self):
        return "%s,%s" % (self.x, self.y)

    def __repr__(self):
        return "%s,%s" % (self.x, self.y)

    def copy(self, new_timer):
        cars_copy = {}
        for direction, cars_list in self.cars.iteritems():
            cars_copy[direction] = [car.copy(new_timer) for car in cars_list]
        copy = Node(self.x, self.y, self.green, cars_copy)
        copy.T = new_timer
        return copy

    def change_light(self):
        if self.green == HORIZONTAL:
            self.green = VERTICAL
        else:
            self.green = HORIZONTAL

    def pop(self, direction):
        return self.cars[direction].pop(0)

    def unpop(self, direction, car):
        return self.cars[direction].insert(0, car)

    def put(self, car, direction):
        self.cars[direction].append(car)

    def unput(self, car, direction):
        self.cars[direction].pop()

    def get_cars_at(self, direction):
        return self.cars[direction]

    def get_car_at(self, direction):
        try:
            car = self.cars[direction][0]
            if not car.already_moved() and not car.is_blocked():
                return car
        except IndexError:
            return None

    def num_cars(self, direction=None):
        if direction is None:
            return sum(map(len, self.cars.itervalues()))
        return len(self.cars[direction])

    def has_space(self, direction):
        return len(self.cars[direction]) < STREET_SIZE
    
    def get_space_left(self, direction):
        return STREET_SIZE - len(self.cars[direction])
        
    def has_cars(self):
        return max([len(cars) for cars in self.cars.values()]) > 0

    def get_next_cars(self, skip_direction=None):
        if self.green == HORIZONTAL:
            return self.get_next_cars_for(EAST, WEST, skip_direction)
        else:
            return self.get_next_cars_for(NORTH, SOUTH, skip_direction)

    def get_next_cars_for(self, dir1, dir2, skip_direction=None):
        L.log("      dir1: %s" % dir1, 2)
        L.log("      dir2: %s" % dir2, 2)
        L.log("      cars %s: %s" % (dir1, self.cars[dir1]), 2)
        L.log("      cars %s: %s" % (dir2, self.cars[dir2]), 2)

        car1 = self.get_car_at(dir1)
        car2 = self.get_car_at(dir2)

        if skip_direction and dir1 in skip_direction:
            L.log("        already moved car from %s" % dir1, 2)
            car1 = None
        if skip_direction and dir2 in skip_direction:
            L.log("        already moved car from %s" % dir2, 2)
            car2 = None

        car1 = self.check_move(car1)
        car2 = self.check_move(car2)

        L.log("      car %s: %s" % (dir1, car1), 2)
        L.log("      car %s: %s" % (dir2, car2), 2)

        return self.get_free_cars(car1, car2)

    def check_move(self, car):
        if not car:
            return
        if car.already_moved():
            L.log("        car %s already moved" % car, 2)
            return
        next_node, next_direction = car.next_node()
        if next_node and not next_node.has_space(next_direction):
            L.log("        car %s no space in next node" % car, 2)
            return

        return car

    def get_free_cars(self, car1, car2):
        if not car1 and not car2:
            return []
        if car1 and not car2:
            return [car1]
        if not car1 and car2:
            return [car2]

        free_turns = self.get_free_turns(car1.next_turn(), car2.next_turn())
        if free_turns == 0:
            return [car1, car2]
        if free_turns == 1:
            return [car1]
        if free_turns == 2:
            return [car2]

        return []

    def get_free_turns(self, turn1, turn2):
        t = turn1 == STRAIGHT and turn2 == STRAIGHT
        t = t or turn1 == LEFT and turn2 == LEFT
        t = t or turn1 == RIGHT and turn2 == RIGHT
        t = t or turn1 == RIGHT and turn2 == STRAIGHT
        t = t or turn1 == STRAIGHT and turn2 == RIGHT
        if t:
            return 0 # both turning

        t = turn1 == RIGHT and turn2 == LEFT
        t = t or turn1 == STRAIGHT and turn2 == LEFT
        if t:
            return 1 # turn1 allowed

        t = turn1 == LEFT and turn2 == RIGHT
        t = t or turn1 == LEFT and turn2 == STRAIGHT
        if t:
            return 2 # turn2 allowed
        

class Car(object):
    def __init__(self, turn_path):
        self.turn_path = turn_path
        self.turn_path_history = []
        self.node_path = [] # generated on parse
        self.node_path_history = []
        self.last_move = None
        self.last_move_history = []
        self.blocked = None
        self.T = T

    def copy(self, new_timer):
        copy = Car(list(self.turn_path))
        copy.turn_path_history = list(self.turn_path_history)
        copy.node_path = self.node_path
        copy.node_path_history = self.node_path_history
        copy.last_move = self.last_move
        copy.last_move_history = list(self.last_move_history)
        copy.blocked = self.blocked
        copy.T = new_timer
        return copy

    def __str__(self):
        return str(id(self))[-3:]

    def __repr__(self):
        return str(id(self))[-3:]

    def next_turn(self):
        return self.turn_path[0]

    def current_node(self):
        return self.node_path[0]

    def next_node(self):
        try:
            return self.node_path[1]
        except IndexError:
            return None, None

    def is_turning(self, direction):
        return self.turn_path[0] == direction

    def move(self):
        self.turn_path_history.append(self.turn_path.pop(0))
        self.node_path_history.append(self.node_path.pop(0))
        self.last_move_history.append(self.last_move)
        self.last_move = self.T.light_cycle

    def unmove(self):
        self.turn_path.insert(0, self.turn_path_history.pop())
        self.node_path.insert(0, self.node_path_history.pop())
        self.last_move = self.last_move_history.pop()

    def already_moved(self):
        return self.last_move == self.T.light_cycle

    def block(self):
        self.blocked = self.T.time_step

    def unblock(self):
        self.blocked = None

    def is_blocked(self):
        return self.blocked == self.T.time_step
