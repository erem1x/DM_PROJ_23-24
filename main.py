from lib import *
# Schedule format: S = [["T1", "W", "X"], ["T2", "R", "X"]] -> S: W1(X), R2(X)

    
# not conf, view
ex1="r1(x) r1(t) r2(z) w3(x) w1(x) r1(y) w3(t) w2(x) w1(y)"

# not conf, not view
ex2="r1(y) r3(y) r1(x) w2(x) r2(y) w3(x) w2(y)"


def exec(S):
    print(f"{bcolors.OKCYAN}\nSCHEDULE: {S}\n{bcolors.ENDC}")
    S = write_schedule(S)
    main_fun(S)

exec(ex1)


