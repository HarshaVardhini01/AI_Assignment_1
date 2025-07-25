class State:
    def __init__(self, config, goal):
        self.config = tuple(config)  # Store as tuple for hashability
        self.goal = tuple(goal)

    def goalTest(self):
        return self.config == self.goal

    def moveGen(self):
        children = []
        lst = list(self.config)
        idx = lst.index('_')  # find empty space

        # Left neighbor moves right into empty
        if idx > 0 and lst[idx - 1] == 'W':
            new = lst[:]
            new[idx], new[idx - 1] = new[idx - 1], new[idx]
            children.append(State(new, self.goal))

        # Left jump over 1
        if idx > 1 and lst[idx - 2] == 'W' and lst[idx - 1] in ['E', 'W']:
            new = lst[:]
            new[idx], new[idx - 2] = new[idx - 2], new[idx]
            children.append(State(new, self.goal))

        # Right neighbor moves left into empty
        if idx < 6 and lst[idx + 1] == 'E':
            new = lst[:]
            new[idx], new[idx + 1] = new[idx + 1], new[idx]
            children.append(State(new, self.goal))

        # Right jump over 1
        if idx < 5 and lst[idx + 2] == 'E' and lst[idx + 1] in ['E', 'W']:
            new = lst[:]
            new[idx], new[idx + 2] = new[idx + 2], new[idx]
            children.append(State(new, self.goal))

        return children

    def __str__(self):
        return ''.join(self.config)

    def __eq__(self, other):
        return self.config == other.config

    def __hash__(self):
        return hash(self.config)


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, _ in OPEN]
    closed_nodes = [node for node, _ in CLOSED]
    return [c for c in children if c not in open_nodes and c not in closed_nodes]

def reconstructPath(node_pair, CLOSED):
    path = []
    parent_map = {node: parent for node, parent in CLOSED}
    node, parent = node_pair
    path.append(node)
    while parent is not None:
        path.append(parent)
        parent = parent_map[parent]
    return path[::-1]

def bfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair
        if N.goalTest():
            print("BFS: Goal Found")
            path = reconstructPath(node_pair, CLOSED)
            for p in path:
                print(p)
            return
        CLOSED.append(node_pair)
        children = N.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        new_pairs = [(c, N) for c in new_nodes]
        OPEN.extend(new_pairs)
    print("BFS: No solution")

def dfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair
        if N.goalTest():
            print("DFS: Goal Found")
            path = reconstructPath(node_pair, CLOSED)
            for p in path:
                print(p)
            return
        CLOSED.append(node_pair)
        children = N.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        new_pairs = [(c, N) for c in new_nodes]
        OPEN = new_pairs + OPEN  # DFS stack behavior
    print("DFS: No solution")


# Run it
initial = ['W', 'W', 'W', '_', 'E', 'E', 'E']
goal =    ['E', 'E', 'E', '_', 'W', 'W', 'W']

start_state = State(initial, goal)

print("=== BFS ===")
bfs(start_state)

print("\n=== DFS ===")
dfs(start_state)

