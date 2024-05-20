from aux import *
# SET OF AUX FUNCTIONS

def main_fun(S, flag):
    print(f"{bcolors.ITALIC}Checking conflict-serializability...{bcolors.ENDC}", end="\n\n")
    nodes, edges = precedence_graph(S, flag)
    if not check_cycle(nodes, edges):
        print(f"{bcolors.OKGREEN}Schedule is conflict-serializable!{bcolors.ENDC}")
        conf_ser = True
        view_ser = True
        print(f"\n{bcolors.ITALIC}Checking if it belongs to the 2PL class...{bcolors.ENDC}", end="\n\n")
        twoPL = check_2PL(S, flag)
        if(isinstance(twoPL, Schedule)):
            print(f"\n{bcolors.OKGREEN}Schedule is in 2PL class!{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}{twoPL}{bcolors.ENDC}")

    
    else:
        print(f"{bcolors.FAIL}Schedule is not conflict-serializable!{bcolors.ENDC}\n")
        conf_ser = False
        print(f"{bcolors.ITALIC}Checking view-serializability...{bcolors.ENDC}", end="\n\n")

        ret = check_view(S, flag)
        if(ret is not None):
            view_ser = True
            print(f"Here is a view-equivalent schedule:")
            print("["+', '.join(['T' + str(num) for num in ret.trans])+"]\n", bcolors.BOLD)
            print(ret, f"{bcolors.ENDC}\n")
            print(f"{bcolors.OKGREEN}Schedule is view-serializable!{bcolors.ENDC}")

        else:
            print(f"{bcolors.FAIL}Schedule is not view-serializable, couldn't find a view-equivalent serial schedule!{bcolors.ENDC}")


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
                return f"{ret}\n{Twolock.locktable}\nSchedule not in 2PL: {e}"
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


# check if a lock schedule is legal
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
        print(l)
        return False


# Function to get a view-equivalent schedule
def brute_force(S, R, F, O):
    # easiest way is to swap until we find a view-eq schedule
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
def check_view(S, flag=False):
    reads_from, final_write, write_order = get_view(S)

    if(flag):
        print("FINAL-WRITE:",print_view(final_write, "FW"))
        print("READS-FROM:", print_view(reads_from, "RF"), end="\n\n")

    return brute_force(S, reads_from, final_write, write_order)

