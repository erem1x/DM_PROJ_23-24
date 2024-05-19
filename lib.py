from aux import *
# SET OF AUX FUNCTIONS

def main_fun(S):
    # summary
    twoPL = False 
    conf_ser = False
    view_ser = False

    print(f"{bcolors.ITALIC}Checking conflict-serializability...{bcolors.ENDC}", end="\n\n")
    nodes, edges = precedence_graph(S)
    if not check_cycle(nodes, edges):
        print(f"{bcolors.OKGREEN}Schedule is conflict-serializable!{bcolors.ENDC}")
        conf_ser = True
        view_ser = True
        print(f"\n{bcolors.ITALIC}Checking if it belongs to the 2PL class...{bcolors.ENDC}", end="\n\n")
        twoPL = check_2PL(S)
        if(twoPL):
            print(f"\n{bcolors.OKGREEN}Schedule is in 2PL class!{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Schedule is not in 2PL class!{bcolors.ENDC}")

    
    else:
        print(f"{bcolors.FAIL}Schedule is not conflict-serializable!{bcolors.ENDC}\n")
        conf_ser = False
        print(f"{bcolors.ITALIC}Checking view-serializability...{bcolors.ENDC}", end="\n\n")

        ret = check_view(S)
        if(ret is not None):
            view_ser = True
            print(f"Here is a view-equivalent schedule:")
            print("["+', '.join(['T' + str(num) for num in ret.trans])+"]\n", bcolors.BOLD)
            print(ret, f"{bcolors.ENDC}\n")
            print(f"{bcolors.OKGREEN}Schedule is view-serializable!{bcolors.ENDC}")

        else:
            print(f"{bcolors.FAIL}Schedule is not view-serializable!{bcolors.ENDC}")


# Function to assign locks and unlocks
# Most of the work is in the TwoPL class itself
def check_2PL(S):
    Twolock = TwoPL(S)
    ret = Schedule()
    for elem in S.transactions:
        lock = Twolock.lock(elem)
        if(lock == "ERROR"):
            return False
        elif(lock):
            for item in lock:
                ret.add(item)
        
        unlock = Twolock.unlock(elem)
        ret.add(elem)
        if(unlock):
            for item in unlock:
                ret.add(item)
    
    print(ret)
    return ret


# Function to get a view-equivalent schedule
def brute_force(S, R, F, O):
    # easiest way is to swap items until we find a view-eq schedule
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
    
# compute READS-FROM and FINAL-WRITE on one cycle
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
def check_view(S):
    reads_from, final_write, write_order = get_view(S)

    print("FINAL-WRITE:",print_view(final_write, "FW"))
    print("READS-FROM:", print_view(reads_from, "RF"), end="\n\n")

    return brute_force(S, reads_from, final_write, write_order)