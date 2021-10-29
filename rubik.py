#!/usr/local/bin/python3

import sys
import moves as mov
import twa
import subprocess

def main():
    for arg in sys.argv:
        if arg == "./rubik.py" or arg == "rubik.py" or len(arg) == 0:
            continue
        if arg[0] == '-':
            mov.parse_opt(arg)
            if mov.opt[2] == True:
                break
        else:
            mov.parse_mix(arg)
            break
    if mov.state == mov.GOAL:
        print("No mix list or random option as arguments\n" + mov.USAGE)
    else:
        twa.solver()
        tmp = ""
        for m in mov.moves_log:
            tmp += m + ' '
        print(tmp)
        if mov.opt[0] == True:
            subprocess.run(["./Rubik.app/Contents/MacOS/42Rubik", mov.mix, tmp])

if __name__ == "__main__":
    main()
