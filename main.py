from lib import *
# Schedule format: S = [["T1", "W", "X"], ["T2", "R", "X"]] -> S: W1(X), R2(X)

    

schedule = ("w3(A) w2(C) r1(A) w1(B) r1(C) w2(A) r4(A) w4(D)")

schedule2 = ("R1(A) R2(A) R3(B) W1(A) R2(C) R2(B) W2(B) W1(C)")

schedule3 = "r1(A) w2(A) r2(B) w3(B) r4(B) w4(C) w4(D) r5(C) r6(C) r7(D) w7(E) r8(E)"

exercise4 = "w1(x) r2(x) w1(z) r2(z) r3(x) r4(z) w4(z) w2(x)"


print("\nSCHEDULE: ",schedule,"\n\n")
precedence_graph(write_schedule(schedule))

print("\nSCHEDULE: ",schedule2,"\n\n")
precedence_graph(write_schedule(schedule2))

print("\nSCHEDULE: ",schedule3,"\n\n")
precedence_graph(write_schedule(schedule3))

print("\nSCHEDULE: ",exercise4,"\n\n")
precedence_graph(write_schedule(exercise4))

