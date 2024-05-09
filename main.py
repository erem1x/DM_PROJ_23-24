from lib import *
# Schedule format: S = [["T1", "W", "X"], ["T2", "R", "X"]] -> S: W1(X), R2(X)

    
# conf-ser
schedule = ("w3(A) w2(C) r1(A) w1(B) r1(C) w2(A) r4(A) w4(D)")
schedule2 = ("R1(A) R2(A) R3(B) W1(A) R2(C) R2(B) W2(B) W1(C)")
schedule3 = "r1(A) w2(A) r2(B) w3(B) r4(B) w4(C) w4(D) r5(C) r6(C) r7(D) w7(E) r8(E)"
exercise4 = "w1(x) r2(x) w1(z) r2(z) r3(x) r4(z) w4(z) w2(x)"

#view-ser
ex1 = "r3(B) w1(A) w3(B) r1(B) r2(A) w3(A) w2(A)"
ex2 = "w0(x) r2(x) r1(x) w2(x) w2(z)"
ex3 = "w1(y) r2(x) w2(x) r1(x) w2(z)"
ex4 = "w1(x) r2(x) w2(y) r1(y)"
ex5 = "w0(x) r1(x) w1(x) w2(z) w1(z)"


def exec(S):
    print("\nSCHEDULE: ", S,"\n\n")
    S=write_schedule(S)
    precedence_graph(S)
    check_view(S)

exec(ex5)

