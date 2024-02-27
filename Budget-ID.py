# an Item has a name, value, and cost
class Item:
    def __init__(self, name, value, cost):
        self.name = name
        self.value = value
        self.cost = cost


# a Node is a state containing a list of items, the total value, and the total cost
class Node:
    def __init__(self, items=[], total_value=0, total_cost=0):
        self.items = items
        self.total_value = total_value
        self.total_cost = total_cost
        self.children = []


def read_file(file_path):
    # create dictionary with target value, budget, output type, and a list of items
    file_info = {
        "target": 0,
        "budget": 0,
        "output_type": '',
        "items": []
    }
    # retrieve target value, budget, and output type from first line
    with open(file_path, 'r') as file:
        first_line = file.readline().split()
        file_info["target"] = int(first_line[0])
        file_info["budget"] = int(first_line[1])
        file_info["output_type"] = first_line[2]
        # create an Item for each line and store in the list of items
        for line in file:
            name, value_str, cost_str = line.strip().split()
            item = Item(name, int(value_str), int(cost_str))
            file_info["items"].append(item)

    return file_info


# function to return item.name for sort function
def get_item_name(item):
    return item.name


def build_search_tree(file_info):
    # root node (initial state) is an empty set
    root = Node()
    # sort the items in the list alphabetically by item.name
    file_info["items"].sort(key=get_item_name)
    build_tree_recursive(root, file_info["items"], 0, file_info["budget"])
    return root


def build_tree_recursive(node, items, index, budget):
    if index >= len(items):
        return
    for i in range(index, len(items)):
        item = items[i]
        # only add current item if does not exceed budget
        if node.total_cost + item.cost <= budget:
            # create a new node with current item added to current state
            new_items = node.items + [item]
            new_total_value = node.total_value + item.value
            new_total_cost = node.total_cost + item.cost
            new_node = Node(new_items, new_total_value, new_total_cost)
            node.children.append(new_node)
            # recursively add more items
            build_tree_recursive(new_node, items, i + 1, budget)


def iterative_deepening_search(root, target, output_type, max_depth=100):
    for depth in range(1, max_depth):
        if output_type == 'V':
            print()
            print("Depth =", depth)
        result = depth_limited_search(root, target, output_type, depth)
        if result is not None:
            return result
    return None


def depth_limited_search(node, target,  output_type, limit, depth=0):
    if output_type == 'V':
        item_names = [item.name for item in node.items]
        # put item names into a string separated by spaces
        items_str = ' '.join(item_names)
        print(f"{{{items_str}}}. Value = {node.total_value}. Cost = {node.total_cost}.")
    # if current state meets target value, return
    if node.total_value >= target:
        return node
    # else if depth limit is reached, return none
    elif depth == limit:
        return None
    else:
        for child in node.children:
            # call DLS for each successor (with depth extended one level)
            result = depth_limited_search(child, target, output_type, limit, depth + 1)
            if result is not None:
                return result
    return None


def main():
    file_path = "iterative_deepening_input.txt"
    file_info = read_file(file_path)
    root = build_search_tree(file_info)
    result_node = iterative_deepening_search(root, file_info["target"], file_info["output_type"])

    if file_info["output_type"] == 'C':
        if result_node is not None:
            item_names = [item.name for item in result_node.items]
            items_str = ' '.join(item_names)
            print(items_str)
        else:
            print("\nNo Solution")

    elif file_info["output_type"] == 'V':
        if result_node is not None:
            item_names = [item.name for item in result_node.items]
            items_str = ' '.join(item_names)
            print(f"\nFound Solution: {{{items_str}}}. Value = {result_node.total_value}. Cost = {result_node.total_cost}.")
        else:
            print("\nNo Solution")


if __name__ == '__main__':
    main()
