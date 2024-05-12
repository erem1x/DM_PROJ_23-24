# SET OF AUX FUNCTIONS

# class of transaction to make things easier
class Transaction:
    def __init__(self, trans, oper, var):
        self.trans = trans.upper()
        self.oper = oper.upper()
        self.var = var.upper()

    def __str__(self):
        return f"{self.oper}{self.trans[1]}({self.var})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, Transaction):
            return self.trans == other.trans and self.oper == other.oper and self.var == other.var
        return False
    
    def __hash__(self):
        return hash((self.trans, self.var, self.oper))

def main_fun(S):
    # summary
    twoPL = False 
    conf_ser = False
    view_ser = False

    print(f"{bcolors.ITALIC}Checking conflict-serialisability...{bcolors.ENDC}", end="\n\n")
    nodes, edges = precedence_graph(S)
    if not check_cycle(nodes, edges):
        print(f"{bcolors.OKGREEN}Schedule is conflict-serialisable!{bcolors.ENDC}")
        conf_ser = True
        view_ser = True
    
    else:
        print(f"{bcolors.FAIL}Schedule is not conflict-serialisable!{bcolors.ENDC}\n")
        conf_ser = False
        print(f"{bcolors.ITALIC}Checking view-serialisability...{bcolors.ENDC}", end="\n\n")

        ret = check_view(S)
        if(ret is not None):
            view_ser = True
            print(f"Here is a view-equivalent schedule:\n{bcolors.BOLD}")
            print(*ret, f"{bcolors.ENDC}\n")
            print(f"{bcolors.OKGREEN}Schedule is view-serialisable!{bcolors.ENDC}")

        else:
            print(f"{bcolors.FAIL}Schedule is not view-serialisable!{bcolors.ENDC}")

# Build the precedence graph
def precedence_graph(S):
    nodes = []
    edges = {}
    
    for i in range(len(S)):
        curr = S[i]
        trans = curr.trans
        oper = curr.oper
        var = curr.var
        # set nodes in nodes list
        if(trans) not in nodes:
            nodes.append(trans)

        # memorizing the conflicts here
        if(trans not in edges):
            edges[trans] = []
        
        # nested cycle to check previous transactions
        for j in range(i):
            old = S[j]
            old_trans = old.trans 
            old_oper = old.oper
            old_var = old.var
            
            #if conflict
            if(old_var == var and (old_oper == "W" or oper == "W") and trans!=old_trans):
                if trans not in edges[old_trans]:
                    edges[old_trans].append(trans)
    
    print_graph(nodes, edges)

    return [nodes, edges]

# Print the graph
def print_graph(nodes, edges):
    print("PRECEDENCE GRAPH:")
    nodes = sorted(nodes, key=lambda x: int(x[1:]))
    for node in nodes:
        if node in edges:
            print(node + " ->", ", ".join(edges[node]))
        else:
            print(node + " ->")
    print("")
    

# Check whether the graph has a cycle (dfs)
def check_cycle(nodes, edges):
    visited = set()
    path = set()

    def dfs(node):
        if(node in path):
            return True
        if(node in visited):
            return False
        
        visited.add(node)
        path.add(node)

        for elem in edges[node]:
            if(elem in path):
                return True
            else: 
                if(dfs(elem)):
                    return True
        
        path.remove(node)
        return False
    
    
    for elem in nodes:
        if(dfs(elem)):
            print("CYCLE FOUND!\n")
            return True
    print("CYCLE NOT FOUND!")
    return False
    

# Only way is to bruteforce, not suitable for big inputs
def check_view(S):
    reads_from, final_write, write_order = get_view(S)

    print("FINAL-WRITE:",print_view(final_write, "FW"))
    print("READS-FROM:", print_view(reads_from, "RF"), end="\n\n")

    return brute_force(S, reads_from, final_write, write_order)


# Function to get a view-equivalent schedule
def brute_force(S, R, F, O):
    # easiest way is to swap items until we find a view-eq schedule
    def recurr(aux):
        nonlocal found
        if found: return
        if check(aux):
            found = True
            ret.extend(aux)
        else:
            return None

    def check(aux):
        if(get_view(aux)[:2] == [R, F]):
            return True
        else: return False


    
    found = False
    ret = []
    recurr(build_serial(S, O))
    
    return ret if found else None
    
# compute READS-FROM and FINAL-WRITE on one cycle
def get_view(S):
    final_write = {} # dict[var] = Transaction
    reads_from = {} # dict[trans] = [trans]

    write_set = {}
    write_order = {} #useful for topological order 
    
    for i in range(len(S)):
        curr = S[i]
        #write case
        if curr.oper == "W":
            if curr.var in final_write:
                write_order[curr.var].append(int(curr.trans[1]))
            final_write[curr.var] = curr
            write_set[curr.var] = curr
            if not curr.var in write_order:
                write_order[curr.var] = [int(curr.trans[1])]
        
        # read case
        else:
            if curr.var in write_set:
                reads_from[curr] = write_set[curr.var]

    return [reads_from, final_write, write_order]

# print final-write and reads-from
def print_view(ret, flag):
    if(flag=="FW"):
        output ="<"
        for key, value in ret.items():
            output+=f"w{value.trans[1]}({key}) "
        output = output[:-1]+">"

    else:
        output = ""
        for key, value in ret.items():
            output+="<"
            output+=(f"r{key.trans[1]}({key.var}), w{value.trans[1]}({key.var}) ")
            output = output[:-1]+"> "
        
    
    return output


# sort schedule in topological order following constraints
def build_serial(S, O):
    # sorting function based on last write
    def custom_sort(x):
        for key in list(O.keys())[::-1]:
            if x in O[key]:
                return (list(O.keys())[::-1].index(key), O[key].index(x))
    
    # sort schedule by newly built order
    def order_by_trans(l):
        aux = S
        ret = []
        for elem in l:
            for item in aux:
                if int(item.trans[1]) == elem:
                    ret.append(item)
        
        if len(ret)==len(S):
            return ret
        
        else: return None


    all_trans = []
    for sublist in O.values():
        all_trans.extend(sublist)
    try:
        sorted_order = sorted(all_trans, key=lambda x: custom_sort(x))
        unique_numbers = []
        seen = set()
        for num in sorted_order:
            if num not in seen:
                unique_numbers.append(num)
                seen.add(num)
                
        return order_by_trans(unique_numbers)

    except ValueError:
        return None
    

# Format function
# W1(A) -> "T1", "W", "A"
def write_schedule(S):
    l = S.split()
    ret=[]
    for elem in l:
        ret.append(Transaction("T"+elem[1], elem[0], elem[3]))
    return ret

# colors used in terminal
class bcolors:
    OKGREEN = '\033[92m'
    OKCYAN = '\033[36m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'