def move(state, source, destination):
    if(len(state) <= source or len(state) <= destination or
            source < 0 or destination < 0 or source == destination or
            state[source] == False or state[destination] == True):
        raise Exception("move failed for state = " + str(state) +
            " source = " + str(source) + ", destination = " +
            str(destination))
    newstate = state[:]
    newstate[source] = False
    newstate[destination] = True
    return newstate

def get_end_points(state):
    def lend(state):
        for i in range(len(state)):
            if(state[i] == True):
                return i
        raise Exception("left end not found in state " + str(state) + ".")
    def rend(state):
        for i in range(len(state) - 1, -1, -1):
            if(state[i] == True):
                return i
        raise Exception("right end not found! in state " + str(state) + ".")
    return (lend(state), rend(state))

def find_gaps(state):
    lend, rend = get_end_points(state)
    def find_next_gap(state, start):
        i = start
        is_gap = False
        p1 = -1
        while(i <= rend):
            if(is_gap == True):
                if(state[i] == True):
                    return (p1, i - 1)
            else:
                if(state[i] == False):
                    p1 = i
                    is_gap = True
            i += 1
        raise Exception("right end not found")

    gaps = []
    while(True):
        if(gaps == []):
            start = lend
        else:
            start = gaps[-1][1] + 1
        try:
            gap = find_next_gap(state, start)
            gaps.append(gap)
        except Exception as e:
            break

    return gaps

def is_contiguous(state):
    return find_gaps(state) == []

def find_next_states(state):
    if(is_contiguous(state) == True):
        next_states = []
    else:
        sds = [] # source-destination list
        gaps = find_gaps(state)
        lend, rend = get_end_points(state)
        for gap in gaps:
            sds.append((lend, gap[0]))
            sds.append((lend, gap[1]))
            sds.append((rend, gap[0]))
            sds.append((lend, gap[1]))
        next_states = [ move(state, src, dest) for src, dest in sds]
    return next_states

class MyTable:
    def __init__(self):
        self.table = {}

    def get(self, k):
        if(not str(k) in self.table):
            return None
        return self.table[str(k)]

    def put(self, k, v):
        self.table[str(k)] = v

def min_cost(state):
    table = MyTable()
    min_cost = len(state) # the number of moves is definitely less than
        # the number of slots. Hence a safe initial value.
    def min_aux(state):
        if(table.get(state) == None):
            if(is_contiguous(state)):
                table.put(state, 0)
            else:
                next_states = find_next_states(state)
                next_mins = [min_aux(next_state) for next_state in next_states]
                table.put(state, 1 + min(next_mins))
        return table.get(state)
    return min_aux(state)
        
def t_move_1():
    s1 = [True, False, True]
    src = 2
    dest = 1
    print(move(s1, src, dest))

def t_move_2():
    try:
        s1 = [True, False, True]
        src = 1
        dest = 2
        print(move(s1, src, dest))
    except Exception as e:
        print(e)

def t_find_gaps():
    print(find_gaps([True, False, False, True]))
    print(find_gaps([True, False, False, True, False, False, False, True]))
    print(find_gaps([True, False, False, True, False, False, False]))
    print(find_gaps([False, False, False, True, False, False, False]))
    print(find_gaps([False, False, False, True, False, False, False, True]))

def t_get_end_points():
    print(get_end_points([True, True, True]))
    print(get_end_points([False, True, True]))
    print(get_end_points([True, True, False]))
    print(get_end_points([False, True, False]))

def t_min():
    print(min_cost([True, False, False, True]))
    print(min_cost([True, False, False, True, False, False, False, True]))
    print(min_cost([True, False, False, True, False, False, False]))
    print(min_cost([False, False, False, True, False, False, False]))
    print(min_cost([False, False, False, True, False, False, False, True]))


if __name__ == "__main__":
    #t_move_1()
    #t_move_2()
    #t_get_end_points()
    #t_find_gaps()
    t_min()
