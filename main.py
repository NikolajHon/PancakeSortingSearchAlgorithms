import random
import heapq


class Node:
    def __init__(self, state, h, cost, parent=None):
        self.state = state
        self.h = h
        self.cost = cost
        self.parent = parent

    def f(self):
        return self.cost + self.h

    def __lt__(self, other):
        return self.f() < other.f()


def largest_misplaced_stick(state):
    sorted_state = sorted(state)
    max_misplaced = 0
    for i in range(len(state)):
        if state[i] != sorted_state[i]:
            max_misplaced = max(max_misplaced, state[i])
    return max_misplaced


def gap_heuristic(state):
    gaps = 0
    for i in range(len(state) - 1):
        if abs(state[i] - state[i + 1]) != 1:
            gaps += 1
    if state[-1] != len(state):
        gaps += 1
    return gaps


def weighted_gap_heuristic(state):
    gaps = 0
    for i in range(len(state) - 1):
        if abs(state[i] - state[i + 1]) != 1:
            gaps += i + 1

    if state[-1] != len(state):
        gaps += len(state)
    return gaps


def num_of_misplaced_sticks(state):
    sorted_state = sorted(state)
    return sum(1 for i in range(len(state)) if state[i] != sorted_state[i])


def sum_of_distances(state):
    sorted_state = sorted(state)
    return sum(abs(i - state.index(sorted_state[i])) for i in range(len(state)))


def reconstruct_path(node):
    path = []
    total_cost = 0
    while node:
        path.append((node.state, node.h, node.cost))
        total_cost += node.cost
        node = node.parent
    return path[::-1], total_cost


def greedy_search(sticks, heuristic):
    start_state = sticks
    goal_state = sorted(sticks)

    open_set = []
    heapq.heappush(open_set, Node(start_state, heuristic(start_state), cost=0))

    closed_set = set()
    expanded_nodes = 0

    while open_set:
        current = heapq.heappop(open_set)



        if current.state == goal_state:
            path, total_cost = reconstruct_path(current)
            return path, total_cost, expanded_nodes
        expanded_nodes += 1
        closed_set.add(tuple(current.state))

        for i in range(1, len(current.state) + 1):
            first_part = current.state[:i]
            second_part = current.state[i:]

            reversed_first_part = first_part[::-1]

            new_state = reversed_first_part + second_part

            if tuple(new_state) in closed_set:
                continue
            flip_cost = i
            heapq.heappush(open_set, Node(new_state, heuristic(new_state), 0, parent=current))
    return None, 0, expanded_nodes


def uniform_cost_search(sticks):
    start_state = sticks
    goal_state = sorted(sticks)

    open_set = []
    heapq.heappush(open_set, Node(start_state, h=0, cost=0))

    closed_set = set()
    expanded_nodes = 0
    current_step = 0

    while open_set:
        current = heapq.heappop(open_set)
        print("Current step:", current_step, current.state)

        current_step += 1
        if current.state == goal_state:
            path, total_cost = reconstruct_path(current)
            return path, current.cost, expanded_nodes
        expanded_nodes += 1
        closed_set.add(tuple(current.state))

        for i in range(1, len(current.state) + 1):
            new_state = current.state[:i][::-1] + current.state[i:]
            if tuple(new_state) in closed_set:
                continue
            new_cost = current.cost + i
            heapq.heappush(open_set, Node(new_state, h=0, cost=new_cost, parent=current))

    return None, 0, expanded_nodes


def a_star_search(sticks, heuristic):
    start_state = sticks
    goal_state = sorted(sticks)

    open_set = []
    heapq.heappush(open_set, Node(start_state, h=heuristic(start_state), cost=0))

    closed_set = set()
    expanded_nodes = 0

    while open_set:

        for node in open_set:
            print(f"State: {node.state}, Cost: {node.cost}", "Heuristic: ", {node.h})

        current = heapq.heappop(open_set)
        print("We choose a ", current.state)
        expanded_nodes += 1

        if current.state == goal_state:
            path, total_cost = reconstruct_path(current)
            return path, current.cost, expanded_nodes
        expanded_nodes += 1
        closed_set.add(tuple(current.state))

        for i in range(1, len(current.state) + 1):
            new_state = current.state[:i][::-1] + current.state[i:]
            if tuple(new_state) in closed_set:
                continue

            new_cost = current.cost + i
            heuristic_value = heuristic(new_state)

            if heuristic_value > new_cost:
                print(f"Warning: Heuristic value {heuristic_value} exceeds real cost {new_cost} for state {new_state}")

            heapq.heappush(open_set, Node(new_state, h=heuristic_value, cost=new_cost, parent=current))

    return None, 0, expanded_nodes



if __name__ == "__main__":
    num_sticks = int(input("Enter the number of sticks: "))

    sticks = list(range(1, num_sticks + 1))
    random.shuffle(sticks)


    print("\nStarting configuration:", sticks)
    print("\nUniform Cost Search (UCS):")
    solution_ucs, total_cost_ucs, expanded_nodes_ucs = uniform_cost_search(sticks)
    for i, (step, h, c) in enumerate(solution_ucs, 1):
        print(f"Step {i}: {step}, Cost: {c}")
    print(f"Total Cost: {total_cost_ucs}")
    print(f"Total Expanded Nodes: {expanded_nodes_ucs}\n")

    print("\nA* Search (Heuristic: Largest misplaced stick):")
    solution_astar_1, total_cost_astar_1, expanded_nodes_astar_1 = a_star_search(sticks,
                                                                                 heuristic=largest_misplaced_stick)
    for i, (step, h, c) in enumerate(solution_astar_1, 1):
        print(f"Step {i}: {step}, Cost: {c}, Heuristic: {h}")
    print(f"Total Cost: {total_cost_astar_1}")
    print(f"Total Expanded Nodes: {expanded_nodes_astar_1}\n")

    print("A* Search (Heuristic: Sum of distances to the goal):")
    solution_astar_2, total_cost_astar_2, expanded_nodes_astar_2 = a_star_search(sticks, heuristic=sum_of_distances)
    for i, (step, h, c) in enumerate(solution_astar_2, 1):
        print(f"Step {i}: {step}, Cost: {c}, Heuristic: {h}")
    print(f"Total Cost: {total_cost_astar_2}")
    print(f"Total Expanded Nodes: {expanded_nodes_astar_2}\n")

    print("A* Search (Heuristic: Gap Heuristic):")
    solution_astar_3, total_cost_astar_3, expanded_nodes_astar_3 = a_star_search(sticks, heuristic=gap_heuristic)
    for i, (step, h, c) in enumerate(solution_astar_3, 1):
        print(f"Step {i}: {step}, Cost: {c}, Heuristic: {h}")
    print(f"Total Cost: {total_cost_astar_3}")
    print(f"Total Expanded Nodes: {expanded_nodes_astar_3}\n")

    print("A* Search (Heuristic: Weighted Gap Heuristic):")
    solution_astar_4, total_cost_astar_4, expanded_nodes_astar_4 = a_star_search(sticks,
                                                                                 heuristic=weighted_gap_heuristic)
    for i, (step, h, c) in enumerate(solution_astar_4, 1):
        print(f"Step {i}: {step}, Cost: {c}, Heuristic: {h}")
    print(f"Total Cost: {total_cost_astar_4}")
    print(f"Total Expanded Nodes: {expanded_nodes_astar_4}\n")

    # Greedy Search
    print("\nGreedy Search (Heuristic: Largest misplaced stick):")
    solution_greedy_1, total_cost_greedy_1, expanded_nodes_greedy_1 = greedy_search(sticks,
                                                                                    heuristic=largest_misplaced_stick)
    for i, (step, h, c) in enumerate(solution_greedy_1, 1):
        print(f"Step {i}: {step}, Cost: {c}, Heuristic: {h}")
    print(f"Total Cost: {total_cost_greedy_1}")
    print(f"Total Expanded Nodes: {expanded_nodes_greedy_1}\n")

    print("Greedy Search (Heuristic: Sum of distances to the goal):")
    solution_greedy_2, total_cost_greedy_2, expanded_nodes_greedy_2 = greedy_search(sticks, heuristic=sum_of_distances)
    for i, (step, h, c) in enumerate(solution_greedy_2, 1):
        print(f"Step {i}: {step}, Cost: {c}, Heuristic: {h}")
    print(f"Total Cost: {total_cost_greedy_2}")
    print(f"Total Expanded Nodes: {expanded_nodes_greedy_2}\n")

    print("Greedy Search (Heuristic: Gap Heuristic):")
    solution_greedy_3, total_cost_greedy_3, expanded_nodes_greedy_3 = greedy_search(sticks, heuristic=gap_heuristic)
    for i, (step, h, c) in enumerate(solution_greedy_3, 1):
        print(f"Step {i}: {step}, Cost: {c}, Heuristic: {h}")
    print(f"Total Cost: {total_cost_greedy_3}")
    print(f"Total Expanded Nodes: {expanded_nodes_greedy_3}\n")

    print("Greedy Search (Heuristic: Weighted Gap Heuristic):")
    solution_greedy_4, total_cost_greedy_4, expanded_nodes_greedy_4 = greedy_search(sticks,
                                                                                    heuristic=weighted_gap_heuristic)
    for i, (step, h, c) in enumerate(solution_greedy_4, 1):
        print(f"Step {i}: {step}, Cost: {c}, Heuristic: {h}")
    print(f"Total Cost: {total_cost_greedy_4}")
    print(f"Total Expanded Nodes: {expanded_nodes_greedy_4}\n")

    print("\nCup Metrics")

    search_methods = {
        "Uniform Cost Search (UCS)": (total_cost_ucs, expanded_nodes_ucs),
        "A* Search (Heuristic: Largest misplaced stick)": (total_cost_astar_1, expanded_nodes_astar_1),
        "A* Search (Heuristic: Sum of distances to the goal)": (total_cost_astar_2, expanded_nodes_astar_2),
        "A* Search (Heuristic: Gap Heuristic)": (total_cost_astar_3, expanded_nodes_astar_3),
        "A* Search (Heuristic: Weighted Gap Heuristic)": (total_cost_astar_4, expanded_nodes_astar_4),
        "Greedy Search (Heuristic: Largest misplaced stick)": (total_cost_greedy_1, expanded_nodes_greedy_1),
        "Greedy Search (Heuristic: Sum of distances to the goal)": (total_cost_greedy_2, expanded_nodes_greedy_2),
        "Greedy Search (Heuristic: Gap Heuristic)": (total_cost_greedy_3, expanded_nodes_greedy_3),
        "Greedy Search (Heuristic: Weighted Gap Heuristic)": (total_cost_greedy_4, expanded_nodes_greedy_4),
    }

    comparison_pairs = [
        ("Uniform Cost Search (UCS)", "A* Search (Heuristic: Largest misplaced stick)"),
        ("Uniform Cost Search (UCS)", "A* Search (Heuristic: Sum of distances to the goal)"),
        ("Uniform Cost Search (UCS)", "A* Search (Heuristic: Gap Heuristic)"),
        ("Uniform Cost Search (UCS)", "A* Search (Heuristic: Weighted Gap Heuristic)"),
        ("Greedy Search (Heuristic: Largest misplaced stick)", "A* Search (Heuristic: Largest misplaced stick)"),
        ("Greedy Search (Heuristic: Sum of distances to the goal)", "A* Search (Heuristic: Largest misplaced stick)"),
        ("Greedy Search (Heuristic: Gap Heuristic)", "A* Search (Heuristic: Largest misplaced stick)"),
        ("Greedy Search (Heuristic: Weighted Gap Heuristic)", "A* Search (Heuristic: Largest misplaced stick)"),
        ("Greedy Search (Heuristic: Largest misplaced stick)", "A* Search (Heuristic: Sum of distances to the goal)"),
        ("Greedy Search (Heuristic: Sum of distances to the goal)",
         "A* Search (Heuristic: Sum of distances to the goal)"),
        ("Greedy Search (Heuristic: Gap Heuristic)", "A* Search (Heuristic: Sum of distances to the goal)"),
        ("Greedy Search (Heuristic: Weighted Gap Heuristic)", "A* Search (Heuristic: Sum of distances to the goal)"),
        ("Greedy Search (Heuristic: Largest misplaced stick)", "A* Search (Heuristic: Gap Heuristic)"),
        ("Greedy Search (Heuristic: Sum of distances to the goal)", "A* Search (Heuristic: Gap Heuristic)"),
        ("Greedy Search (Heuristic: Gap Heuristic)", "A* Search (Heuristic: Gap Heuristic)"),
        ("Greedy Search (Heuristic: Weighted Gap Heuristic)", "A* Search (Heuristic: Gap Heuristic)"),
        ("Greedy Search (Heuristic: Largest misplaced stick)", "A* Search (Heuristic: Weighted Gap Heuristic)"),
        ("Greedy Search (Heuristic: Sum of distances to the goal)", "A* Search (Heuristic: Weighted Gap Heuristic)"),
        ("Greedy Search (Heuristic: Gap Heuristic)", "A* Search (Heuristic: Weighted Gap Heuristic)"),
        ("Greedy Search (Heuristic: Weighted Gap Heuristic)", "A* Search (Heuristic: Weighted Gap Heuristic)"),
    ]

    print("\nCup Metrics")
    for method1, method2 in comparison_pairs:
        cost1, expanded1 = search_methods[method1]
        cost2, expanded2 = search_methods[method2]
        cost_ratio = cost1 / cost2
        expanded_ratio = expanded1 / expanded2
        print(
            f"{method1} VS {method2} - price ratio is {cost_ratio:.2f} and ratio of Expanded Nodes is {expanded_ratio:.2f}"
        )
