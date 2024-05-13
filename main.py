from lib import *
from aux import bcolors, write_schedule
# Schedule format: S = [["T1", "W", "X"], ["T2", "R", "X"]] -> S: W1(X), R2(X)

def exec(S):
    print(f"{bcolors.OKCYAN}\nSCHEDULE: {S}\n{bcolors.ENDC}")
    S = write_schedule(S)
    main_fun(S)


# Schedules are in schedules.txt

with open("schedules.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    tmp = line.strip()
    exec(tmp)

