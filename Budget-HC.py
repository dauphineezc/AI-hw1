import random


# an Item has a name, value, and cost
class Item:
    def __init__(self, name, value, cost):
        self.name = name
        self.value = value
        self.cost = cost


# a State is a state containing a list of items, the total value, and the total cost
class State:
    def __init__(self, items=[], total_value=0, total_cost=0, error=0):
        self.items = items
        self.total_value = total_value
        self.total_cost = total_cost
        self.error = error
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def calculate_error(self, file_info):
        self.error = max((self.total_cost - file_info["budget"]), 0) + max((file_info["target"] - self.total_value), 0)


def read_file(file_path):
    # create dictionary with target value, budget, output type, # of random restarts, and a list of items
    file_info = {
        "target": 0,
        "budget": 0,
        "output_type": '',
        "num_restarts": 0,
        "items": []
    }
    # retrieve target value, budget, output type, and num_restarts from first line
    with open(file_path, 'r') as file:
        first_line = file.readline().split()
        file_info["target"] = int(first_line[0])
        file_info["budget"] = int(first_line[1])
        file_info["output_type"] = first_line[2]
        file_info["num_restarts"] = int(first_line[3])
        # create an Item for each line and store in the list of items
        for line in file:
            name, value_str, cost_str = line.strip().split()
            item = Item(name, int(value_str), int(cost_str))
            file_info["items"].append(item)

    return file_info


# function to return item.name for sort function
def get_item_name(item):
    return item.name


def generate_neighbors(state, file_info):
    # clear to prevent duplicate neighbors
    state.neighbors.clear()

    # generate neighbors by adding each item not in the current state
    for item in file_info["items"]:
        if item not in state.items:
            new_items = state.items + [item]
            # sort the items in the list alphabetically by item.name
            new_items.sort(key=get_item_name)
            new_state = State(new_items, state.total_value + item.value, state.total_cost + item.cost)
            new_state.calculate_error(file_info)
            state.add_neighbor(new_state)

    # generate neighbors by removing each item in the current state
    if len(state.items) > 0:
        for item in state.items:
            new_items = [i for i in state.items if i != item]
            new_items.sort(key=get_item_name)
            new_total_value = sum(i.value for i in new_items)
            new_total_cost = sum(i.cost for i in new_items)
            new_state = State(new_items, new_total_value, new_total_cost)
            new_state.calculate_error(file_info)
            state.add_neighbor(new_state)


# function to return state.error for min function
def get_state_error(state):
    return state.error


def hill_climbing_search(curr_state, file_info):
    # generate/update neighbors for current state
    generate_neighbors(curr_state, file_info)
    if file_info["output_type"] == 'V':
        print("Neighbors:")
        for neighbor in curr_state.neighbors:
            item_names = [item.name for item in neighbor.items]
            # put item names into a string separated by spaces
            items_str = ' '.join(item_names)
            print(f"{{{items_str}}}. Value = {neighbor.total_value}. Cost = {neighbor.total_cost}. Error = {neighbor.error}.")

    # find neighbor with smallest error
    next_state = min(curr_state.neighbors, key=get_state_error)

    # if next state is better than current state, move and repeat search
    if next_state.error < curr_state.error and next_state.items:
        if file_info["output_type"] == 'V':
            item_names = [item.name for item in next_state.items]
            # put item names into a string separated by spaces
            items_str = ' '.join(item_names)
            print(f"\nMove to {{{items_str}}}. Value = {next_state.total_value}. Cost = {next_state.total_cost}. Error = {next_state.error}.")
        return hill_climbing_search(next_state, file_info)
    # current state is local minimum
    else:
        return curr_state


def generate_random_initial_state(items):
    random_items = random.sample(items, random.randint(1, len(items)))
    random_items.sort(key=get_item_name)
    # calculate total value and cost for items
    total_value = sum(item.value for item in random_items)
    total_cost = sum(item.cost for item in random_items)
    # create and return the random initial state
    return State(random_items, total_value, total_cost)


def main():
    file_path = "hill_climbing_input.txt"
    file_info = read_file(file_path)

    solutions = []
    for i in range(file_info["num_restarts"]):
        initial_state = generate_random_initial_state(file_info["items"])
        initial_state.calculate_error(file_info)
        if file_info["output_type"] == 'V':
            item_names = [item.name for item in initial_state.items]
            items_str = ' '.join(item_names)
            print("\nRandomly chosen starting state:")
            print(f"{{{items_str}}}. Value = {initial_state.total_value}. Cost = {initial_state.total_cost}. Error = {initial_state.error}.")
        result_state = hill_climbing_search(initial_state, file_info)
        solutions.append(result_state)
    best_solution = min(solutions, key=get_state_error)

    if file_info["output_type"] == 'C':
        item_names = [item.name for item in best_solution.items]
        items_str = ' '.join(item_names)
        print(items_str)

    elif file_info["output_type"] == 'V':
        item_names = [item.name for item in best_solution.items]
        items_str = ' '.join(item_names)
        print(f"\nFound Solution: {{{items_str}}}. Value = {best_solution.total_value}. Cost = {best_solution.total_cost}. Error = {best_solution.error}.")


if __name__ == '__main__':
    main()
