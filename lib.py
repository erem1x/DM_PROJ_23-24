# SET OF AUX FUNCTIONS

# Format function
# W1(A) -> "T1", "W", "A"
def write_schedule(S):
    S = S.upper()
    l = S.split()
    ret=[]
    for elem in l:
        ret.append(["T"+elem[1], elem[0], elem[3]])
    return ret



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
    
    



class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'