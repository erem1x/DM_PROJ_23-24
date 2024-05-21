from itertools import permutations

# classes to make things easier
class Transaction:
    def __init__(self, trans, oper, var):
        self.trans = trans.upper()
        self.oper = oper.upper()
        self.var = var.upper()


    def __str__(self):
        if(self.oper == "L"):
            return f"{bcolors.FAIL}{self.oper}{self.trans[1]}({self.var}){bcolors.ENDC}"
        elif(self.oper == "U"):
            return f"{bcolors.OKGREEN}{self.oper}{self.trans[1]}({self.var}){bcolors.ENDC}"
        else:
            return f"{self.oper}{self.trans[1]}({self.var})"


    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        if isinstance(other, Transaction):
            return self.trans == other.trans and self.oper == other.oper and self.var == other.var
        return False


    def __hash__(self):
        return hash((self.trans, self.var, self.oper))


    # returns the integer of the transaction i
    def get_int(self):
        return int(self.trans[1])


# For semplicity, the class keeps stored the list of variables used 
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
    
    # Returns the indexes range between the actions of the same T but different var, 
    # where, betweem them, there is an action from a different T but with the same var of
    # the first action. i.e. W1(X) W2(X) R1(Y), so T1 needs to anticipate the lock on Y
    # (USED FOR 2PL CHECKING)
    # Cycles just once per T since the lock anticipations are registered 
    def index_range(self, item):
        if not(isinstance(item, Transaction)):
            return False
        else:
            init = self.transactions.index(item)
            ret = [init]
            for elem in self.transactions[init+1:]:
                if elem.get_int() == item.get_int() and elem.var != item.var:
                     ret.append(self.transactions.index(elem))
        if len(ret) < 1:
            return False
        return ret


    def __len__(self):
        return len(self.transactions)


    # sort the schedule according to a given Ti order
    def sort(self, order):
        ret = Schedule()
        for elem in order:
            for item in self.transactions:
                if(item.get_int() == elem):
                    ret.add(item)
        return ret


    # returns a dictionary of the schedule where the actions are associated to the common variable
    def get_sorted(self):
        ret = {}
        for elem in self.transactions:
            if not elem.var in ret:
                ret[elem.var] = [elem]
            else:
                ret[elem.var].append(elem)
        return ret


    def __repr__(self):
        return ', '.join(map(repr, self.transactions))


# Contains the locktable and keeps track of the transactions' phase (growing or shrinking) 
# and a list of "future" operations that require attention
# If a future operation has been already granted an anticipated lock, it gets deleted from that list
class TwoPL:
    def __init__(self, S):
        self.schedule = S
        self.locktable = {}
        self.operations = S.get_sorted() # actions for each variable
        self.phase = {} # growing or shrinking
        for elem in S.transactions:
            if elem.get_int() not in self.phase:
                # initially set all the T's to be in growing phase
                self.phase[elem.get_int()] = True 
            
            # initialize locktable 
            if elem.var not in self.locktable:
                self.locktable[elem.var] = None

    
    # lock function (checks for anticipated locks too)
    # returns a list of locks
    def lock(self, elem, flag=False):
        var = elem.var
        # check if T has already locked var
        if self.locktable[var] != None:
            if self.locktable[var] == elem.get_int():
                return False
            else:
                raise SystemError(f"{elem} cannot lock {var} because already locked by T{self.locktable[var]}")
                    
        else:
             # check if T in shrinking phase
            if(self.phase[elem.get_int()] == False):
                raise SystemError(f"T{elem.get_int()} is in shrinking mode, {elem} cannot lock {var}")
            
            # can lock
            ret = []
            self.locktable[var] = elem.get_int()
            ret.append(Transaction(elem.trans, "L", var))


            # can't recurse if the lock has already been anticipated
            if elem not in self.operations[elem.var]:
                return ret

            # now checks if it needs to anticipate some other lock
            check = self.check_lock(elem)
            if(check):
                for item in check:
                    ret.append(item)
            return ret


    # unlock function, checks if and how many unlocks to perform
    def unlock(self, elem):
        int_t = elem.get_int()
        # Remove item from operations list
        if elem in self.operations[elem.var]:
            self.operations[elem.var].remove(elem)

        # check if there are other operations later
        for values in self.operations.values():
            for i in values:
                if int_t == i.get_int():
                    return False # can't unlock yet

        # change phase to shrinking
        if(self.phase[int_t] == True):
            self.phase[elem.get_int()] = False
        
        # Release all var locked by this T
        ret=self.release(elem)    
        return ret
    

    # aux function used to effectively unlock the locks
    def release(self, elem):
        # just to clean up the code a bit
        def free(key):
            self.locktable[key] = None
            ret.append(Transaction(elem.trans, "U", key))

        trans = elem.get_int()
        ret = []
        remaining = self.schedule.transactions[self.schedule.transactions.index(elem)+1:]

        # checks for every variable if the current transaction has the lock, proceed to unlock it 
        # if it is no longer needed 
        for key, values in self.locktable.items():
            if(values == trans):                
                if(len(remaining) < 1):
                    free(key)
                else:
                    flag=True
                    for item in remaining:
                        if(values == item.get_int() and key == item.var):
                            flag=False
                        if(key == item.var and values != item.get_int() and self.locktable[key] != None and flag):
                            free(key)
                    if(flag and self.locktable[key] != None):
                        free(key)

        return ret


    # aux function used to check if some locks need to be anticipated before entering the shrinking phase
    # It gets a tuple of indexes of future actions by the same T
    def check_lock(self, elem):
        tup = self.schedule.index_range(elem) # at least two items, current action and future actions
        if not tup: 
            return False # no future actions

        flag = False
        # Now checking all the other operations under the same T to check if they need the lock now
        # If flag set to True, T has to unlock so it will lock for all its actions that need it :
        init=tup[0]
        final=tup[-1]
        ret = []
        for i in range(init+1, final):
            item = self.schedule.transactions[i]
            if(item.var == elem.var):
                flag = True
                break
        if(flag):
            for item in tup[1:]:
                new = self.schedule.transactions[item]
                self.operations[new.var].remove(new)
                try:
                    lock = self.lock(new)
                    if(not lock):
                        continue
                    ret.extend(lock)
                except SystemError:
                    return False
        
        return ret


    def __repr__(self):
        return f"{self.locktable}\n"



# Build the precedence graph
def precedence_graph(S, flag=False):
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
    
    if(flag):
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
