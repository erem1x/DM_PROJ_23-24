from lib import *
# Schedule format: S = [["T1", "W", "X"], ["T2", "R", "X"]] -> S: W1(X), R2(X)

    

schedule = ("w3(A) w2(C) r1(A) w1(B) r1(C) w2(A) r4(A) w4(D)")

schedule2 = ("R1(A) R2(A) R3(B) W1(A) R2(C) R2(B) W2(B) W1(C)")

print("\nSCHEDULE: ",schedule,"\n\n")
precedence_graph(write_schedule(schedule))

