#!/usr/bin/env python3

from lib import *
from aux import bcolors, write_schedule
import argparse


# Schedule format inside the app: S = [["T1", "W", "X"], ["T2", "R", "X"]] -> S: W1(X), R2(X)

def exec(S, flag=False):
    if(args.verbose and cnt!=1): print("\n\n\n")
    print(f"{bcolors.OKCYAN}\nSCHEDULE {cnt}: {S}\n{bcolors.ENDC}")
    S = write_schedule(S)

    conf = conflict_serializable(S, flag)
    
    # if the schedule is conflict-serializable, we can proceede to check if it's in 2PL
    if not conf:
        print(f"{bcolors.OKGREEN}Schedule is conflict-serializable!{bcolors.ENDC}")
        print(f"\n{bcolors.ITALIC}Checking if it belongs to the 2PL class...{bcolors.ENDC}", end="\n\n")

        twoPL = check_2PL(S, flag)
        if(isinstance(twoPL, Schedule)):
            print(f"\n{bcolors.OKGREEN}Schedule is in 2PL class!{bcolors.ENDC}")
        else:
            print(f"{twoPL}")
    
    # else, we can still check if it's view-serializable
    else:
        print(f"{bcolors.FAIL}Schedule is not conflict-serializable!{bcolors.ENDC}\n")
        print(f"{bcolors.ITALIC}Checking view-serializability...{bcolors.ENDC}", end="\n\n")

        view = check_view(S, flag)
        if(view):
            print(f"Here is a view-equivalent schedule:")
            print("["+', '.join(['T' + str(num) for num in view.trans])+"]\n", bcolors.BOLD)
            print(view, f"{bcolors.ENDC}\n")
            print(f"{bcolors.OKGREEN}Schedule is view-serializable!{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Schedule is not view-serializable, couldn't find a view-equivalent serial schedule!{bcolors.ENDC}")



file = "schedules.txt"

# parser for verbosity and demo modes
parser = argparse.ArgumentParser(description="A Python application for schedules")
parser.add_argument('-v', '--verbose', action='store_true', help="increase output verbosity")
parser.add_argument('-d', '--demo', action="store_true", help="run a demo of the app")
args = parser.parse_args()
if args.verbose:
    print(f"{bcolors.OKGREEN}Verbose mode enabled. Providing more details...{bcolors.ENDC}")
if args.demo:
    print(f"{bcolors.OKGREEN}Demo mode enabled, checking a list of different schedules{bcolors.ENDC}")
    file = "demo.txt"


# Schedules are in schedules.txt
with open(file, "r") as file:
    lines = file.readlines()

cnt = 1
for line in lines:
    tmp = line.strip()
    if tmp != "":
        if(tmp[0] == "#"):
            continue
        exec(tmp, args.verbose)
        cnt+=1

