from lib import *
from aux import bcolors, write_schedule
import argparse
# Schedule format: S = [["T1", "W", "X"], ["T2", "R", "X"]] -> S: W1(X), R2(X)

def exec(S, flag=False):
    print(f"{bcolors.OKCYAN}\nSCHEDULE: {S}\n{bcolors.ENDC}")
    S = write_schedule(S)
    main_fun(S, flag)

# parser for verbosity mode
parser = argparse.ArgumentParser(description="A Python application for schedules")
parser.add_argument('-v', '--verbose', action='store_true', help="increase output verbosity")
args = parser.parse_args()
if args.verbose:
    print(f"{bcolors.OKGREEN}\nVerbose mode enabled. Providing more details...{bcolors.ENDC}")


# Schedules are in schedules.txt
with open("schedules.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    tmp = line.strip()
    exec(tmp, args.verbose)

