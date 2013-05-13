from constants import *
from logger import L
from timer import T

class Visualizer(object):
    def __init__(self):
        self.enabled = True
        self.paused = False

    def pause(self):
        self.paused = True

    def play(self):
        self.paused = False

    def create_data_file(self):
        with open(VISUALIZER_DATA_FILE,"w") as f:
            f.write("")

    def create_settings_file(self, city):
        city_size = max(city.num_rows()+1, city.num_cols()+1)
        block_size = CANVAS_SIZE / city_size
        lines = [
            "var blockSize = %s;" % block_size,
            "var speed = %s;" % START_SPEED,
            ]
        with open(VISUALIZER_SETTINGS_FILE,"w") as f:
            f.write("\n".join(lines)+"\n")

    def draw_node(self, *args):
        return 'drawIntersection(%s,%s,"%s",%s);' % args

    def draw_car(self, *args):
        return 'drawCar(%s,%s,"%s",%s,"%s",%s,%s,%s);' % args

    def draw(self, city, focused_node=None, focused_car=None, msg="", verbosity=0):
        if not self.enabled:
            T.increment_frame()
            return
        if self.paused or verbosity > L.verbosity:
            return

        if T.frame == 0:
            self.create_settings_file(city)
            self.create_data_file()
            lines = ["frame0();"]
        else:
            lines = []

        lines.append("function frame%s() {" % T.frame)

        lines += [
            "thisFrame = frame%s;" % T.frame,
            "previousFrame = frame%s;" % max(T.frame-1, 0),
            "if (typeof frame%s == 'function') {" % (T.frame+1),
            "    nextFrame = frame%s;" % (T.frame+1),
            "}",
            "else {",
            "    nextFrame = frame%s;" % T.frame,
            "}",
            ]

        if T.beginning_of_time_step:
            lines += [
                "if (typeof timestep%s == 'function') {" % max(T.time_step-1, 0),
                "    previousTimestep = timestep%s;" % max(T.time_step-1, 0),
                "}",
                "else {",
                "    previousTimestep = frame0;",
                "}",
                "if (typeof timestep%s == 'function') {" % (T.time_step+1),
                "    nextTimestep = timestep%s;" % (T.time_step+1),
                "}",
                "else {",
                "    nextTimestep = frame%s;" % T.frame,
                "}",
                ]

        if T.beginning_of_light_cycle:
            lines += [
                "if (typeof cycle%s == 'function') {" % max(T.light_cycle-1, 0),
                "    previousCycle = cycle%s;" % max(T.light_cycle-1, 0),
                "}",
                "else {",
                "    previousCycle = frame0;",
                "}",
                "if (typeof cycle%s == 'function') {" % (T.light_cycle+1),
                "    nextCycle = cycle%s;" % (T.light_cycle+1),
                "}",
                "else {",
                "    nextCycle = frame%s;" % T.frame,
                "}",
                ]

        lines += [
            "clear();",
            "drawNavIcon();",
            "drawCycle(%s);" % T.light_cycle,
            "drawSubCycle(%s);" % T.sub_cycle,
            "drawFrame(%s);" % T.frame,
            'drawMessage("%s");' % msg,
            "drawSpeed();",
            ]

        for node in city.nodes_list:
            focused = "true" if node == focused_node else "false"
            x, y, green = node.x, node.y, node.green
            lines.append(self.draw_node(x, y, green, focused))
            for d in [NORTH,SOUTH,EAST,WEST]:
                for p, car in enumerate(node.cars[d]):
                    t = car.next_turn()
                    f = "true" if car == focused_car else "false"
                    m = "true" if car.already_moved() else "false"
                    b = "true" if car.is_blocked() else "false"
                    lines.append(self.draw_car(x, y, d, p, t, f, m, b))

        lines += [
            "drawNextFrame();",
            "}",
            "lastFrame = frame%s;" % T.frame,
            ]

        if T.beginning_of_time_step:
            lines.append(
                "timestep%s = frame%s;" % (T.time_step, T.frame))

        if T.beginning_of_light_cycle:
            lines.append(
                "cycle%s = frame%s;" % (T.light_cycle, T.frame))

        with open(VISUALIZER_DATA_FILE,"a") as f:
            f.write("\n".join(lines)+"\n\n")

        T.increment_frame()

V = Visualizer()
