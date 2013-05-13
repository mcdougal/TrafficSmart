from constants import *
from utils.logger import L
from utils.timer import T

class Agent(object):
    def change_lights(self, city):
        #list of changed lights
        lights_to_change = []
        
        # do for all nodes
        for i, node in enumerate(city.nodes_list):
            
            #Find the space left for cars going out of the intersection 
            space_left = {NORTH:STREET_SIZE, SOUTH:STREET_SIZE, EAST:STREET_SIZE,
                          WEST:STREET_SIZE}
            
            #Saves the number of cars that can move out of the intersection in 
            #light cycle for all four direction
            car_moving = {NORTH:0, SOUTH:0, EAST:0, WEST:0}
            
            #x and y of node/intersection
            x = node.x
            y = node.y
            
            #if there is an intersection to the west of the current intersection
            if city.get_node(x - 1, y) != None:
                #find the space left that can move into that intersection
                space_left[WEST] = city.get_node(x - 1, y).get_space_left(EAST)
            if city.get_node(x + 1 , y) != None:
                space_left[EAST] = city.get_node(x + 1, y).get_space_left(WEST)
            if city.get_node(x, y + 1) != None:
                space_left[SOUTH] = city.get_node(x, y + 1).get_space_left(NORTH)
            if city.get_node(x, y - 1) != None:
                space_left[NORTH] = city.get_node(x, y - 1).get_space_left(SOUTH)
                
            #check how many cars moving from the south of the intersection(facing north or moving up)
            #can actually clear the intersection    
            for car in node.cars[SOUTH]:
                #if car is turning right, its moving east
                if car.is_turning(RIGHT):
                    #check if there is space to the east of the intersection
                    if space_left[EAST] > car_moving[EAST]:
                        car_moving[EAST] += 1
                    else:
                        #since the cars behind this car can't move until this
                        #car moves, we end here
                        break
                #similarly for cars turning left
                elif car.is_turning(LEFT):
                    if space_left[WEST] > car_moving[WEST]:
                        car_moving[WEST] += 1
                    else:
                        break
                elif space_left[NORTH] > car_moving[NORTH]:
                    car_moving[NORTH] += 1
                    #print "straight"
                else:
                    break
            
            #similar to the above for loop, execpt the cars are in the north street
            #facing/moving south
            for car in node.cars[NORTH]:
                if car.is_turning(LEFT):
                    if space_left[EAST] > car_moving[EAST]:
                        car_moving[EAST] += 1
                    else:
                        break
                elif car.is_turning(RIGHT):
                    if space_left[WEST] > car_moving[WEST]:
                        car_moving[WEST] += 1
                    else:
                        break
                elif space_left[SOUTH] > car_moving[SOUTH]:
                    car_moving[SOUTH] += 1
                else:
                    break
            #total number of cars that can move when the signal is green for north/south streets
            totalCarNorthSouth = sum(car_moving.values())
            
            #reset the car_moving dict for finding cars moving east/west
            
            car_moving = {NORTH:0, SOUTH:0, EAST:0, WEST:0}
            for car in node.cars[WEST]:
                if car.is_turning(RIGHT):
                    if space_left[SOUTH] > car_moving[SOUTH]:
                        car_moving[SOUTH] += 1
                    else:
                        break
                elif car.is_turning(LEFT):
                    if space_left[NORTH] > car_moving[NORTH]:
                        car_moving[NORTH] += 1
                    else:
                        break
                elif space_left[EAST] > car_moving[EAST]:
                    car_moving[EAST] += 1
                else:
                    break
            for car in node.cars[EAST]:
                if car.is_turning(LEFT):
                    if space_left[SOUTH] > car_moving[SOUTH]:
                        car_moving[SOUTH] += 1
                    else:
                        break
                elif car.is_turning(RIGHT):
                    if space_left[NORTH] > car_moving[NORTH]:
                        car_moving[NORTH] += 1
                    else:
                        break
                elif space_left[WEST] > car_moving[WEST]:
                    car_moving[WEST] += 1
                else:
                    break
            #sum cars that can move east/west
            totalCarEastWest = sum(car_moving.values())
            
            #check if we need to change lights
            #if signal is green for north/south and more cars can go through east/west
            if node.green == VERTICAL and totalCarNorthSouth < totalCarEastWest:
                #change lights
                lights_to_change.append(node)
            #similar check to above
            elif node.green == HORIZONTAL and totalCarNorthSouth > totalCarEastWest:
                lights_to_change.append(node)
                
        return lights_to_change
