from aux import *
# SET OF AUX FUNCTIONS

def conflict_serializable(S, flag):
    print(f"{bcolors.ITALIC}Checking conflict-serializability...{bcolors.ENDC}", end="\n\n")
    nodes, edges = precedence_graph(S, flag)
    check = check_cycle(nodes, edges)
    if(not check and flag):
        print("Here is a conflict-equivalent schedule:\n")
        order = topological_sort(nodes, edges)
        print(f"{bcolors.BOLD}{S.sort(order)}{bcolors.ENDC}\n")
    return check

        

# Function to assign locks and unlocks
# Most of the work is in the TwoPL class itself
def check_2PL(S, flag=False):
    Twolock = TwoPL(S)
    ret = Schedule()
    for elem in S.transactions:
        try:
            lock = Twolock.lock(elem, flag)
        except SystemError as e:
            if(flag):
                return f"{ret}\n\n{bcolors.FAIL}Schedule not in 2PL: {e}{bcolors.ENDC}"
            else:
                return "Schedule not in 2PL!"
        
        if(lock):
            for item in lock:
                ret.add(item)
        
        unlock = Twolock.unlock(elem)
        ret.add(elem)
        if(unlock):
            for item in unlock:
                ret.add(item)
    
    if(is_valid(ret)):
        if(flag):
            print(f"LOCKTABLE:\n{Twolock.locktable}\n")
            print(f"Any T in growing phase?\n{Twolock.phase}\n")
            print(ret, "\n")
        return ret
    else:return False

# check if a lock schedule is legal before outputting it
def is_valid(S):
    l = []
    for elem in S.transactions:
        if(elem.oper == "L"):
            l.append(elem.trans[1]+elem.var)
        elif(elem.oper == "U"):
            l.remove(elem.trans[1]+elem.var)
    if(l == []):
        return True
    else:
        return False

# Function to get a view-equivalent schedule, it's a brute force algorithm that generates
# all the permutations of the Ti, i.e. if there are three transactions, [T1, T2, T3], it will
# generate all the permutations of 1,2,3. That's the heavy part, but after that, the permutations
# have to pass a check given from the writeset, final-write and read-from
def brute_force(S, R, F, O):
    # easiest way is to swap Ti until we find a view-eq schedule
    def recurr(aux):
        nonlocal found
        if found: return
        if check(aux):
            found = True
            return True
        else:
            return None

    def check(aux):
        if(get_view(aux)[:2] == [R, F]):
            return True
        else:
            return False


    
    found = False
    aux = build_serial(S,O,R)
    ret = None
    if(aux):
        for item in aux:
            if(recurr(item)):
                ret=item
                break
    
    return ret if found else None
    
# computes READS-FROM and FINAL-WRITE on one cycle
def get_view(S):
    final_write = {} # dict[var] = Transaction
    reads_from = {} # dict[trans] = [trans]

    write_set = {}
    write_order = {} #useful for topological order 
    for i in range(len(S)):
        curr = S.transactions[i]
        #write case
        if curr.oper == "W":
            if curr.var in final_write:
                write_order[curr.var].append(curr.get_int())
            final_write[curr.var] = curr
            write_set[curr.var] = curr
            if not curr.var in write_order:
                write_order[curr.var] = [curr.get_int()]
        
        # read case
        else:
            if curr.var in write_set:
                reads_from[curr] = write_set[curr.var]

    return [reads_from, final_write, write_order]


#Only way is to bruteforce, not suitable for big inputs
def check_view(S, flag=False):
    reads_from, final_write, write_order = get_view(S)

    if(flag):
        print("FINAL-WRITE:",print_view(final_write, "FW"))
        print("READS-FROM:", print_view(reads_from, "RF"), end="\n\n")

    return brute_force(S, reads_from, final_write, write_order)

