from itertools import combinations

class State:
    def __init__(self, left, right, umbrella, time):
        self.left = frozenset(left)
        self.right = frozenset(right)
        self.umbrella = umbrella  # 'L' or 'R'
        self.time = time

    def goalTest(self):
        return len(self.left) == 0 and self.umbrella == 'R'

    def moveGen(self):
        times = {
            "Amogh": 5,
            "Ameya": 10,
            "Grandmother": 20,
            "Grandfather": 25
        }

        children = []

        if self.umbrella == 'L':
            # Send 2 people from left to right
            for pair in combinations(self.left, 2):
                new_left = set(self.left) - set(pair)
                new_right = set(self.right) | set(pair)
                cost = max(times[p] for p in pair)
                new_time = self.time + cost
                if new_time <= 60:
                    children.append(State(new_left, new_right, 'R', new_time))

        else:
            # Send 1 person back from right to left
            for p in self.right:
                new_left = set(self.left) | {p}
                new_right = set(self.right) - {p}
                cost = times[p]
                new_time = self.time + cost
                if new_time <= 60:
                    children.append(State(new_left, new_right, 'L', new_time))

        return children

    def __str__(self):
        return f"L:{sorted(self.left)} | R:{sorted(self.right)} | Umbrella: {self.umbrella} | Time: {self.time}"

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right and self.umbrella == other.umbrella and self.time == other.time

    def __hash__(self):
        return hash((self.left, self.right, self.umbrella, self.time))


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, _ in OPEN]
    closed_nodes = [node for node, _ in CLOSED]
    return [c for c in children if c not in open_nodes and c not in closed_nodes]

def reconstructPath(node_pair, CLOSED):
    path = []
    parent_map = {node: parent for node, parent in CLOSED}
    node, parent = node_pair
    path.append(node)
    while parent:
        path.append(parent)
        parent = parent_map.get(parent)
    return path[::-1]

def bfs(start):
    OPEN = [(start, None)]
    CLOSED = []

    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print("BFS: Goal Reached")
            path = reconstructPath(node_pair, CLOSED)
            for step in path:
                print(step)
            print(f"Total Time: {path[-1].time} minutes")
            return
        CLOSED.append(node_pair)
        children = N.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        new_pairs = [(c, N) for c in new_nodes]
        OPEN.extend(new_pairs)
    print("No solution found")

# Start the search
people = ["Amogh", "Ameya", "Grandmother", "Grandfather"]
start_state = State(left=people, right=[], umbrella='L', time=0)

bfs(start_state)

