# SET OF AUX FUNCTIONS

# Build the precedence graph
def precedence_graph(S):
    nodes = []
    edges = {}
    
    for i in range(len(S)):
        trans, oper, var = S[i]
        # set nodes in nodes list
        if(trans) not in nodes:
            nodes.append(trans)

        # memorizing the conflicts here
        if(trans not in edges):
            edges[trans] = []
        
        # nested cycle to check previous transactions
        for j in range(i):
            old_trans, old_oper, old_var = S[j]
            
            #if conflict
            if(old_var == var and (old_oper == "W" or oper == "W") and trans!=old_trans):
                if trans not in edges[old_trans]:
                    edges[old_trans].append(trans)
    
    print_graph(nodes, edges)
    if not check_cycle(nodes, edges):
        print(f"{bcolors.OKGREEN}Schedule is conflict-serialisable!{bcolors.ENDC}")
        return True
    
    else:
        print(f"{bcolors.FAIL}Schedule is not conflict-serialisable!{bcolors.ENDC}")
        return False


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
            return True
    
    return False
    

# Only way is to bruteforce, not suitable for big inputs
def check_view(S):
    reads_from = get_view(S)[0]
    final_write = get_view(S)[1]
    print("FINAL-WRITE:",print_view(final_write, "FW"))
    print("READS-FROM:", print_view(reads_from, "RF"))

    return False


# compute READS-FROM and LAST-WRITE on one cycle
def get_view(S):
    LAST_WRITE = {}
    READS_FROM = []

    write_set = {}
    for i in range(len(S)):
        trans, oper, var = S[i]
        if oper == "W":
            LAST_WRITE[var] = trans
            write_set[var] = trans
        
        else:
            if var in write_set:
                READS_FROM.append([var, trans, write_set[var]])

    return [READS_FROM, LAST_WRITE]

# print final-write and reads-from
def print_view(ret, flag):
    if(flag=="FW"):
        output ="<"
        for key, value in ret.items():
            output+=f"w{value[1]}({key}) "
        output = output[:-1]+">"

    else:
        output = ""
        for elem in ret:
            output+="<"
            output+=(f"r{elem[1][1]}({elem[0]}), w{elem[2][1]}({elem[0]}) ")
            output = output[:-1]+"> "
        
    
    return output

# Format function
# W1(A) -> "T1", "W", "A"
def write_schedule(S):
    S = S.upper()
    l = S.split()
    ret=[]
    for elem in l:
        ret.append(["T"+elem[1], elem[0], elem[3]])
    return ret

# colors used in terminal
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'