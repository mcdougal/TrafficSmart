#!/usr/bin/env python
import os
import re
import sys; sys.path.append("..")
from subprocess import Popen, PIPE
from utils.lib.timeout import *

@timeout(10)
def run_test(f, agent):
    sys.stdout.flush()
    cmd = ["../run.py", os.path.join("..","tests",f), args.agent]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    return p.stdout.read()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('agent')
    args = parser.parse_args()

    test_files = []
    for f in os.listdir("../tests"):
        if f.endswith(".json"):
            test_files.append(f)

    ljust = max(map(len, test_files)) + 1

    for f in os.listdir("../tests"):
        if f.endswith(".json"):
            print f.ljust(ljust),
            try:
                result = run_test(f, args.agent)
                print re.search(r"Cycles: (\d+)", result).group(1)
            except TimeoutError:
                print "timeout"
        
