#!/usr/bin/env python
import argparse
import imp
import sys
import time
from utils.logger import L
from utils.parser import P
from utils.visualizer import V

def error(msg):
    print "Error!", msg
    print
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help="JSON file containing intersection/car definitions")
    parser.add_argument('agent_file', help="Python file with AI Agent class to change lights")
    parser.add_argument('-b','--breakpoint',type=int,help="pause execution at this minor step and enter debug mode")
    parser.add_argument('-v','--verbose',action='count',help="print out debug info")
    parser.add_argument('-d','--draw',action='store_true',default=False,help="dump data.js")
    args = parser.parse_args()

    L.breakpoint = args.breakpoint
    L.verbosity = args.verbose or 0
    V.enabled = args.draw

    try:
        agent = imp.load_source('agent',args.agent_file).Agent()
    except IOError:
        error("Bad agent file: %s" % args.agent_file)
    except AttributeError:
        error("Agent file missing Agent() class definition")

    try:
        city = P.parse(args.data_file, agent)
    except IOError:
        error("Bad json data file: %s" % args.data_file)

    t = time.time()
    city.generate()
    L.log("")
    L.log("finished in %.2f seconds" % (time.time()-t))
