from itertools import permutations

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
    
    def get_int(self):
        return int(self.trans[1])

class Schedule:
    def __init__(self):
        self.transactions = []
        self.var = []
        self.trans = []

    def add(self, item):
        if(isinstance(item, Transaction)):
            self.transactions.append(item)
            if item.var not in self.var:
                self.var.append(item.var)
            if item.get_int() not in self.trans:
                self.trans.append(item.get_int())
    
    def swap(self, ind1, ind2):
        try:
            self.transactions[ind1], self.transactions[ind2] = self.transactions[ind2], self.transactions[ind1]
        except:
            print("Error swapping")

    def __len__(self):
        return len(self.transactions)
    
    def sort(self, order):
        ret = Schedule()
        for elem in order:
            for item in self.transactions:
                if(item.get_int() == elem):
                    ret.add(item)
        return ret

    def __repr__(self):
        return ', '.join(map(repr, self.transactions))


# Build the precedence graph
def precedence_graph(S):
    nodes = []
    edges = {}
    
    for i in range(len(S)):
        curr = S.transactions[i]
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
            old = S.transactions[j]
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


# print final-write and reads-from
def print_view(ret, flag):
    if(flag=="FW"):
        output ="<"
        for key, value in ret.items():
            output+=f"w{value.get_int()}({key}) "
        output = output[:-1]+">"

    else:
        output = ""
        for key, value in ret.items():
            output+="<"
            output+=(f"r{key.get_int()}({key.var}), w{value.get_int()}({key.var}) ")
            output = output[:-1]+"> "
        
    
    return output

# sort schedule in topological order following constraints
# O stores the order of writes, i.e. final-write for X is W1 but there is also W2(X)
# in the schedule, so W1(X) must come before W2(X)
# R is the read-from set. In any case, each possible schedule gets
# obviously compared to the main one to check that both the final-write
# and the read-from sets are identical
# the output is the list of all possible combinations
def build_serial(S, O, R):
    # generate all possible orders
    def gen_ord():

        # get all the constaints in a dictionary, {"Ti": ["Tj", "Tk"} means that
        # Ti must come after Tj and Tk
        def gen_constraints():
            # from the write set
            for item in O.values():
                if(len(item)>1):
                    for i in range(len(item)-1):
                        if item[-1] not in const:
                            const[item[-1]]=[]
                        if item[i] not in const[item[-1]]:
                            const[item[-1]].append(item[i])

            # from the read-from property
            for key, value in R.items():
                if key.get_int() not in const:
                    const[key.get_int()] = [value.get_int()]
                else:
                    if(value.get_int() not in const[key.get_int()]):
                        const[key.get_int()].append(value.get_int())

        # check if the permutations of T are legal according to constraints 
        def check_const(p):
            for key, values in const.items():
                for value in values:
                    const_list.append(p.index(key) > p.index(value))
            if all(const_list):
                return True
            else:
                return False
            

        const_list = []
        const = {}
        ret = []
        gen_constraints()

        # compute permutations and check them
        for p in permutations(S.trans):
            const_list.clear()
            if(check_const(p)):
                ret.append(p)
        return ret
        
    try:
        ret = gen_ord()
        if ret is None:
            return None
        ret_schedule = []

        for item in ret:
            ret_schedule.append(S.sort(item))
        return ret_schedule

    except ValueError:
        return None


# Format function
# W1(A) -> "1", "W", "A"
def write_schedule(S):
    l = S.split()
    ret = Schedule()
    for elem in l:
        ret.add(Transaction("T"+elem[1], elem[0], elem[3]))
    return ret

# colors used in terminal
class bcolors:
    OKGREEN = '\033[92m'
    OKCYAN = '\033[36m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
