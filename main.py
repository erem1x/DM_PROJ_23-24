from lib import *
from aux import bcolors, write_schedule
# Schedule format: S = [["T1", "W", "X"], ["T2", "R", "X"]] -> S: W1(X), R2(X)

easy ="r2(A), r3(B), w1(A), r2(C), r2(D), w1(D)"

# not conf, view
ex1="r1(x) r1(t) r2(z) w3(x) w1(x) r1(y) w3(t) w2(x) w1(y)"

# not conf, view
ex2="r3(B), w1(A), w3(B), r1(B), r2(A), w3(A), w2(A)"

# nothing
ex3="r1(y) r3(y) r1(x) w2(x) r2(y) w3(x) w2(y)"

# not conf, view
ex4="r1(x) r4(y) w1(z) r4(z) w2(y) r3(y) w1(x) w2(x) w3(z) w4(x) w3(x)"


def exec(S):
    print(f"{bcolors.OKCYAN}\nSCHEDULE: {S}\n{bcolors.ENDC}")
    S = write_schedule(S)
    main_fun(S)

exec(ex4)
exec(ex3)
exec(ex2)


